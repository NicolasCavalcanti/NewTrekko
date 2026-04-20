import "dotenv/config";
import express, { Request, Response } from "express";
import { createServer } from "http";
import net from "net";
import { createExpressMiddleware } from "@trpc/server/adapters/express";
import { registerOAuthRoutes } from "./oauth";
import mercadopagoWebhook from "../webhooks/mercadopago";
import { offlineMapRouter } from "../routes/offline-map";
import { sitemapRouter } from "../routes/sitemap";
import { financialInfoRouter } from "../routes/financial-info";
import { appRouter } from "../routers";
import { createContext } from "./context";
import { serveStatic, setupVite } from "./vite";
import { getDb, getRawPool, getNearbyTrails } from "../db";
import { viewCounter } from "../lib/viewCounter";

function isPortAvailable(port: number): Promise<boolean> {
  return new Promise(resolve => {
    const server = net.createServer();
    server.listen(port, () => {
      server.close(() => resolve(true));
    });
    server.on("error", () => resolve(false));
  });
}

async function findAvailablePort(startPort: number = 3000): Promise<number> {
  for (let port = startPort; port < startPort + 20; port++) {
    if (await isPortAvailable(port)) {
      return port;
    }
  }
  throw new Error(`No available port found starting from ${startPort}`);
}

async function startServer() {
  const app = express();
  const server = createServer(app);

  // CORS — allow the GitHub Pages frontend and production domain to call the API
  const allowedOrigins = new Set([
    "https://nicolascavalcanti.github.io",
    "https://trekko.com.br",
    "https://www.trekko.com.br",
    "http://localhost:3000",
    "http://localhost:5173",
    ...(process.env.CORS_ORIGINS ?? "")
      .split(",")
      .map((o) => o.trim())
      .filter(Boolean),
  ]);

  app.use((req, res, next) => {
    const origin = req.headers.origin;
    if (origin && allowedOrigins.has(origin)) {
      res.setHeader("Access-Control-Allow-Origin", origin);
      res.setHeader("Access-Control-Allow-Credentials", "true");
      res.setHeader("Access-Control-Allow-Methods", "GET, POST, PATCH, OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type");
      res.setHeader("Access-Control-Max-Age", "86400");
    }
    if (req.method === "OPTIONS") {
      res.sendStatus(204);
      return;
    }
    next();
  });

  // Configure body parser with larger size limit for file uploads
  app.use(express.json({ limit: "50mb" }));
  app.use(express.urlencoded({ limit: "50mb", extended: true }));

  // DB-PERF-06: Health check endpoint — required for Railway/Render liveness probes.
  // Returns 200 when the DB pool is reachable, 503 otherwise.
  app.get("/health", async (_req: Request, res: Response) => {
    try {
      const pool = getRawPool();
      if (!pool) {
        return res.status(503).json({ status: "error", db: "pool not initialised" });
      }
      await pool.query("SELECT 1");
      return res.json({ status: "ok", db: "connected" });
    } catch (err) {
      return res.status(503).json({ status: "error", db: "unreachable" });
    }
  });

  // DB-ARCH-02: Nearby trails API — GET /api/trilhas/nearby?lat=X&lng=Y&radiusKm=50
  app.get("/api/trilhas/nearby", async (req: Request, res: Response) => {
    const lat = parseFloat(req.query.lat as string);
    const lng = parseFloat(req.query.lng as string);
    const radiusKm = parseFloat(req.query.radiusKm as string) || 50;
    if (isNaN(lat) || isNaN(lng)) {
      return res.status(400).json({ error: "lat and lng query parameters are required" });
    }
    try {
      const nearby = await getNearbyTrails(lat, lng, radiusKm);
      return res.json({ trails: nearby });
    } catch (err) {
      return res.status(500).json({ error: "Failed to query nearby trails" });
    }
  });

  // Mercado Pago webhook
  app.use('/api/webhooks/mercadopago', mercadopagoWebhook);

  // Sitemap
  app.use(sitemapRouter);

  // Financial info REST API (Stories 14 & 15)
  app.use('/api/financial-info', financialInfoRouter);

  // Offline map download route
  app.use('/api/trilhas', offlineMapRouter);

  // OAuth callback under /api/oauth/callback
  registerOAuthRoutes(app);
  // tRPC API
  app.use(
    "/api/trpc",
    createExpressMiddleware({
      router: appRouter,
      createContext,
    })
  );
  // development mode uses Vite, production mode uses static files
  if (process.env.NODE_ENV === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }

  const preferredPort = parseInt(process.env.PORT || "3000");
  const port = await findAvailablePort(preferredPort);

  if (port !== preferredPort) {
    console.log(`Port ${preferredPort} is busy, using port ${port} instead`);
  }

  server.listen(port, () => {
    console.log(`Server running on http://localhost:${port}/`);
    // DB-PERF-05: Start the buffered view-count flush loop.
    // Flushes every 5 min; also registers SIGTERM handler to flush before exit.
    viewCounter.start(getDb);
  });
}

startServer().catch(console.error);
