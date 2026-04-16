/**
 * Post-export patch: fixes swapped images between
 * "Travessia Lençóis Maranhenses" and "Cânion do Guartelá".
 *
 * Background: The images for these two trails were accidentally stored in
 * swapped order in the database (Lençóis shows Guartelá scenery and vice versa).
 * This script detects the swap by checking whether Lençóis' imageUrl actually
 * references a Lençóis image (URL path contains "lencois"), and corrects it
 * by swapping `imageUrl` and `images` between the two trails in trails.json.
 *
 * Idempotent: once the swap has been applied (or if the DB is later fixed so
 * that the URLs already point to the right trail), the script is a no-op.
 *
 * Usage: node scripts/patch-trail-images.mjs
 * Run after scripts/export-trails-static.ts in the CI pipeline.
 *
 * NOTE: Remove this script from the workflow once the underlying DB data has
 * been corrected.
 */

import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const trailsJsonPath = join(__dirname, '..', 'client', 'public', 'data', 'trails.json');

// ── Load trails.json ─────────────────────────────────────────────────────────

let trails;
try {
  trails = JSON.parse(readFileSync(trailsJsonPath, 'utf-8'));
} catch {
  console.log('[patch-trail-images] trails.json not found or invalid — skipping.');
  process.exit(0);
}

if (!Array.isArray(trails)) {
  console.log('[patch-trail-images] trails.json is not an array — skipping.');
  process.exit(0);
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function normalize(str) {
  return (str ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

// ── Find the two affected trails ─────────────────────────────────────────────

const lencoisIdx = trails.findIndex(
  (t) =>
    normalize(t.name).includes('lencois') ||
    normalize(t.slug ?? '').includes('lencois'),
);

const guartelaIdx = trails.findIndex(
  (t) =>
    normalize(t.name).includes('guartela') ||
    normalize(t.slug ?? '').includes('guartela'),
);

if (lencoisIdx === -1) {
  console.log('[patch-trail-images] Lençóis trail not found in trails.json — skipping.');
  process.exit(0);
}

if (guartelaIdx === -1) {
  console.log('[patch-trail-images] Guartelá trail not found in trails.json — skipping.');
  process.exit(0);
}

const lencois = trails[lencoisIdx];
const guartela = trails[guartelaIdx];

// ── Detect whether a swap is needed ──────────────────────────────────────────
//
// The Lençóis images were uploaded to CloudFront under the slug
// "lencois-maranhenses", so their URLs contain "lencois".
// If the current imageUrl of the Lençóis trail does NOT contain "lencois"
// (or "maranhens"), the images are swapped and need to be corrected.
//
// Also handles the case where images are stored as local /trails/ paths:
// the known-correct local Lençóis filenames are checked explicitly.

const LENCOIS_KNOWN_FILES = new Set([
  '4oJtSdUBL70H.jpg',
  'nKxhMLPUSf7M.jpg',
  'JTRpXweC3hBk.jpg',
  'ytDfSS1F173W.jpg',
]);

function looksLikeLencoisImage(url) {
  if (!url) return false;
  const u = normalize(url);
  if (u.includes('lencois') || u.includes('maranhens')) return true;
  // Check known local filenames
  const filename = url.split('/').pop() ?? '';
  return LENCOIS_KNOWN_FILES.has(filename);
}

const imageUrlOfLencois = lencois.imageUrl ?? (lencois.images?.[0] ?? '');

if (looksLikeLencoisImage(imageUrlOfLencois)) {
  console.log('[patch-trail-images] Images appear correct already — no swap needed.');
  process.exit(0);
}

// ── Apply the swap ────────────────────────────────────────────────────────────

console.log(
  `[patch-trail-images] Swapping images between "${lencois.name}" (idx ${lencoisIdx}) ` +
  `and "${guartela.name}" (idx ${guartelaIdx})...`,
);

const savedImages    = lencois.images;
const savedImageUrl  = lencois.imageUrl;

trails[lencoisIdx] = { ...lencois,  images: guartela.images,  imageUrl: guartela.imageUrl  };
trails[guartelaIdx] = { ...guartela, images: savedImages,      imageUrl: savedImageUrl       };

writeFileSync(trailsJsonPath, JSON.stringify(trails));

console.log('[patch-trail-images] Done — images corrected.');
