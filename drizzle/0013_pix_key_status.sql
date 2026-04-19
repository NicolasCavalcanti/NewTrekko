-- ============================================================
-- Migration 0013 — Pix Key Status
-- Story 9: add pix_key_status enum column to guide_financial_info
-- State machine: pending → valid | invalid
-- Default 'pending'; set to 'valid' on every successful save/update
-- (validation already ran at the application layer before write).
-- ============================================================

ALTER TABLE `guide_financial_info`
  ADD COLUMN IF NOT EXISTS `pix_key_status`
    enum('pending','valid','invalid') NOT NULL DEFAULT 'pending'
    AFTER `pix_key_holder_name`;
