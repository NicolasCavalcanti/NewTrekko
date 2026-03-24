import { useEffect } from "react";
import { useLocation } from "wouter";

const ADSENSE_CLIENT = "ca-pub-2482023752745520";
const ADSENSE_SRC = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_CLIENT}`;
const SCRIPT_ID = "adsense-script";

/**
 * Routes on which AdSense must NOT be loaded.
 * Prefix-matched: /perfil also blocks /perfil/settings, etc.
 */
const BLOCKED_PREFIXES = [
  "/checkout",
  "/perfil",
  "/reservas",
  "/admin",
  "/login",
];

function isBlocked(path: string): boolean {
  return BLOCKED_PREFIXES.some(
    (prefix) => path === prefix || path.startsWith(prefix + "/")
  );
}

/**
 * Dynamically injects or removes the Google AdSense script based on the
 * current wouter route.  Place this component once inside the app tree
 * (inside the wouter Router context) and it will manage itself automatically.
 *
 * Allowed:  /, /trilhas, /trilha/:id, /guias, /guia/:id, /blog, /blog/:slug
 * Blocked:  /checkout, /perfil, /reservas, /admin, /login
 */
export function AdSenseLoader() {
  const [location] = useLocation();

  useEffect(() => {
    const blocked = isBlocked(location);
    const existing = document.getElementById(SCRIPT_ID);

    if (blocked) {
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
