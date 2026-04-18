import { useEffect } from "react";
import { useLocation } from "wouter";

const ADSENSE_CLIENT = "ca-pub-2482023752745520";
const ADSENSE_SRC = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT}`;
const SCRIPT_ID = "adsense-script";

/**
 * Whitelist of route patterns where AdSense is permitted.
 * Only pages that contain <AdUnit /> placements AND have substantial
 * editorial content should be listed here.
 *
 * Allowed:  /trilha/:id   — Trail detail pages
 *           /blog/:slug   — Blog post pages
 *
 * Everything else (home, lists, legal, contact, etc.) is blocked by default.
 */
const ALLOWED_PATTERNS: RegExp[] = [
  /^\/trilha\/[^/]+/,
  /^\/blog\/[^/]+/,
];

function isAllowed(path: string): boolean {
  return ALLOWED_PATTERNS.some((pattern) => pattern.test(path));
}

/**
 * Manages the Google AdSense script lifecycle based on the current route.
 * Uses a whitelist strategy: the script is injected only on editorial content
 * pages (/trilha/:id, /blog/:slug) and removed from every other route.
 *
 * Place this component once inside the Wouter Router context.
 */
export function AdSenseLoader() {
  const [location] = useLocation();

  useEffect(() => {
    const allowed = isAllowed(location);
    const existing = document.getElementById(SCRIPT_ID);

    if (!allowed) {
      if (existing) existing.remove();
      return;
    }

    // Already injected — nothing to do
    if (existing) return;

    const script = document.createElement("script");
    script.id = SCRIPT_ID;
    script.async = true;
    script.src = ADSENSE_SRC;
    script.crossOrigin = "anonymous";
    document.head.appendChild(script);
  }, [location]);

  return null;
}
