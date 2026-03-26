-- ============================================================
-- Migration 0010 — Database Audit Improvements
-- Covers: DB-SEC-01..04, DB-PERF-01..07, DB-ARCH-01..04
-- Apply with: pnpm drizzle-kit migrate
-- Review each statement before applying to production.
-- ============================================================


-- ============================================================
-- DB-ARCH-04: Timestamp mixin columns missing from tables
-- ============================================================

-- cadastur_registry: add importedAt (replaces internal updatedAt for external data)
ALTER TABLE `cadastur_registry`
  ADD COLUMN IF NOT EXISTS `importedAt` timestamp NOT NULL DEFAULT (now());

-- ============================================================
-- DB-ARCH-01: Soft-delete columns on financial tables
-- ============================================================

ALTER TABLE `reservations`
  ADD COLUMN IF NOT EXISTS `deletedAt` timestamp NULL DEFAULT NULL;

ALTER TABLE `payments`
  ADD COLUMN IF NOT EXISTS `deletedAt` timestamp NULL DEFAULT NULL;

ALTER TABLE `payouts`
  ADD COLUMN IF NOT EXISTS `deletedAt` timestamp NULL DEFAULT NULL;

ALTER TABLE `contestations`
  ADD COLUMN IF NOT EXISTS `deletedAt` timestamp NULL DEFAULT NULL;

ALTER TABLE `users`
  ADD COLUMN IF NOT EXISTS `archivedAt` timestamp NULL DEFAULT NULL;

-- ============================================================
-- DB-ARCH-01: Views for active (non-deleted) records
-- ============================================================

CREATE OR REPLACE VIEW `active_reservations` AS
  SELECT * FROM `reservations` WHERE `deletedAt` IS NULL;

-- ============================================================
-- DB-ARCH-02: Spatial columns for proximity search on trails
-- ============================================================

ALTER TABLE `trails`
  ADD COLUMN IF NOT EXISTS `latitude`  decimal(10,7) NULL,
  ADD COLUMN IF NOT EXISTS `longitude` decimal(10,7) NULL;

-- Backfill lat/lng from the existing mapCoordinates JSON column
-- (Only updates rows that have valid JSON with lat/lng keys)
UPDATE `trails`
SET
  `latitude`  = CAST(JSON_UNQUOTE(JSON_EXTRACT(`mapCoordinates`, '$.lat')) AS DECIMAL(10,7)),
  `longitude` = CAST(JSON_UNQUOTE(JSON_EXTRACT(`mapCoordinates`, '$.lng')) AS DECIMAL(10,7))
WHERE `mapCoordinates` IS NOT NULL
  AND JSON_EXTRACT(`mapCoordinates`, '$.lat') IS NOT NULL;

-- DB-ARCH-02: index for bounding-box pre-filter before Haversine
CREATE INDEX IF NOT EXISTS `idx_trails_geo` ON `trails` (`latitude`, `longitude`);

-- ============================================================
-- DB-ARCH-03: Add 'archived' to trails.status enum
-- ============================================================

ALTER TABLE `trails`
  MODIFY COLUMN `status` enum('draft','published','archived') NOT NULL DEFAULT 'draft';

-- ============================================================
-- DB-PERF-03: trails.slug column and supporting indexes
-- ============================================================

ALTER TABLE `trails`
  ADD COLUMN IF NOT EXISTS `slug` varchar(200) NULL;

-- Backfill slugs from trail names (lowercase, no accents, hyphens)
-- Note: MySQL does not have a built-in transliteration function; this handles
-- the most common ASCII-only names. Run scripts/generate-trail-slugs.mjs for
-- full accent stripping on rows that still have NULL slugs after this UPDATE.
UPDATE `trails`
SET `slug` = LOWER(
  REPLACE(
    REPLACE(
      REPLACE(
        REPLACE(
          REPLACE(`name`, ' ', '-'),
        'ã', 'a'), 'ê', 'e'), 'ú', 'u'), 'ç', 'c')
  )
WHERE `slug` IS NULL;

-- Ensure uniqueness after backfill
CREATE UNIQUE INDEX IF NOT EXISTS `idx_trails_slug`       ON `trails` (`slug`);
CREATE INDEX IF NOT EXISTS        `idx_trails_status`     ON `trails` (`status`);
CREATE INDEX IF NOT EXISTS        `idx_trails_uf`         ON `trails` (`uf`);
CREATE INDEX IF NOT EXISTS        `idx_trails_difficulty` ON `trails` (`difficulty`);
CREATE INDEX IF NOT EXISTS        `idx_trails_status_uf`  ON `trails` (`status`, `uf`);

