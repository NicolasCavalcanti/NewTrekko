/**
 * Server-side rendering (SSR) handler for SEO-critical pages.
 *
 * Supported routes:
 *   /trilha/:id   — Trail detail
 *   /blog/:slug   — Blog post
 *   /guia/:id     — Guide detail (cadasturNumber)
 *
 * For each route we:
 *   1. Call tRPC procedures server-side (no HTTP round-trip)
 *   2. Pre-populate a React Query client with the fetched data
 *   3. Render the matching page component to an HTML string
 *   4. Inject the rendered HTML + dehydrated state into the index.html template
 */

import type { ViteDevServer } from "vite";
import type { Express, Request, Response } from "express";
import fs from "fs";
import path from "path";
import superjson from "superjson";
import { appRouter } from "../routers";
import { createCallerFactory } from "../_core/trpc";
import type { TrpcContext } from "../_core/context";

const createCaller = createCallerFactory(appRouter);

// tRPC v11 query key format: [["procedure", "name"], { input: {...}, type: "query" }]
function trpcKey(pathParts: string[], input: unknown): unknown[] {
  return [pathParts, { input, type: "query" }];
}

// Build a minimal context for SSR callers (unauthenticated public access)
function ssrContext(req: Request, res: Response): TrpcContext {
  return { req: req as any, res: res as any, user: null };
}

type HelmetContext = {
  helmet?: {
    title?: { toString(): string };
    meta?: { toString(): string };
    link?: { toString(): string };
    script?: { toString(): string };
    style?: { toString(): string };
  };
};

interface RenderResult {
  html: string;
  helmetContext: HelmetContext;
  dehydratedState: unknown;
}

interface RenderModule {
  render: (url: string, preloadedState?: unknown) => Promise<RenderResult>;
}

async function loadRenderModule(vite?: ViteDevServer): Promise<RenderModule> {
  if (vite) {
    // Dev mode: load via Vite's SSR module system so aliases & TS work
    return vite.ssrLoadModule("/src/entry-server.tsx") as Promise<RenderModule>;
  }
  // Prod mode: load the pre-built SSR bundle
  const ssrPath = path.resolve(
    path.dirname(new URL(import.meta.url).pathname),
    "..",
    "server",
    "entry-server.js"
  );
  return import(ssrPath) as Promise<RenderModule>;
}

function injectSSR(
  template: string,
  renderedHtml: string,
  helmetContext: HelmetContext,
  dehydratedState: unknown
): string {
  // Build head tags from helmet
  const { helmet } = helmetContext;
  const headTags = helmet
    ? [
        helmet.title?.toString() ?? "",
        helmet.meta?.toString() ?? "",
        helmet.link?.toString() ?? "",
        helmet.style?.toString() ?? "",
        helmet.script?.toString() ?? "",
      ]
        .filter(Boolean)
        .join("\n    ")
    : "";

  // Serialize dehydrated state — superjson handles Date, BigInt, etc.
  const stateScript = `<script>window.__DEHYDRATED_STATE__ = ${JSON.stringify(
    superjson.serialize(dehydratedState)
  )};</script>`;

  return template
    .replace(/<title>[^<]*<\/title>/, "") // remove default title (helmet will set it)
    .replace("</head>", `    ${headTags}\n    ${stateScript}\n</head>`)
    .replace('<div id="root"></div>', `<div id="root">${renderedHtml}</div>`);
}

const SSR_PATTERNS = [
  /^\/trilha\/\d+$/,
  /^\/blog\/[^/]+$/,
  /^\/guia\/[^/]+$/,
];

export function registerSSRRoutes(app: Express, vite?: ViteDevServer) {
  app.get("*", async (req: Request, res: Response, next) => {
    const url = req.path;
    const isSSR = SSR_PATTERNS.some((p) => p.test(url));
    if (!isSSR) return next();

    try {
      // ── 1. Fetch data server-side via tRPC caller ────────────────────────
      const caller = createCaller(ssrContext(req, res));
      type QueryEntry = {
        queryKey: unknown[];
        queryHash: string;
        state: { data: unknown; status: string; dataUpdatedAt: number };
      };
      const queries: QueryEntry[] = [];

      const trailMatch = url.match(/^\/trilha\/(\d+)$/);
      const blogMatch = url.match(/^\/blog\/([^/]+)$/);
      const guideMatch = url.match(/^\/guia\/([^/]+)$/);

      if (trailMatch) {
        const id = parseInt(trailMatch[1], 10);
        try {
          const data = await caller.trails.getById({ id });
          const key = trpcKey(["trails", "getById"], { id });
          queries.push({
            queryKey: key,
            queryHash: JSON.stringify(key),
            state: { data, status: "success", dataUpdatedAt: Date.now() },
          });
        } catch {
          // Not found — let the page render the error state client-side
        }
      }

      if (blogMatch) {
        const slug = decodeURIComponent(blogMatch[1]);
        try {
          const data = await caller.blog.getBySlug({ slug });
          const key = trpcKey(["blog", "getBySlug"], { slug });
          queries.push({
            queryKey: key,
            queryHash: JSON.stringify(key),
            state: { data, status: "success", dataUpdatedAt: Date.now() },
          });
        } catch {
          // Not found
        }
      }

      if (guideMatch) {
        const cadasturNumber = decodeURIComponent(guideMatch[1]);
        try {
          const data = await caller.guides.getById({ cadasturNumber });
          const key = trpcKey(["guides", "getById"], { cadasturNumber });
          queries.push({
            queryKey: key,
            queryHash: JSON.stringify(key),
            state: { data, status: "success", dataUpdatedAt: Date.now() },
          });
        } catch {
          // Not found
        }
      }

      const ssrDehydratedState = { queries, mutations: [] };

      // ── 2. Render React to HTML ──────────────────────────────────────────
      const renderModule = await loadRenderModule(vite);
      const { html: renderedHtml, helmetContext, dehydratedState } =
        await renderModule.render(url, ssrDehydratedState);

      // ── 3. Load index.html template ──────────────────────────────────────
      let template: string;
      if (vite) {
        const templatePath = path.resolve(process.cwd(), "client", "index.html");
        template = await fs.promises.readFile(templatePath, "utf-8");
        template = await vite.transformIndexHtml(url, template);
      } else {
        const distPath = path.resolve(
          path.dirname(new URL(import.meta.url).pathname),
          "..",
          "public",
          "index.html"
        );
        template = await fs.promises.readFile(distPath, "utf-8");
      }

      const finalHtml = injectSSR(template, renderedHtml, helmetContext, dehydratedState);

      res.status(200).set({ "Content-Type": "text/html" }).end(finalHtml);
    } catch (err) {
      if (vite) {
        vite.ssrFixStacktrace(err as Error);
      }
      console.error("[SSR Error]", err);
      next(err);
    }
  });
}
