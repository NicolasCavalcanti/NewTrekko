import { useEffect } from "react";
import { useLocation } from "wouter";
import { useAdReadiness } from "@/contexts/AdReadinessContext";

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
 * Manages the Google AdSense script lifecycle based on both the current route
 * and content readiness. The script is injected only when two conditions are
 * simultaneously true:
 *   1. The route is in the whitelist (editorial content page)
 *   2. An <AdUnit> on that route has mounted and called markContentReady(),
 *      confirming that real editorial content is in the DOM
 *
 * On every route change the script is removed, resetting the cycle so that
 * the new page starts clean regardless of what the previous page did.
 *
 * Place this component once inside the Wouter Router + AdReadinessProvider.
 */
export function AdSenseLoader() {
  const [location] = useLocation();
  const { readyForLocation } = useAdReadiness();

  // Remove the script on every route change so each page starts from scratch
  useEffect(() => {
    const existing = document.getElementById(SCRIPT_ID);
    if (existing) existing.remove();
  }, [location]);

  // Inject only when the whitelisted route's content is confirmed in the DOM
  useEffect(() => {
    if (!isAllowed(location) || readyForLocation !== location) return;
    if (document.getElementById(SCRIPT_ID)) return;

    const script = document.createElement("script");
    script.id = SCRIPT_ID;
    script.async = true;
    script.src = ADSENSE_SRC;
    script.crossOrigin = "anonymous";
    document.head.appendChild(script);
  }, [location, readyForLocation]);

  return null;
}
