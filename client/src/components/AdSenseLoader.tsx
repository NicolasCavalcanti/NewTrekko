import { useEffect } from "react";
import { useLocation } from "wouter";
import { useAdReadiness } from "@/contexts/AdReadinessContext";
import { isMonetizable } from "@/config/monetization";

const ADSENSE_CLIENT = "ca-pub-2482023752745520";
const ADSENSE_SRC = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT}`;
const SCRIPT_ID = "adsense-script";

/**
 * Manages the Google AdSense script lifecycle.
 *
 * Injects the script only when two conditions are simultaneously true:
 *   1. isMonetizable(location) === true  (route policy, from monetization.ts)
 *   2. readyForLocation === location     (content is in the DOM, from AdUnit)
 *
 * On every route change the script is removed so each page starts clean.
 * Place once inside the Wouter Router + AdReadinessProvider.
 */
export function AdSenseLoader() {
  const [location] = useLocation();
  const { readyForLocation } = useAdReadiness();

  useEffect(() => {
    const existing = document.getElementById(SCRIPT_ID);
    if (existing) existing.remove();
  }, [location]);

  useEffect(() => {
    if (!isMonetizable(location) || readyForLocation !== location) return;
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
