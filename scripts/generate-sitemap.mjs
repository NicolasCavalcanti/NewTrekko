/**
 * Sitemap generator for the Trekko static GitHub Pages build.
 *
 * Run:  node scripts/generate-sitemap.mjs
 *   or: pnpm sitemap
 *
 * Reads the three pre-generated JSON data files and writes
 * client/public/sitemap.xml following the same indexability policy
 * as the React app:
 *
 *   /trilha/:id   all published trails
 *   /blog/:slug   all published posts
 *   /guia/:id     only guides that pass isGuideIndexable()
 *
 * Legal, institutional, functional and authenticated routes are excluded.
 */

import { readFileSync, writeFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR  = join(__dirname, "../client/public/data");
const OUT_PATH  = join(__dirname, "../client/public/sitemap.xml");
const BASE_URL  = "https://trekko.com.br";

// ── Indexability logic (mirrors client/src/lib/guideIndexability.ts) ─────────

const MIN_BIO_CHARS = 80;

function isGuideIndexable(guide, expeditionCount = 0) {
  if (!guide.name?.trim() || !guide.uf) return false;
  const hasEditorialContent = (guide.bio?.trim().length ?? 0) >= MIN_BIO_CHARS;
  const hasPlatformPresence = Boolean(guide.isVerified);
  const hasActiveExpeditions = expeditionCount >= 1;
  return hasEditorialContent || hasPlatformPresence || hasActiveExpeditions;
}

// ── XML helpers ───────────────────────────────────────────────────────────────

function xmlEscape(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function urlEntry(loc, { lastmod, changefreq, priority }) {
  const lines = ["  <url>", `    <loc>${xmlEscape(loc)}</loc>`];
  if (lastmod)    lines.push(`    <lastmod>${lastmod}</lastmod>`);
  if (changefreq) lines.push(`    <changefreq>${changefreq}</changefreq>`);
  if (priority)   lines.push(`    <priority>${priority}</priority>`);
  lines.push("  </url>");
  return lines.join("\n");
}

const today = new Date().toISOString().slice(0, 10);

// ── 1. Static pages ───────────────────────────────────────────────────────────
// Included:  discovery and high-value navigational pages
// Excluded:  legal (/termos /privacidade /politica-editorial)
//            institutional (/sobre /contato)
//            authenticated (/perfil /admin /reservas /checkout)

const STATIC_PAGES = [
  { path: "/",       changefreq: "weekly",  priority: "1.0" },
  { path: "/trilhas", changefreq: "weekly",  priority: "0.9" },
  { path: "/blog",   changefreq: "weekly",  priority: "0.8" },
  { path: "/guias",  changefreq: "monthly", priority: "0.7" },
];

const staticEntries = STATIC_PAGES.map((p) =>
  urlEntry(`${BASE_URL}${p.path}`, {
    lastmod: today,
    changefreq: p.changefreq,
    priority: p.priority,
  })
);

// ── 2. Trail detail pages ─────────────────────────────────────────────────────
// Route: /trilha/:id  (numeric id, see useTrailById)

const trails = JSON.parse(readFileSync(join(DATA_DIR, "trails.json"), "utf-8"));

const trailEntries = trails
  .filter((t) => t.status === "published")
  .map((t) =>
    urlEntry(`${BASE_URL}/trilha/${t.id}`, {
      lastmod: today,
      changefreq: "monthly",
      priority: "0.9",
    })
  );

// ── 3. Blog post pages ────────────────────────────────────────────────────────
// Route: /blog/:slug

const posts = JSON.parse(readFileSync(join(DATA_DIR, "blog.json"), "utf-8"));

const blogEntries = posts
  .filter((p) => p.status === "published" && p.slug)
  .map((p) => {
    const lastmod = p.updatedAt
      ? new Date(p.updatedAt).toISOString().slice(0, 10)
      : today;
    return urlEntry(`${BASE_URL}/blog/${xmlEscape(p.slug)}`, {
      lastmod,
      changefreq: "monthly",
      priority: "0.8",
    });
  });

// ── 4. Guide pages — indexable guides only ────────────────────────────────────
// Route: /guia/:cadasturNumber
// Thin CADASTUR-scraped entries (non-verified, no bio) are excluded.

const guides = JSON.parse(readFileSync(join(DATA_DIR, "guides.json"), "utf-8"));

const indexableGuides = guides.filter((g) => isGuideIndexable(g));

const guideEntries = indexableGuides.map((g) =>
  urlEntry(`${BASE_URL}/guia/${encodeURIComponent(g.cadasturNumber)}`, {
    lastmod: today,
    changefreq: "monthly",
    priority: "0.6",
  })
);

// ── Build and write ───────────────────────────────────────────────────────────

const allEntries = [
  ...staticEntries,
  ...trailEntries,
  ...blogEntries,
  ...guideEntries,
];

const sitemap = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...allEntries,
  "</urlset>",
].join("\n");

writeFileSync(OUT_PATH, sitemap, "utf-8");

console.log("sitemap.xml generated");
console.log(`  static pages : ${staticEntries.length}`);
console.log(`  trail pages  : ${trailEntries.length}`);
console.log(`  blog posts   : ${blogEntries.length}`);
console.log(`  guide pages  : ${guideEntries.length} of ${guides.length} total (${guides.length - indexableGuides.length} excluded as thin content)`);
console.log(`  total URLs   : ${allEntries.length}`);
console.log(`  output       : ${OUT_PATH}`);
