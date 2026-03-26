/**
 * DB-SEC-01: One-time migration script — encrypt existing guide_verification PII.
 *
 * This script reads all guide_verification rows whose sensitive columns contain
 * plaintext values (detected by checking whether the value matches the expected
 * AES-256-GCM ciphertext format iv:tag:ciphertext) and re-saves them encrypted.
 *
 * PREREQUISITES:
 *   1. Set DB_ENCRYPTION_KEY in your environment (64-char hex string).
 *      node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
 *   2. Set DATABASE_URL in your environment.
 *
 * RUN ONCE:
 *   node scripts/encrypt-existing-guide-data.mjs
 *
 * This script is idempotent — rows that are already encrypted (value contains
 * exactly two colons in the expected iv:tag:ct format) are skipped.
 */

import mysql from "mysql2/promise";
import { createCipheriv, randomBytes } from "node:crypto";

const DATABASE_URL = process.env.DATABASE_URL;
const ENCRYPTION_KEY_HEX = process.env.DB_ENCRYPTION_KEY;

if (!DATABASE_URL) {
  console.error("ERROR: DATABASE_URL environment variable is required.");
  process.exit(1);
}

if (!ENCRYPTION_KEY_HEX || ENCRYPTION_KEY_HEX.length !== 64) {
  console.error(
    "ERROR: DB_ENCRYPTION_KEY must be a 64-character hex string (32 bytes).\n" +
    "Generate one with: node -e \"console.log(require('crypto').randomBytes(32).toString('hex'))\""
  );
  process.exit(1);
}

const KEY = Buffer.from(ENCRYPTION_KEY_HEX, "hex");
const ALGORITHM = "aes-256-gcm";
const IV_BYTES = 12;
const SEPARATOR = ":";

function encrypt(value) {
  if (value == null) return null;
  const iv = randomBytes(IV_BYTES);
  const cipher = createCipheriv(ALGORITHM, KEY, iv);
  const ct = Buffer.concat([cipher.update(value, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return [iv.toString("hex"), tag.toString("hex"), ct.toString("hex")].join(SEPARATOR);
}

/** Returns true if the string looks like it was already encrypted by our scheme. */
function isAlreadyEncrypted(value) {
  if (typeof value !== "string") return false;
  const parts = value.split(SEPARATOR);
  // iv (24 hex chars) + tag (32 hex chars) + ciphertext (≥2 hex chars)
  return parts.length === 3 && parts[0].length === 24 && parts[1].length === 32;
}

const COLUMNS = ["documentNumber", "pixKey", "pixKeyDocument"];

async function run() {
  const pool = mysql.createPool({ uri: DATABASE_URL, connectionLimit: 1 });

  try {
    const [rows] = await pool.query(
      `SELECT id, documentNumber, pixKey, pixKeyDocument FROM guide_verification`
    );

    let updatedCount = 0;
    let skippedCount = 0;

    for (const row of rows) {
      const updates = {};

      for (const col of COLUMNS) {
        const val = row[col];
        if (val == null || isAlreadyEncrypted(val)) {
          // null or already ciphertext — skip
          continue;
        }
        updates[col] = encrypt(val);
      }

      if (Object.keys(updates).length === 0) {
        skippedCount++;
        continue;
      }

      const setClauses = Object.keys(updates)
        .map((col) => `\`${col}\` = ?`)
        .join(", ");
      const values = [...Object.values(updates), row.id];

      await pool.query(
        `UPDATE guide_verification SET ${setClauses}, updatedAt = NOW() WHERE id = ?`,
        values
      );
      updatedCount++;
      console.log(`  Encrypted guide_verification id=${row.id} (columns: ${Object.keys(updates).join(", ")})`);
    }

    console.log(`\nDone. Encrypted: ${updatedCount} rows. Skipped (already encrypted or null): ${skippedCount} rows.`);
  } finally {
    await pool.end();
  }
}

run().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});