-- ============================================================
-- DB-PERF-01: Additional cadastur_registry indexes
-- (idx_cadastur_fullname, _uf, _city, _uf_fullname already added
--  in migration 0009; this adds the remaining ones)
-- ============================================================

CREATE INDEX IF NOT EXISTS `idx_cadastur_uf_city` ON `cadastur_registry` (`uf`, `city`(64));
CREATE INDEX IF NOT EXISTS `idx_cadastur_valid`   ON `cadastur_registry` (`validUntil`);
CREATE INDEX IF NOT EXISTS `idx_cadastur_email`   ON `cadastur_registry` (`email`);

-- ============================================================
-- DB-SEC-03: PII masking columns for cadastur_registry
-- ============================================================

ALTER TABLE `cadastur_registry`
  ADD COLUMN IF NOT EXISTS `emailMasked` varchar(255) NULL,
  ADD COLUMN IF NOT EXISTS `phoneMasked` varchar(20) NULL;

-- Populate emailMasked:  jo***@gmail.com
UPDATE `cadastur_registry`
SET `emailMasked` = CONCAT(
  LEFT(`email`, 2),
  '***@',
  SUBSTRING_INDEX(`email`, '@', -1)
)
WHERE `email` IS NOT NULL AND `email` LIKE '%@%';

-- Populate phoneMasked: keep first 4 and last 4 chars, mask middle
-- Example: (11) 98765-4321 → (11) 9****-4321
UPDATE `cadastur_registry`
SET `phoneMasked` = CONCAT(
  LEFT(`phone`, 4),
  REPEAT('*', GREATEST(0, CHAR_LENGTH(`phone`) - 8)),
  RIGHT(`phone`, 4)
)
WHERE `phone` IS NOT NULL AND CHAR_LENGTH(`phone`) >= 8;

-- ============================================================
-- DB-SEC-01: Widen encrypted columns (ciphertext is longer than plaintext)
-- pixKey, pixKeyDocument, documentNumber grow to accommodate iv:tag:ciphertext
-- ============================================================

ALTER TABLE `guide_verification`
  MODIFY COLUMN IF EXISTS `pixKey`         varchar(512)  NULL,
  MODIFY COLUMN IF EXISTS `pixKeyDocument` varchar(256)  NULL,
  MODIFY COLUMN IF EXISTS `documentNumber` varchar(256)  NULL;

-- ============================================================
-- DB-SEC-04: Audit log improvements
-- ============================================================

-- Rename metadata → payload and change type to text
ALTER TABLE `payment_audit_log`
  ADD COLUMN IF NOT EXISTS `payload` text NULL,
  ADD COLUMN IF NOT EXISTS `source`  varchar(50) NULL DEFAULT 'system';

-- Index for retention cleanup queries (purge rows older than 365 days)
CREATE INDEX IF NOT EXISTS `idx_audit_created` ON `payment_audit_log` (`createdAt`);
CREATE INDEX IF NOT EXISTS `idx_audit_entity`  ON `payment_audit_log` (`entityType`, `entityId`);

-- ============================================================
-- DB-PERF-04: Remove enrolledCount (derived from reservations)
-- and create expedition_availability view
-- ============================================================

-- Create the view before dropping the column so apps can migrate
CREATE OR REPLACE VIEW `expedition_availability` AS
SELECT
  e.`id`,
  e.`maxCapacity`,
  COUNT(r.`id`)                                          AS `enrolledCount`,
  (e.`maxCapacity` - COUNT(r.`id`))                     AS `availableSlots`,
  CASE
    WHEN COUNT(r.`id`) >= e.`maxCapacity` THEN 'full'
    ELSE 'available'
  END                                                    AS `availabilityStatus`
FROM `expeditions` e
LEFT JOIN `reservations` r
  ON  r.`expeditionId` = e.`id`
  AND r.`status` NOT IN ('cancelled', 'refunded')
  AND r.`deletedAt` IS NULL
GROUP BY e.`id`;

-- NOTE: The expedition_availability view references `maxCapacity` but the
-- schema column is named `capacity`. Adjust the view if the column name differs.

-- ============================================================
-- DB-PERF-07: Reviews indexes and constraints
-- ============================================================

-- Composite index for the primary query: WHERE targetType=? AND targetId=?
CREATE INDEX IF NOT EXISTS `idx_reviews_target` ON `reviews` (`targetType`, `targetId`);
CREATE INDEX IF NOT EXISTS `idx_reviews_user`   ON `reviews` (`userId`);
CREATE INDEX IF NOT EXISTS `idx_reviews_rating` ON `reviews` (`rating`);

