-- ============================================================
-- Migration 0012 — Audit Pix Key Changes
-- Story 7: extend payment_audit_log.entityType to cover
-- guide_financial_info events (pix_key_created, pix_key_updated)
-- ============================================================

ALTER TABLE `payment_audit_log`
  MODIFY COLUMN `entityType`
    enum('reservation','payment','payout','guide_verification','guide_financial_info')
    NOT NULL;
