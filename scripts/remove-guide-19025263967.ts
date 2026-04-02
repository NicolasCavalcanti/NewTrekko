/**
 * One-time script: completely removes guide BRUNO BREVES FIGUEIREDO (CADASTUR 19025263967)
 * from both the cadasturRegistry and users tables.
 *
 * Usage: DATABASE_URL=... pnpm tsx scripts/remove-guide-19025263967.ts
 */

import 'dotenv/config';
import { drizzle } from 'drizzle-orm/mysql2';
import { eq, and, sql } from 'drizzle-orm';
import { cadasturRegistry, users } from '../drizzle/schema.js';

const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) {
  console.error('DATABASE_URL is not set.');
  process.exit(1);
}

const db = drizzle(dbUrl);
const CADASTUR_NUMBER = '19025263967';
const EMAIL = 'brunobrevesfigueiredo@protonmail.com';

// Remove from cadasturRegistry
const existing = await db
  .select()
  .from(cadasturRegistry)
  .where(eq(cadasturRegistry.certificateNumber, CADASTUR_NUMBER))
  .limit(1);

if (existing.length > 0) {
  console.log(`Removing from cadasturRegistry: ${existing[0].fullName} (${CADASTUR_NUMBER})`);
  await db.delete(cadasturRegistry).where(eq(cadasturRegistry.certificateNumber, CADASTUR_NUMBER));
} else {
  console.log(`Not found in cadasturRegistry — already removed or never existed.`);
}

// Remove from users table (by email and/or cadasturNumber)
const userRows = await db
  .select({ id: users.id, email: users.email })
  .from(users)
  .where(
    sql`${users.email} = ${EMAIL} OR ${users.cadasturNumber} = ${CADASTUR_NUMBER}`
  );

if (userRows.length > 0) {
  for (const u of userRows) {
    console.log(`Removing from users: id=${u.id} email=${u.email}`);
  }
  await db.delete(users).where(
    sql`${users.email} = ${EMAIL} OR ${users.cadasturNumber} = ${CADASTUR_NUMBER}`
  );
} else {
  console.log(`Not found in users table — not a registered Trekko user.`);
}

console.log('Done.');
process.exit(0);
