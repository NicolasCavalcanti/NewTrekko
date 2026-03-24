import express, { type Express } from "express";
import fs from "fs";
import { type Server } from "http";
import { nanoid } from "nanoid";
import path from "path";
import { createServer as createViteServer } from "vite";
import viteConfig from "../../vite.config";
import { registerSSRRoutes } from "../routes/ssr";

const ROBOTS_CONTENT = `User-agent: *
Disallow: /perfil
Disallow: /checkout
Disallow: /reservas
Disallow: /admin
Disallow: /api/

Sitemap: https://trekko.com.br/sitemap.xml
`;

export async function setupVite(app: Express, server: Server) {
  const serverOptions = {
    middlewareMode: true,
    hmr: { server },
    allowedHosts: true as const,
  };

  const vite = await createViteServer({
    ...viteConfig,
    configFile: false,
    server: serverOptions,
    appType: "custom",
  });

  // Serve ads.txt with correct Content-Type header for Google AdSense (development mode)
  const publicPath = path.resolve(import.meta.dirname, "../..", "client", "public");
  app.get('/ads.txt', (_req, res) => {
    const adsPath = path.resolve(publicPath, 'ads.txt');
    if (fs.existsSync(adsPath)) {
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.sendFile(adsPath);
    } else {
      // Fallback: serve the content directly
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.send('google.com, pub-2482023752745520, DIRECT, f08c47fec0942fa0\n');
    }
  });

  // Serve robots.txt (development mode)
  app.get('/robots.txt', (_req, res) => {
    const robotsPath = path.resolve(publicPath, 'robots.txt');
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=86400');
    if (fs.existsSync(robotsPath)) {
      res.sendFile(robotsPath);
    } else {
      res.send(ROBOTS_CONTENT);
    }
  });

  app.use(vite.middlewares);

  // SSR for SEO-critical pages (trail, blog, guide detail)
  registerSSRRoutes(app, vite);

  app.use("*", async (req, res, next) => {
    const url = req.originalUrl;

    try {
      const clientTemplate = path.resolve(
        import.meta.dirname,
        "../..",
        "client",
        "index.html"
      );

      // always reload the index.html file from disk incase it changes
      let template = await fs.promises.readFile(clientTemplate, "utf-8");
      template = template.replace(
        `src="/src/main.tsx"`,
        `src="/src/main.tsx?v=${nanoid()}"`
      );
      const page = await vite.transformIndexHtml(url, template);
      res.status(200).set({ "Content-Type": "text/html" }).end(page);
    } catch (e) {
      vite.ssrFixStacktrace(e as Error);
      next(e);
    }
  });
}

export function serveStatic(app: Express) {
  const distPath =
    process.env.NODE_ENV === "development"
      ? path.resolve(import.meta.dirname, "../..", "dist", "public")
      : path.resolve(import.meta.dirname, "public");
  if (!fs.existsSync(distPath)) {
    console.error(
      `Could not find the build directory: ${distPath}, make sure to build the client first`
    );
  }

  // Serve ads.txt with correct Content-Type header for Google AdSense
  app.get('/ads.txt', (_req, res) => {
    const adsPath = path.resolve(distPath, 'ads.txt');
    if (fs.existsSync(adsPath)) {
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.sendFile(adsPath);
    } else {
      // Fallback: serve the content directly
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.setHeader('Cache-Control', 'public, max-age=86400');
      res.send('google.com, pub-2482023752745520, DIRECT, f08c47fec0942fa0\n');
    }
  });

  // Serve robots.txt
  app.get('/robots.txt', (_req, res) => {
    const robotsPath = path.resolve(distPath, 'robots.txt');
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.setHeader('Cache-Control', 'public, max-age=86400');
    if (fs.existsSync(robotsPath)) {
      res.sendFile(robotsPath);
    } else {
      res.send(ROBOTS_CONTENT);
    }
  });

  app.use(express.static(distPath));

  // SSR for SEO-critical pages (trail, blog, guide detail)
  registerSSRRoutes(app);

  // fall through to index.html if the file doesn't exist
  app.use("*", (_req, res) => {
    res.sendFile(path.resolve(distPath, "index.html"));
  });
}
