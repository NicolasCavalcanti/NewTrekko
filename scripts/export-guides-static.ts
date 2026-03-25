/**
 * Build-time script: exports all CADASTUR guides from the DB to
 * client/public/data/guides.json so the static GitHub Pages deployment
 * can display them without a backend.
 *
 * Usage: pnpm tsx scripts/export-guides-static.ts
 * Requires DATABASE_URL env var.
 */

import 'dotenv/config';
import { drizzle } from 'drizzle-orm/mysql2';
import { eq, and, asc, sql } from 'drizzle-orm';
import { cadasturRegistry, users } from '../drizzle/schema.js';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) {
  console.error('[export-guides-static] DATABASE_URL is not set — skipping export.');
  process.exit(0);
}

const db = drizzle(dbUrl);

console.log('[export-guides-static] Fetching guides from DB...');

const allCadastur = await db
  .select()
  .from(cadasturRegistry)
  .orderBy(asc(cadasturRegistry.fullName));

const registeredGuides = await db
  .select({ cadasturNumber: users.cadasturNumber })
  .from(users)
  .where(and(eq(users.userType, 'guide'), sql`${users.cadasturNumber} IS NOT NULL`));

const registeredSet = new Set(registeredGuides.map((g) => g.cadasturNumber));

const guides = allCadastur.map((c) => ({
  id: c.id,
  name: c.fullName,
  cadasturNumber: c.certificateNumber,
  uf: c.uf,
  city: c.city ?? null,
  phone: c.phone ?? null,
  email: c.email ?? null,
  website: c.website ?? null,
  languages: c.languages ?? null,
  categories: c.categories ?? null,
  segments: c.segments ?? null,
  validUntil: c.validUntil ? c.validUntil.toISOString() : null,
  isVerified: registeredSet.has(c.certificateNumber),
  isDriverGuide: c.isDriverGuide === 1,
}));

// Verified first, then alphabetically — mirrors the DB sort in storage.ts
guides.sort((a, b) => {
  if (a.isVerified !== b.isVerified) return a.isVerified ? -1 : 1;
  return (a.name || '').localeCompare(b.name || '', 'pt-BR');
});

const outputDir = join(process.cwd(), 'client', 'public', 'data');
mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'guides.json'), JSON.stringify(guides));

console.log(`[export-guides-static] Done — exported ${guides.length} guides.`);
process.exit(0);
