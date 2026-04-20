import { useEffect } from "react";
import { useLocation } from "wouter";
import { useAdReadiness } from "@/contexts/AdReadinessContext";

const ADSENSE_CLIENT = "ca-pub-2482023752745520";

/**
 * AdSense ad unit slot IDs.
 * Replace the placeholder values with the numeric IDs from your AdSense account:
 *   https://adsense.google.com → Ads → By ad unit → Create new ad unit
 */
export const AD_SLOTS = {
  /** Trail detail page — after the intro paragraph */
  TRAIL_AFTER_INTRO: "3721854690",
  /** Trail detail page — between logistics sections and photo gallery */
  TRAIL_BEFORE_GALLERY: "6534128907",
  /** Blog post page — after the first two paragraphs */
  BLOG_MID_ARTICLE: "8145037926",
  /** Blog post page — end of article, before tags */
  BLOG_END_ARTICLE: "2907631548",
  /** Guides page — between editorial sections and the guide directory */
  GUIDES_AFTER_EDITORIAL: "5038274619",
} as const;

interface AdUnitProps {
  /** AdSense ad unit slot ID (numeric string from the AdSense dashboard) */
  slot: string;
  className?: string;
}

/**
 * Renders a single responsive AdSense display ad unit.
 *
 * On mount (which only happens after the page's data has loaded and content
 * is in the DOM), this component:
 *   1. Calls markContentReady(location) — triggers AdSenseLoader to inject
 *      the adsbygoogle script now that real content exists on the page.
 *   2. Calls adsbygoogle.push({}) — queued in the array buffer and processed
 *      by the script once it loads, filling this <ins> element.
 *
 * The effect re-runs on location change so that navigating between content
 * pages (e.g. /blog/post-1 → /blog/post-2) correctly re-signals readiness
 * and re-queues the push for the new <ins> element.
 */
export function AdUnit({ slot, className }: AdUnitProps) {
  const [location] = useLocation();
  const { markContentReady } = useAdReadiness();

  useEffect(() => {
    markContentReady(location);
    try {
      ((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({});
    } catch {
      // AdSense script not yet loaded — push is buffered and processed on load
    }
  }, [location, markContentReady]);

  return (
    <div
      className={`w-full overflow-hidden ${className ?? ""}`}
      style={{ minHeight: 100 }}
      aria-label="Anúncio"
    >
      <ins
        className="adsbygoogle"
        style={{ display: "block" }}
        data-ad-client={ADSENSE_CLIENT}
        data-ad-slot={slot}
        data-ad-format="auto"
        data-full-width-responsive="true"
      />
    </div>
  );
}
