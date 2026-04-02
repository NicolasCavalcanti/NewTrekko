/**
 * One-time script: removes guide BRUNO BREVES FIGUEIREDO (CADASTUR 19025263967)
 * from the cadasturRegistry table.
 *
 * Usage: DATABASE_URL=... pnpm tsx scripts/remove-guide-19025263967.ts
 */

import 'dotenv/config';
import { drizzle } from 'drizzle-orm/mysql2';
import { eq } from 'drizzle-orm';
import { cadasturRegistry } from '../drizzle/schema.js';

const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) {
  console.error('DATABASE_URL is not set.');
  process.exit(1);
}

const db = drizzle(dbUrl);
const CADASTUR_NUMBER = '19025263967';

const existing = await db
  .select()
  .from(cadasturRegistry)
  .where(eq(cadasturRegistry.certificateNumber, CADASTUR_NUMBER))
  .limit(1);

if (existing.length === 0) {
  console.log(`Guide ${CADASTUR_NUMBER} not found in cadasturRegistry — nothing to do.`);
  process.exit(0);
}

console.log(`Removing: ${existing[0].fullName} (${CADASTUR_NUMBER})`);

await db
  .delete(cadasturRegistry)
  .where(eq(cadasturRegistry.certificateNumber, CADASTUR_NUMBER));

console.log('Done.');
process.exit(0);
