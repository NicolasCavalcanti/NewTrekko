/**
 * CDN URL helpers
 *
 * When CDN_ORIGIN is set (e.g. "https://cdn.trekko.com.br"), image keys are
 * served through CloudFront instead of the Manus storage proxy.  This gives
 * cached, geo-distributed delivery and WebP content negotiation at the edge.
 *
 * Without CDN_ORIGIN the original storage proxy URL is returned unchanged,
 * so the application works in local / staging environments without extra config.
 */

import { ENV } from "../_core/env";

/**
 * Convert a storage key (relative path, e.g. "trails/123/hero.jpg") into a
 * CDN-served URL.  Falls back to the raw proxy URL when no CDN is configured.
 *
 * @param key       Storage key returned by `storagePut` (no leading slash).
 * @param fallback  Original proxy URL to return when CDN is not configured.
 */
export function cdnUrl(key: string, fallback: string): string {
  const origin = ENV.cdnOrigin;
  if (!origin) return fallback;
  const cleanKey = key.replace(/^\/+/, "");
  const cleanOrigin = origin.replace(/\/+$/, "");
  return `${cleanOrigin}/${cleanKey}`;
}

/**
 * Rewrite an already-stored proxy URL to the CDN equivalent.
 * Used by the migration script and for URLs that pre-date CDN setup.
 *
 * The proxy URL is expected to contain the storage key as its `path` query
 * param (e.g. `…/v1/storage/downloadUrl?path=trails/123/hero.jpg`).
 * We extract the path and build the CDN URL from it.
 *
 * If the URL is already a CDN URL, or if CDN_ORIGIN is not set, it is
 * returned unchanged.
 */
export function rewriteToCdn(storedUrl: string): string {
  const origin = ENV.cdnOrigin;
  if (!origin) return storedUrl;

  // Already a CDN URL — nothing to do
  if (storedUrl.startsWith(origin)) return storedUrl;

  try {
    const parsed = new URL(storedUrl);

    // Proxy download URL: extract `path` query param
    const pathParam = parsed.searchParams.get("path");
    if (pathParam) {
      return cdnUrl(pathParam, storedUrl);
    }

    // Direct S3 or other URL: use the pathname as the key
    const key = parsed.pathname.replace(/^\/+/, "");
    if (key) {
      return cdnUrl(key, storedUrl);
    }
  } catch {
    // Not a valid URL — return as-is
  }

  return storedUrl;
}
