import { Router, Request, Response } from "express";
import { eq } from "drizzle-orm";
import { getDb } from "../db";
import { trails, blogPosts } from "../../drizzle/schema";

const router = Router();

const BASE_URL = process.env.SITE_URL?.replace(/\/$/, "") ?? "https://trekko.com.br";

function toW3CDate(date: Date | null | undefined): string {
  if (!date) return new Date().toISOString().split("T")[0];
  return date instanceof Date ? date.toISOString().split("T")[0] : new Date(date).toISOString().split("T")[0];
}

function urlEntry(
  loc: string,
  lastmod: string,
  changefreq: string,
  priority: string
): string {
  return `  <url>\n    <loc>${loc}</loc>\n    <lastmod>${lastmod}</lastmod>\n    <changefreq>${changefreq}</changefreq>\n    <priority>${priority}</priority>\n  </url>`;
}

router.get("/sitemap.xml", async (_req: Request, res: Response) => {
  const today = toW3CDate(new Date());

  const staticRoutes = [
    urlEntry(`${BASE_URL}/`, today, "daily", "1.0"),
    urlEntry(`${BASE_URL}/trilhas`, today, "daily", "0.8"),
    urlEntry(`${BASE_URL}/guias`, today, "weekly", "0.6"),
    urlEntry(`${BASE_URL}/blog`, today, "daily", "0.7"),
    urlEntry(`${BASE_URL}/sobre`, today, "monthly", "0.6"),
    urlEntry(`${BASE_URL}/contato`, today, "monthly", "0.6"),
    urlEntry(`${BASE_URL}/privacidade`, today, "monthly", "0.6"),
    urlEntry(`${BASE_URL}/termos`, today, "monthly", "0.6"),
  ];

  const dynamicEntries: string[] = [];

  try {
    const db = await getDb();

    if (db) {
      const [publishedTrails, publishedPosts] = await Promise.all([
        db
          .select({ id: trails.id, updatedAt: trails.updatedAt })
          .from(trails)
          .where(eq(trails.status, "published")),
        db
          .select({ slug: blogPosts.slug, updatedAt: blogPosts.updatedAt })
          .from(blogPosts)
          .where(eq(blogPosts.status, "published")),
      ]);

      for (const trail of publishedTrails) {
        dynamicEntries.push(
          urlEntry(
            `${BASE_URL}/trilha/${trail.id}`,
            toW3CDate(trail.updatedAt),
            "weekly",
            "0.9"
          )
        );
      }

      for (const post of publishedPosts) {
        dynamicEntries.push(
          urlEntry(
            `${BASE_URL}/blog/${post.slug}`,
            toW3CDate(post.updatedAt),
            "monthly",
            "0.7"
          )
        );
      }
    }
  } catch (err) {
    console.error("[sitemap] DB error:", err);
    // Serve static-only sitemap rather than failing entirely
  }

  const xml = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="https://www.sitemaps.org/schemas/sitemap/0.9">',
    ...staticRoutes,
    ...dynamicEntries,
    "</urlset>",
  ].join("\n");

  res.setHeader("Content-Type", "application/xml; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=3600");
  res.status(200).send(xml);
});

export const sitemapRouter = router;
