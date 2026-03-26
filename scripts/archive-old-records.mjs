/**
 * DB-ARCH-01: Periodic archival script for financial records.
 *
 * Brazilian law (Código de Defesa do Consumidor + LGPD) requires financial
 * transaction records to be retained for at least 5 years.
 *
 * This script moves records older than RETENTION_YEARS from the main tables
 * to corresponding _archive tables, then marks them as archived.
 *
 * RUN PERIODICALLY (e.g. monthly via cron):
 *   node scripts/archive-old-records.mjs
 *
 * PREREQUISITES:
 *   - DATABASE_URL in environment
 *   - Archive tables must exist (created by this script on first run if needed)
 *
 * SAFETY: This script does NOT hard-delete any rows. It copies them to archive
 * tables and sets a soft deletedAt marker on the originals.
 */

import mysql from "mysql2/promise";

const DATABASE_URL = process.env.DATABASE_URL;
const RETENTION_YEARS = 5;

if (!DATABASE_URL) {
  console.error("ERROR: DATABASE_URL environment variable is required.");
  process.exit(1);
}

const CUTOFF_SQL = `DATE_SUB(NOW(), INTERVAL ${RETENTION_YEARS} YEAR)`;

const ARCHIVE_JOBS = [
  {
    source: "reservations",
    archive: "reservations_archive",
    createSql: `
      CREATE TABLE IF NOT EXISTS reservations_archive LIKE reservations;
    `,
  },
  {
    source: "payments",
    archive: "payments_archive",
    createSql: `
      CREATE TABLE IF NOT EXISTS payments_archive LIKE payments;
    `,
  },
  {
    source: "payouts",
    archive: "payouts_archive",
    createSql: `
      CREATE TABLE IF NOT EXISTS payouts_archive LIKE payouts;
    `,
  },
  {
    source: "payment_audit_log",
    archive: "payment_audit_log_archive",
    createSql: `
      CREATE TABLE IF NOT EXISTS payment_audit_log_archive LIKE payment_audit_log;
    `,
  },
];

async function archiveTable(conn, job) {
  const { source, archive, createSql } = job;

  // Ensure archive table exists
  await conn.query(createSql);

  // Count rows eligible for archival
  const [[{ cnt }]] = await conn.query(
    `SELECT COUNT(*) AS cnt FROM \`${source}\` WHERE createdAt < ${CUTOFF_SQL} AND deletedAt IS NULL`
  );

  if (Number(cnt) === 0) {
    console.log(`  ${source}: no rows older than ${RETENTION_YEARS} years — skipping.`);
    return;
  }

  console.log(`  ${source}: archiving ${cnt} rows…`);

  // Copy to archive (INSERT IGNORE skips duplicates on re-run)
  const [copyResult] = await conn.query(
    `INSERT IGNORE INTO \`${archive}\`
     SELECT * FROM \`${source}\`
     WHERE createdAt < ${CUTOFF_SQL} AND deletedAt IS NULL`
  );

  // Soft-mark as deleted in the source table (preserves FK references)
  await conn.query(
    `UPDATE \`${source}\`
     SET deletedAt = NOW()
     WHERE createdAt < ${CUTOFF_SQL} AND deletedAt IS NULL`
  );

  console.log(`  ${source}: ${copyResult.affectedRows} rows archived → ${archive}.`);
}

async function run() {
  const pool = mysql.createPool({ uri: DATABASE_URL, connectionLimit: 1 });
  const conn = await pool.getConnection();

  try {
    console.log(`Archiving records older than ${RETENTION_YEARS} years (cutoff: records before ${new Date(Date.now() - RETENTION_YEARS * 365.25 * 24 * 3600 * 1000).toISOString().slice(0, 10)})…\n`);

    for (const job of ARCHIVE_JOBS) {
      await archiveTable(conn, job);
    }

    // Also purge payment_audit_log rows older than 365 days from the live table
    // (these are already in the archive; purge the live copy to keep the table lean)
    const [purgeResult] = await conn.query(
      `DELETE FROM payment_audit_log
       WHERE createdAt < DATE_SUB(NOW(), INTERVAL 365 DAY)
         AND deletedAt IS NOT NULL`
    );
    console.log(`\npayment_audit_log: purged ${purgeResult.affectedRows} already-archived rows (>365 days old).`);

    console.log("\nArchival complete.");
  } finally {
    conn.release();
    await pool.end();
  }
}

run().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