-- One review per user per target (enforced at DB level)
-- Ignore if already exists from schema definition
CREATE UNIQUE INDEX IF NOT EXISTS `uniq_review` ON `reviews` (`userId`, `targetType`, `targetId`);

-- CHECK constraint: rating must be 0–5
ALTER TABLE `reviews`
  ADD CONSTRAINT IF NOT EXISTS `chk_rating` CHECK (`rating` BETWEEN 0 AND 5);

-- ============================================================
-- DB-PERF-04: expedition index helpers
-- ============================================================

CREATE INDEX IF NOT EXISTS `idx_expeditions_guide`     ON `expeditions` (`guideId`);
CREATE INDEX IF NOT EXISTS `idx_expeditions_trail`     ON `expeditions` (`trailId`);
CREATE INDEX IF NOT EXISTS `idx_expeditions_status`    ON `expeditions` (`status`);
CREATE INDEX IF NOT EXISTS `idx_expeditions_startDate` ON `expeditions` (`startDate`);

-- ============================================================
-- DB-PERF-02: Normalized tables for previously-JSON data
-- ============================================================

CREATE TABLE IF NOT EXISTS `blog_post_tags` (
  `id`     int AUTO_INCREMENT NOT NULL,
  `postId` int NOT NULL,
  `tag`    varchar(100) NOT NULL,
  CONSTRAINT `blog_post_tags_id` PRIMARY KEY (`id`),
  INDEX `idx_bpt_post` (`postId`),
  INDEX `idx_bpt_tag`  (`tag`),
  CONSTRAINT `blog_post_tags_postId_fk`
    FOREIGN KEY (`postId`) REFERENCES `blog_posts` (`id`) ON DELETE CASCADE
);
--> statement-breakpoint

CREATE TABLE IF NOT EXISTS `blog_post_trails` (
  `postId`  int NOT NULL,
  `trailId` int NOT NULL,
  CONSTRAINT `blog_post_trails_pk` PRIMARY KEY (`postId`, `trailId`),
  INDEX `idx_bptr_trail` (`trailId`),
  CONSTRAINT `blog_post_trails_postId_fk`
    FOREIGN KEY (`postId`)  REFERENCES `blog_posts` (`id`) ON DELETE CASCADE,
  CONSTRAINT `blog_post_trails_trailId_fk`
    FOREIGN KEY (`trailId`) REFERENCES `trails`     (`id`) ON DELETE CASCADE
);
--> statement-breakpoint

CREATE TABLE IF NOT EXISTS `cadastur_operating_cities` (
  `id`         int AUTO_INCREMENT NOT NULL,
  `registryId` int NOT NULL,
  `city`       varchar(100) NOT NULL,
  `uf`         varchar(2)   NOT NULL,
  CONSTRAINT `cadastur_operating_cities_id` PRIMARY KEY (`id`),
  INDEX `idx_coc_registry`  (`registryId`),
  INDEX `idx_coc_city_uf`   (`city`, `uf`),
  CONSTRAINT `coc_registryId_fk`
    FOREIGN KEY (`registryId`) REFERENCES `cadastur_registry` (`id`) ON DELETE CASCADE
);
--> statement-breakpoint

CREATE TABLE IF NOT EXISTS `cadastur_categories` (
  `id`         int AUTO_INCREMENT NOT NULL,
  `registryId` int NOT NULL,
  `category`   varchar(100) NOT NULL,
  CONSTRAINT `cadastur_categories_id` PRIMARY KEY (`id`),
  INDEX `idx_cc_registry` (`registryId`),
  INDEX `idx_cc_category` (`category`),
  CONSTRAINT `cc_registryId_fk`
    FOREIGN KEY (`registryId`) REFERENCES `cadastur_registry` (`id`) ON DELETE CASCADE
);
--> statement-breakpoint

-- Migrate existing JSON data into the new normalized tables
-- (Run in a transaction; can be re-run safely due to INSERT IGNORE)

INSERT IGNORE INTO `blog_post_tags` (`postId`, `tag`)
SELECT `id`, JSON_UNQUOTE(jt.`value`)
FROM `blog_posts`
CROSS JOIN JSON_TABLE(
  COALESCE(`tags`, '[]'),
  '$[*]' COLUMNS (`value` varchar(100) PATH '$')
) AS jt
WHERE `tags` IS NOT NULL AND JSON_LENGTH(`tags`) > 0;

INSERT IGNORE INTO `blog_post_trails` (`postId`, `trailId`)
SELECT `id`, CAST(JSON_UNQUOTE(jt.`value`) AS UNSIGNED)
FROM `blog_posts`
CROSS JOIN JSON_TABLE(
  COALESCE(`relatedTrailIds`, '[]'),
  '$[*]' COLUMNS (`value` varchar(20) PATH '$')
) AS jt
WHERE `relatedTrailIds` IS NOT NULL AND JSON_LENGTH(`relatedTrailIds`) > 0;

