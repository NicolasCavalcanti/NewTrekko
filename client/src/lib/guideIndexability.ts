const MIN_BIO_CHARS = 80;

export interface GuideIndexabilityInput {
  name: string | null;
  bio: string | null;
  photoUrl: string | null;
  isVerified: boolean;
  uf: string | null;
  categories: string[] | null;
  segments: string[] | null;
}

export interface IndexabilityResult {
  shouldIndex: boolean;
  robotsContent: "index, follow" | "noindex, nofollow";
}

/**
 * Evaluates whether a /guia/:id page should be indexed by search engines.
 *
 * Hard requirements (fail = noindex immediately):
 *   - guide.name is present
 *   - guide.uf  is present
 *
 * Depth signal (at least one required to pass):
 *   - bio with ≥ 80 characters  — editorial content authored by the guide
 *   - isVerified               — guide is active on the Trekko platform
 *   - expeditionCount ≥ 1      — guide has an active commercial presence
 *
 * In static/GitHub-Pages mode bio is always null, so only isVerified
 * guides pass. Non-verified CADASTUR-scraped entries receive noindex.
 */
export function evaluateGuideIndexability(
  guide: GuideIndexabilityInput,
  expeditionCount: number,
): IndexabilityResult {
  const hasName = Boolean(guide.name?.trim());
  const hasState = Boolean(guide.uf);

  if (!hasName || !hasState) {
    return { shouldIndex: false, robotsContent: "noindex, nofollow" };
  }

  const hasEditorialContent = (guide.bio?.trim().length ?? 0) >= MIN_BIO_CHARS;
  const hasPlatformPresence = guide.isVerified;
  const hasActiveExpeditions = expeditionCount >= 1;

  const shouldIndex =
    hasEditorialContent || hasPlatformPresence || hasActiveExpeditions;

  return {
    shouldIndex,
    robotsContent: shouldIndex ? "index, follow" : "noindex, nofollow",
  };
}
