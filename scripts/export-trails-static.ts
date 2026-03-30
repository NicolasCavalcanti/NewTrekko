/**
 * Build-time script: exports all published trails from the DB to
 * client/public/data/trails.json so the static GitHub Pages deployment
 * can display them without a backend.
 *
 * Usage: pnpm tsx scripts/export-trails-static.ts
 * Requires DATABASE_URL env var.
 */

import 'dotenv/config';
import { drizzle } from 'drizzle-orm/mysql2';
import { eq, desc } from 'drizzle-orm';
import { trails } from '../drizzle/schema.js';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) {
  console.error('[export-trails-static] DATABASE_URL is not set — skipping export.');
  process.exit(0);
}

const db = drizzle(dbUrl);

console.log('[export-trails-static] Fetching trails from DB...');

const allTrails = await db
  .select()
  .from(trails)
  .where(eq(trails.status, 'published'))
  .orderBy(desc(trails.viewCount));

const output = allTrails.map((t) => ({
  id: t.id,
  name: t.name,
  slug: t.slug ?? null,
  uf: t.uf,
  city: t.city ?? null,
  region: t.region ?? null,
  park: t.park ?? null,
  distanceKm: t.distanceKm ?? null,
  elevationGain: t.elevationGain ?? null,
  maxAltitude: t.maxAltitude ?? null,
  difficulty: t.difficulty ?? null,
  description: t.description ?? null,
  shortDescription: t.shortDescription ?? null,
  hookText: t.hookText ?? null,
  ctaText: t.ctaText ?? null,
  guideRequired: t.guideRequired ?? 0,
  entranceFee: t.entranceFee ?? null,
  waterPoints: t.waterPoints ?? null,
  campingPoints: t.campingPoints ?? null,
  bestSeason: t.bestSeason ?? null,
  estimatedTime: t.estimatedTime ?? null,
  trailType: t.trailType ?? null,
  imageUrl: t.imageUrl ?? null,
  images: t.images ?? null,
  highlights: t.highlights ?? null,
  wiklocUrl: t.wiklocUrl ?? null,
  wiklocGpxUrl: t.wiklocGpxUrl ?? null,
  viewCount: t.viewCount ?? 0,
  status: t.status,
}));

const outputDir = join(process.cwd(), 'client', 'public', 'data');
mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'trails.json'), JSON.stringify(output));

console.log(`[export-trails-static] Done — exported ${output.length} trails.`);
process.exit(0);
