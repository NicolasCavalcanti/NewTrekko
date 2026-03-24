#!/usr/bin/env tsx
/**
 * One-time migration: rewrite stored image URLs to CDN URLs.
 *
 * Run after CDN_ORIGIN and DATABASE_URL are set in the environment:
 *
 *   CDN_ORIGIN=https://cdn.trekko.com.br \
 *   DATABASE_URL=mysql://... \
 *   npx tsx scripts/migrate-cdn-urls.ts
 *
 * The script is idempotent — rows already pointing at the CDN are skipped.
 * Pass --dry-run to preview changes without writing to the database.
 *
 * Tables updated:
 *   trails        — imageUrl (text), images (json string[])
 *   blog_posts    — imageUrl (text), images (json string[])
 *   review_images — imageUrl (text)
 */

import { drizzle } from "drizzle-orm/mysql2";
import { sql } from "drizzle-orm";

const CDN_ORIGIN = process.env.CDN_ORIGIN?.replace(/\/+$/, "");
const DATABASE_URL = process.env.DATABASE_URL;
const DRY_RUN = process.argv.includes("--dry-run");

if (!CDN_ORIGIN) {
  console.error("Error: CDN_ORIGIN env var is required.");
  process.exit(1);
}
if (!DATABASE_URL) {
  console.error("Error: DATABASE_URL env var is required.");
  process.exit(1);
}

const db = drizzle(DATABASE_URL);

// ─── Helpers ────────────────────────────────────────────────────────────────

/**
 * Rewrite a single stored URL to CDN.  Returns the original string unchanged
 * when it is already a CDN URL, is empty, or cannot be parsed.
 */
function toCdn(stored: string | null | undefined): string | null | undefined {
  if (!stored) return stored;
  if (stored.startsWith(CDN_ORIGIN!)) return stored; // already CDN

  try {
    const parsed = new URL(stored);
    // Manus proxy download URL — key is the `path` query param
    const pathParam = parsed.searchParams.get("path");
    if (pathParam) {
      return `${CDN_ORIGIN}/${pathParam.replace(/^\/+/, "")}`;
    }
    // Direct S3 / other URL — use pathname as key
    const key = parsed.pathname.replace(/^\/+/, "");
    if (key) return `${CDN_ORIGIN}/${key}`;
  } catch {
    // Not a valid URL, leave as-is
  }
  return stored;
}

function rewriteJsonArray(jsonVal: string | null | undefined): string | null {
  if (!jsonVal) return jsonVal ?? null;
  try {
    const arr: string[] = JSON.parse(jsonVal);
    if (!Array.isArray(arr)) return jsonVal;
    const rewritten = arr.map((u) => toCdn(u) ?? u);
    // Only return new JSON when something actually changed
    const changed = rewritten.some((v, i) => v !== arr[i]);
    return changed ? JSON.stringify(rewritten) : jsonVal;
  } catch {
    return jsonVal;
  }
}

let totalUpdated = 0;

// ─── trails ──────────────────────────────────────────────────────────────────

async function migrateTrails() {
  const [rows] = await db.execute(sql`SELECT id, imageUrl, images FROM trails`);
  const trail_rows = rows as Array<{ id: number; imageUrl: string | null; images: string | null }>;

  let count = 0;
  for (const row of trail_rows) {
    const newImageUrl = toCdn(row.imageUrl) ?? null;
    const newImages = rewriteJsonArray(row.images);

    const imageUrlChanged = newImageUrl !== row.imageUrl;
    const imagesChanged = newImages !== row.images;

    if (!imageUrlChanged && !imagesChanged) continue;

    count++;
    if (DRY_RUN) {
      console.log(`[DRY] trails id=${row.id}  imageUrl: ${row.imageUrl} → ${newImageUrl}`);
      continue;
    }

    if (imageUrlChanged && imagesChanged) {
      await db.execute(
        sql`UPDATE trails SET imageUrl = ${newImageUrl}, images = ${newImages} WHERE id = ${row.id}`
      );
    } else if (imageUrlChanged) {
      await db.execute(
        sql`UPDATE trails SET imageUrl = ${newImageUrl} WHERE id = ${row.id}`
      );
    } else {
      await db.execute(
        sql`UPDATE trails SET images = ${newImages} WHERE id = ${row.id}`
      );
    }
  }

  console.log(`trails: ${count} row(s) ${DRY_RUN ? "would be" : ""} updated`);
  totalUpdated += count;
}

// ─── blog_posts ───────────────────────────────────────────────────────────────

async function migrateBlogPosts() {
  const [rows] = await db.execute(sql`SELECT id, imageUrl, images FROM blog_posts`);
  const blog_rows = rows as Array<{ id: number; imageUrl: string | null; images: string | null }>;

  let count = 0;
  for (const row of blog_rows) {
    const newImageUrl = toCdn(row.imageUrl) ?? null;
    const newImages = rewriteJsonArray(row.images);

    const imageUrlChanged = newImageUrl !== row.imageUrl;
    const imagesChanged = newImages !== row.images;

    if (!imageUrlChanged && !imagesChanged) continue;

    count++;
    if (DRY_RUN) {
      console.log(`[DRY] blog_posts id=${row.id}  imageUrl: ${row.imageUrl} → ${newImageUrl}`);
      continue;
    }

    if (imageUrlChanged && imagesChanged) {
      await db.execute(
        sql`UPDATE blog_posts SET imageUrl = ${newImageUrl}, images = ${newImages} WHERE id = ${row.id}`
      );
    } else if (imageUrlChanged) {
      await db.execute(
        sql`UPDATE blog_posts SET imageUrl = ${newImageUrl} WHERE id = ${row.id}`
      );
    } else {
      await db.execute(
        sql`UPDATE blog_posts SET images = ${newImages} WHERE id = ${row.id}`
      );
    }
  }

  console.log(`blog_posts: ${count} row(s) ${DRY_RUN ? "would be" : ""} updated`);
  totalUpdated += count;
}

// ─── review_images ────────────────────────────────────────────────────────────

async function migrateReviewImages() {
  const [rows] = await db.execute(sql`SELECT id, imageUrl FROM review_images`);
  const ri_rows = rows as Array<{ id: number; imageUrl: string }>;

  let count = 0;
  for (const row of ri_rows) {
    const newImageUrl = toCdn(row.imageUrl) ?? row.imageUrl;
    if (newImageUrl === row.imageUrl) continue;

    count++;
    if (DRY_RUN) {
      console.log(`[DRY] review_images id=${row.id}  ${row.imageUrl} → ${newImageUrl}`);
      continue;
    }

    await db.execute(
      sql`UPDATE review_images SET imageUrl = ${newImageUrl} WHERE id = ${row.id}`
    );
  }

  console.log(`review_images: ${count} row(s) ${DRY_RUN ? "would be" : ""} updated`);
  totalUpdated += count;
}

// ─── Main ────────────────────────────────────────────────────────────────────

(async () => {
  console.log(`CDN origin: ${CDN_ORIGIN}`);
  if (DRY_RUN) console.log("DRY RUN — no changes will be written\n");

  await migrateTrails();
  await migrateBlogPosts();
  await migrateReviewImages();

  console.log(`\nDone. Total rows ${DRY_RUN ? "to update" : "updated"}: ${totalUpdated}`);
  process.exit(0);
})();
