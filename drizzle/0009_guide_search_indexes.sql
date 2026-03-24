-- Indexes to speed up guide search on the 50k-row cadastur_registry table.
--
-- fullName  — prefix name search (LIKE 'term%').  A 64-char prefix index
--             covers all real-world first-name searches and keeps the index
--             small.  The column collation (utf8mb4_unicode_ci / _0900_ai_ci)
--             makes comparisons case- and accent-insensitive automatically.
--
-- uf        — exact state filter (eq).  Very selective; 27 distinct values
--             across 50k rows means ~1850 rows per state on average.
--
-- city      — exact city filter used after a state is selected.  Combined
--             with the uf index the optimizer can choose the best plan.
--
-- (uf, fullName) composite — covers the common pattern of filtering by state
--             AND searching by name in a single index scan.
--
-- certificateNumber already has a UNIQUE constraint (= implicit unique index)
-- so no additional index is needed for cadastur-code look-ups.

ALTER TABLE `cadastur_registry`
  ADD INDEX `idx_cadastur_fullname`    (`fullName`(64)),
  ADD INDEX `idx_cadastur_uf`          (`uf`),
  ADD INDEX `idx_cadastur_city`        (`city`(64)),
  ADD INDEX `idx_cadastur_uf_fullname` (`uf`, `fullName`(64));
