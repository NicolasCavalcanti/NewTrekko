/**
 * Monetization policy — single source of truth for AdSense governance.
 *
 * Every route in the app is explicitly assigned a tier:
 *
 *   full        — deep editorial content; always eligible for ads
 *   none        — legal, navigational, functional or authenticated pages
 *   conditional — could become eligible when specific content criteria are met
 *
 * Any route NOT listed here defaults to "none" (safe by default).
 * To monetize a new page, add it here with tier "full" and a rationale.
 */

export type MonetizationTier = "full" | "none" | "conditional";

interface RoutePolicy {
  pattern: RegExp;
  tier: MonetizationTier;
  /** Why this tier was assigned — required for audit trail and governance. */
  rationale: string;
}

export const ROUTE_POLICIES: RoutePolicy[] = [
  // ── FULL: deep editorial content ──────────────────────────────────────────
  {
    pattern: /^\/trilha\/[^/]+/,
    tier: "full",
    rationale:
      "Trail detail: long-form editorial content with description, logistics, " +
      "gallery and reviews. Meets AdSense depth and value criteria.",
  },
  {
    pattern: /^\/blog\/[^/]+/,
    tier: "full",
    rationale:
      "Blog article: structured long-form editorial content written by the " +
      "Trekko team. Meets AdSense depth and value criteria.",
  },

  // ── NONE: navigational ────────────────────────────────────────────────────
  {
    pattern: /^\/$/,
    tier: "none",
    rationale: "Home page: navigational hub, not deep editorial content.",
  },
  {
    pattern: /^\/trilhas/,
    tier: "none",
    rationale: "Trail listing: paginated index page, no per-page editorial depth.",
  },
  {
    pattern: /^\/blog$/,
    tier: "none",
    rationale: "Blog listing: index page, no editorial content of its own.",
  },
  {
    pattern: /^\/guias/,
    tier: "none",
    rationale: "Guide listing: navigational, programmatic index.",
  },
  {
    pattern: /^\/guia\/[^/]+/,
    tier: "none",
    rationale: "Guide profile: structured data page, not original editorial content.",
  },

  // ── NONE: institutional ───────────────────────────────────────────────────
  {
    pattern: /^\/sobre/,
    tier: "none",
    rationale: "About page: institutional, not editorial.",
  },
  {
    pattern: /^\/contato/,
    tier: "none",
    rationale: "Contact page: functional form, zero editorial content.",
  },
  {
    pattern: /^\/termos/,
    tier: "none",
    rationale: "Terms of service: legal page — ads prohibited by AdSense policy.",
  },
  {
    pattern: /^\/privacidade/,
    tier: "none",
    rationale: "Privacy policy: legal page — ads prohibited by AdSense policy.",
  },
  {
    pattern: /^\/politica-editorial/,
    tier: "none",
    rationale: "Editorial policy: institutional, not audience-facing content.",
  },

  // ── NONE: authenticated / transactional ──────────────────────────────────
  {
    pattern: /^\/perfil/,
    tier: "none",
    rationale: "User profile: authenticated area, personalised data — not editorial.",
  },
  {
    pattern: /^\/admin/,
    tier: "none",
    rationale: "Admin area: internal tool, not a public page.",
  },
  {
    pattern: /^\/reservas/,
    tier: "none",
    rationale: "Reservations: authenticated transactional flow.",
  },
  {
    pattern: /^\/checkout/,
    tier: "none",
    rationale: "Checkout: transactional page — ads create friction and policy risk.",
  },

  // ── CONDITIONAL: eligible once content depth criteria are met ─────────────
  {
    pattern: /^\/expedicao\/[^/]+/,
    tier: "conditional",
    rationale:
      "Expedition detail: promote to \"full\" when pages consistently contain " +
      ">500 words of original editorial content and an author attribution.",
  },
];

/** Tier assigned to any route not explicitly listed above. */
const DEFAULT_TIER: MonetizationTier = "none";

/** Returns the monetization tier for a given path. */
export function getRouteTier(path: string): MonetizationTier {
  return (
    ROUTE_POLICIES.find((entry) => entry.pattern.test(path))?.tier ??
    DEFAULT_TIER
  );
}

/**
 * Returns true only for routes with tier "full".
 * This is the gate used by AdSenseLoader before injecting the script.
 */
export function isMonetizable(path: string): boolean {
  return getRouteTier(path) === "full";
}
