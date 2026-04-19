-- ============================================================
-- Migration 0011 — guide_financial_info table
-- Story 5: Separate Pix payment routing data from identity
-- verification into its own table for cleaner domain separation.
-- DB-SEC-01: pix_key stored encrypted (AES-256-GCM, app layer)
-- DB-SEC-02: ON DELETE CASCADE from users
-- ============================================================

CREATE TABLE IF NOT EXISTS `guide_financial_info` (
  `id`                   int          NOT NULL AUTO_INCREMENT,
  `guide_id`             int          NOT NULL,
  `pix_key_type`         enum('cpf','cnpj','email','phone','random') NULL,
  `pix_key`              varchar(512) NULL COMMENT 'AES-256-GCM encrypted',
  `pix_key_holder_name`  varchar(256) NULL,
  `pix_key_verified`     int          NOT NULL DEFAULT 0,
  `payment_enabled`      int          NOT NULL DEFAULT 0,
  `createdAt`            timestamp    NOT NULL DEFAULT (now()),
  `updatedAt`            timestamp    NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT `guide_financial_info_id`       PRIMARY KEY (`id`),
  CONSTRAINT `guide_financial_info_guide_fk`
    FOREIGN KEY (`guide_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
);
--> statement-breakpoint

CREATE UNIQUE INDEX IF NOT EXISTS `idx_gfi_guide_id` ON `guide_financial_info` (`guide_id`);
