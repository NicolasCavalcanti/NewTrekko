import { useEffect, useRef } from "react";

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
} as const;

interface AdUnitProps {
  /** AdSense ad unit slot ID (numeric string from the AdSense dashboard) */
  slot: string;
  className?: string;
}

/**
 * Renders a single responsive AdSense display ad unit.
 *
 * - Uses data-ad-format="auto" + data-full-width-responsive="true" for responsiveness
 * - Wraps in a min-height container to prevent Cumulative Layout Shift (CLS)
 * - Guards adsbygoogle.push() so it silently no-ops when the AdSense script is
 *   absent (blocked routes, ad blockers, or SSR)
 */
export function AdUnit({ slot, className }: AdUnitProps) {
  const pushed = useRef(false);

  useEffect(() => {
    if (pushed.current) return;
    pushed.current = true;
    try {
      ((window as any).adsbygoogle = (window as any).adsbygoogle || []).push({});
    } catch {
      // AdSense script not loaded (blocked route, ad blocker, etc.)
    }
  }, []);

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