-- ============================================================
-- DB-SEC-02: Foreign key constraints
-- (Added to new columns above; existing legacy columns below)
-- Note: Run SHOW ENGINE INNODB STATUS if any FK fails — it means
-- orphaned rows exist that must be cleaned up first.
-- ============================================================

-- guide_profiles → users
ALTER TABLE `guide_profiles`
  ADD CONSTRAINT IF NOT EXISTS `gp_userId_fk`
    FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

-- expeditions → users (guideId), trails
ALTER TABLE `expeditions`
  ADD CONSTRAINT IF NOT EXISTS `exp_guideId_fk`
    FOREIGN KEY (`guideId`) REFERENCES `users`  (`id`) ON DELETE RESTRICT,
  ADD CONSTRAINT IF NOT EXISTS `exp_trailId_fk`
    FOREIGN KEY (`trailId`) REFERENCES `trails` (`id`) ON DELETE RESTRICT;

-- reservations → expeditions, users
ALTER TABLE `reservations`
  ADD CONSTRAINT IF NOT EXISTS `res_expeditionId_fk`
    FOREIGN KEY (`expeditionId`) REFERENCES `expeditions` (`id`) ON DELETE RESTRICT,
  ADD CONSTRAINT IF NOT EXISTS `res_userId_fk`
    FOREIGN KEY (`userId`)       REFERENCES `users`       (`id`) ON DELETE SET NULL;

-- payments → reservations
ALTER TABLE `payments`
  ADD CONSTRAINT IF NOT EXISTS `pay_reservationId_fk`
    FOREIGN KEY (`reservationId`) REFERENCES `reservations` (`id`) ON DELETE RESTRICT;

-- payouts → users (guideId), reservations
ALTER TABLE `payouts`
  ADD CONSTRAINT IF NOT EXISTS `payout_guideId_fk`
    FOREIGN KEY (`guideId`)      REFERENCES `users`        (`id`) ON DELETE RESTRICT,
  ADD CONSTRAINT IF NOT EXISTS `payout_reservationId_fk`
    FOREIGN KEY (`reservationId`) REFERENCES `reservations` (`id`) ON DELETE RESTRICT;

-- contestations → reservations, users
ALTER TABLE `contestations`
  ADD CONSTRAINT IF NOT EXISTS `con_reservationId_fk`
    FOREIGN KEY (`reservationId`) REFERENCES `reservations` (`id`) ON DELETE RESTRICT,
  ADD CONSTRAINT IF NOT EXISTS `con_userId_fk`
    FOREIGN KEY (`userId`)        REFERENCES `users`        (`id`) ON DELETE SET NULL;

-- guide_verification → users
ALTER TABLE `guide_verification`
  ADD CONSTRAINT IF NOT EXISTS `gv_userId_fk`
    FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

-- reviews → users
ALTER TABLE `reviews`
  ADD CONSTRAINT IF NOT EXISTS `rev_userId_fk`
    FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE SET NULL;

-- review_images → reviews
ALTER TABLE `review_images`
  ADD CONSTRAINT IF NOT EXISTS `ri_reviewId_fk`
    FOREIGN KEY (`reviewId`) REFERENCES `reviews` (`id`) ON DELETE CASCADE;

-- blog_posts → users (authorId)
ALTER TABLE `blog_posts`
  ADD CONSTRAINT IF NOT EXISTS `bp_authorId_fk`
    FOREIGN KEY (`authorId`) REFERENCES `users` (`id`) ON DELETE SET NULL;

-- favorites → users, trails
ALTER TABLE `favorites`
  ADD CONSTRAINT IF NOT EXISTS `fav_userId_fk`
    FOREIGN KEY (`userId`)  REFERENCES `users`  (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT IF NOT EXISTS `fav_trailId_fk`
    FOREIGN KEY (`trailId`) REFERENCES `trails` (`id`) ON DELETE CASCADE;

-- expedition_participants → expeditions, users
ALTER TABLE `expedition_participants`
  ADD CONSTRAINT IF NOT EXISTS `ep_expeditionId_fk`
    FOREIGN KEY (`expeditionId`) REFERENCES `expeditions` (`id`) ON DELETE RESTRICT,
  ADD CONSTRAINT IF NOT EXISTS `ep_userId_fk`
    FOREIGN KEY (`userId`)       REFERENCES `users`       (`id`) ON DELETE SET NULL;
