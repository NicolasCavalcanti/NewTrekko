/**
 * Expedition content quality scoring for SEO indexation decisions.
 *
 * A "weak" page — noindex — has little editorial value beyond price/date.
 * A "strong" page — index — has a proper description, meeting point, and
 * at least one additional piece of content (guide notes or included items).
 */

export type ExpeditionForQuality = {
  status: string;
  startDate: string;
  description?: string | null;
  meetingPoint?: string | null;
  guideNotes?: string | null;
  includedItems?: string | null;
  title?: string | null;
};

export type QualityResult = {
  shouldIndex: boolean;
  missingFields: string[];
  score: number; // 0-5
};

const MIN_DESCRIPTION_LENGTH = 80;
const STALE_CLOSED_DAYS = 90;

/**
 * Returns whether an expedition page has sufficient editorial content to be
 * indexed by search engines, and a list of missing fields for guide-facing UI.
 */
export function evaluateExpeditionQuality(
  expedition: ExpeditionForQuality
): QualityResult {
  const missing: string[] = [];
  let score = 0;

  // ── Status gate ──────────────────────────────────────────────────────────────
  const indexableStatuses = new Set(["active", "full"]);
  if (!indexableStatuses.has(expedition.status)) {
    // Closed expeditions < 90 days old still have informational value
    if (expedition.status === "closed" || expedition.status === "completed") {
      const daysSince =
        (Date.now() - new Date(expedition.startDate).getTime()) /
        (1000 * 60 * 60 * 24);
      if (daysSince > STALE_CLOSED_DAYS) {
        return { shouldIndex: false, missingFields: [], score: 0 };
      }
    } else {
      // draft / cancelled → always noindex
      return { shouldIndex: false, missingFields: [], score: 0 };
    }
  }

  // ── Content checks ───────────────────────────────────────────────────────────
  // 1. Title (custom or will fall back to trail name — both are fine)
  score += 1;

  // 2. Description with editorial depth
  const desc = expedition.description?.trim() ?? "";
  if (desc.length >= MIN_DESCRIPTION_LENGTH) {
    score += 1;
  } else {
    missing.push(
      desc.length === 0
        ? "Descrição da expedição (mínimo 80 caracteres)"
        : `Descrição muito curta (${desc.length} de ${MIN_DESCRIPTION_LENGTH} caracteres mínimos)`
    );
  }

  // 3. Meeting point
  if (expedition.meetingPoint?.trim()) {
    score += 1;
  } else {
    missing.push("Ponto de encontro");
  }

  // 4. Guide notes OR included items
  const hasNotes = Boolean(expedition.guideNotes?.trim());
  const hasItems = Boolean(expedition.includedItems?.trim());
  if (hasNotes || hasItems) {
    score += 1;
  } else {
    missing.push("Observações do guia ou itens inclusos");
  }

  // 5. Future-dated (within 365 days) — still time to book
  const daysUntil =
    (new Date(expedition.startDate).getTime() - Date.now()) /
    (1000 * 60 * 60 * 24);
  if (daysUntil > -1) {
    score += 1;
  }

  // Index only when score is 4 or 5 (description + meeting point + notes/items)
  const shouldIndex = score >= 4 && missing.length === 0;

  return { shouldIndex, missingFields: missing, score };
}
