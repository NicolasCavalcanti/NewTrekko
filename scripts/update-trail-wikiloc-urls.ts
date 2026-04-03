/**
 * One-time script: sets wiklocUrl and wiklocGpxUrl for trails that have
 * confirmed Wikiloc entries.
 *
 * Usage: DATABASE_URL=... pnpm tsx scripts/update-trail-wikiloc-urls.ts
 */

import 'dotenv/config';
import { drizzle } from 'drizzle-orm/mysql2';
import { eq } from 'drizzle-orm';
import { trails } from '../drizzle/schema.js';

const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) {
  console.error('DATABASE_URL is not set.');
  process.exit(1);
}

const db = drizzle(dbUrl);

const WIKILOC_DATA: Array<{ id: number; wiklocUrl: string; wiklocGpxUrl: string }> = [
  {
    id: 2, // Travessia Petrópolis x Teresópolis
    wiklocUrl: 'https://pt.wikiloc.com/trilhas-trekking/travessia-petropolis-teresopolis-petro-x-tere-143686385',
    wiklocGpxUrl: 'https://www.wikiloc.com/wikiloc/download.do?id=143686385',
  },
  // Add more trails here as Wikiloc URLs are confirmed:
  // { id: 1, wiklocUrl: '...', wiklocGpxUrl: '...' }, // Monte Roraima
];

for (const entry of WIKILOC_DATA) {
  const existing = await db.select({ id: trails.id, name: trails.name })
    .from(trails)
    .where(eq(trails.id, entry.id))
    .limit(1);

  if (existing.length === 0) {
    console.log(`Trail id=${entry.id} not found — skipping.`);
    continue;
  }

  await db.update(trails)
    .set({ wiklocUrl: entry.wiklocUrl, wiklocGpxUrl: entry.wiklocGpxUrl } as any)
    .where(eq(trails.id, entry.id));

  console.log(`Updated: [${entry.id}] ${existing[0].name}`);
}

console.log('Done.');
process.exit(0);
