-- ============================================================
-- Migration 0014 — Editorial Template High Value (Story 3.3)
-- Adds fields to blog_posts to support high-value article standard:
--   authorSlug       — links article to author profile page
--   isHighValue      — flags articles that follow the full template
--   reviewedAt       — date of last editorial review/update
--   reviewerName     — name of the editor/expert who reviewed
--   faqData          — JSON array of {question, answer} for FAQ section
-- ============================================================

ALTER TABLE `blog_posts`
  ADD COLUMN IF NOT EXISTS `authorSlug`    VARCHAR(128)   NULL         AFTER `authorName`,
  ADD COLUMN IF NOT EXISTS `isHighValue`   TINYINT(1)     NOT NULL DEFAULT 0 AFTER `publishedAt`,
  ADD COLUMN IF NOT EXISTS `reviewedAt`    TIMESTAMP      NULL         AFTER `isHighValue`,
  ADD COLUMN IF NOT EXISTS `reviewerName`  VARCHAR(128)   NULL         AFTER `reviewedAt`,
  ADD COLUMN IF NOT EXISTS `faqData`       JSON           NULL         AFTER `reviewerName`;

CREATE INDEX IF NOT EXISTS `idx_blog_high_value` ON `blog_posts` (`isHighValue`);
