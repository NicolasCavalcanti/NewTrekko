/**
 * DATABASE ENGINE AUDIT — 2026-03-25
 * ============================================================
 * CONFIRMED ENGINE: MySQL 8.x
 *   - drizzle.config.ts: dialect = "mysql"
 *   - server/db.ts: drizzle-orm/mysql2 driver
 *   - All migrations use MySQL DDL (ENUM, AUTO_INCREMENT, etc.)
 *
 * MIGRATION TO POSTGRESQL: Not planned yet.
 *   - If migration happens, the following raw mysql2 queries in server/db.ts
 *     must be ported to pg/Drizzle-postgres:
 *       · getReviews()         — uses db.execute(sql`…`) with mysql2 result shape [rows][0]
 *       · getRatingStats()     — same
 *       · getUserReview()      — same
 *       · createReview()       — same
 *       · updateRatingStats()  — ON DUPLICATE KEY UPDATE (postgres: INSERT … ON CONFLICT)
 *     Additional scripts bypassing Drizzle that must be ported:
 *       · restore-data.mjs, check-schema2.mjs, scripts/import-cadastur.mjs
 *         — all use mysql2.createConnection() directly.
 *
 * POSTGRESQL-ONLY FEATURES REFERENCED IN todo.md:
 *   - unaccent() function for accent-insensitive search
 *   - jsonb operators for querying JSON arrays
 *   Both are unavailable in MySQL; current workarounds use collation-based
 *   case/accent-insensitive indexes (utf8mb4_unicode_ci) instead.
 * ============================================================
 */

import {
  int,
  mysqlEnum,
  mysqlTable,
  text,
  timestamp,
  varchar,
  decimal,
  json,
  index,
  uniqueIndex,
} from "drizzle-orm/mysql-core";
import { sql } from "drizzle-orm";

// ---------------------------------------------------------------------------
// Reusable timestamp mixin (DB-ARCH-04)
// Apply to every table that needs both createdAt and auto-updating updatedAt.
// ---------------------------------------------------------------------------
export const timestamps = {
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
};

// ---------------------------------------------------------------------------
// users
// ---------------------------------------------------------------------------
export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  passwordHash: varchar("passwordHash", { length: 256 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  userType: mysqlEnum("userType", ["trekker", "guide"]).default("trekker").notNull(),
  bio: text("bio"),
  photoUrl: text("photoUrl"),
  cadasturNumber: varchar("cadasturNumber", { length: 64 }),
  cadasturValidated: int("cadasturValidated").default(0),
  // DB-ARCH-01: archive instead of hard-delete
  archivedAt: timestamp("archivedAt"),
  ...timestamps,
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

// ---------------------------------------------------------------------------
// guide_profiles
// ---------------------------------------------------------------------------
export const guideProfiles = mysqlTable("guide_profiles", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: FK → users.id (cascade: delete profile when user is deleted)
  userId: int("userId").notNull().references(() => users.id, { onDelete: "cascade" }),
  cadasturNumber: varchar("cadasturNumber", { length: 64 }).notNull(),
  cadasturValidatedAt: timestamp("cadasturValidatedAt"),
  cadasturExpiresAt: timestamp("cadasturExpiresAt"),
  uf: varchar("uf", { length: 2 }),
  city: varchar("city", { length: 128 }),
  categories: json("categories").$type<string[]>(),
  languages: json("languages").$type<string[]>(),
  contactPhone: varchar("contactPhone", { length: 32 }),
  contactEmail: varchar("contactEmail", { length: 320 }),
  website: text("website"),
  ...timestamps,
});

export type GuideProfile = typeof guideProfiles.$inferSelect;
export type InsertGuideProfile = typeof guideProfiles.$inferInsert;

// ---------------------------------------------------------------------------
// trails  (DB-PERF-03, DB-ARCH-02, DB-ARCH-03, DB-ARCH-04)
// ---------------------------------------------------------------------------
export const trails = mysqlTable("trails", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 256 }).notNull(),
  // DB-PERF-03: slug for SEO URLs
  slug: varchar("slug", { length: 200 }).unique(),
  uf: varchar("uf", { length: 2 }).notNull(),
  city: varchar("city", { length: 128 }),
  region: varchar("region", { length: 256 }),
  park: varchar("park", { length: 256 }),
  distanceKm: decimal("distanceKm", { precision: 8, scale: 2 }),
  elevationGain: int("elevationGain"),
  maxAltitude: int("maxAltitude"),
  difficulty: mysqlEnum("difficulty", ["easy", "moderate", "hard", "expert"]).default("moderate"),
  description: text("description"),
  shortDescription: text("shortDescription"),
  hookText: text("hookText"),
  ctaText: text("ctaText"),
  guideRequired: int("guideRequired").default(0),
  entranceFee: varchar("entranceFee", { length: 64 }),
  /* display-only: not queryable */ waterPoints: json("waterPoints").$type<string[]>(),
  /* display-only: not queryable */ campingPoints: json("campingPoints").$type<string[]>(),
  bestSeason: varchar("bestSeason", { length: 128 }),
  estimatedTime: varchar("estimatedTime", { length: 64 }),
  trailType: mysqlEnum("trailType", ["linear", "circular", "traverse"]).default("linear"),
  imageUrl: text("imageUrl"),
  /* display-only: not queryable */ images: json("images").$type<string[]>(),
  // DB-ARCH-02: deprecated — use latitude/longitude for proximity queries
  /* deprecated: use latitude/longitude columns */ mapCoordinates: json("mapCoordinates").$type<{ lat: number; lng: number }>(),
  // DB-ARCH-02: extracted lat/lng for Haversine proximity search
  latitude: decimal("latitude", { precision: 10, scale: 7 }),
  longitude: decimal("longitude", { precision: 10, scale: 7 }),
  /* display-only: not queryable */ highlights: json("highlights").$type<string[]>(),
  source: varchar("source", { length: 128 }),
  wiklocUrl: text("wikiloc_url"),
  wiklocGpxUrl: text("wikiloc_gpx_url"),
  // DB-ARCH-03: added 'archived' status
  status: mysqlEnum("status", ["draft", "published", "archived"]).default("draft"),
  ...timestamps,
}, (t) => [
  // DB-PERF-03: indexes for trail listing and detail queries
  uniqueIndex("idx_trails_slug").on(t.slug),
  index("idx_trails_status").on(t.status),
  index("idx_trails_uf").on(t.uf),
  index("idx_trails_difficulty").on(t.difficulty),
  index("idx_trails_status_uf").on(t.status, t.uf),
  // DB-ARCH-02: index for proximity bounding-box pre-filter
  index("idx_trails_geo").on(t.latitude, t.longitude),
]);

export type Trail = typeof trails.$inferSelect;
export type InsertTrail = typeof trails.$inferInsert;

// ---------------------------------------------------------------------------
// expeditions  (DB-PERF-04: enrolledCount removed — derived from reservations)
// ---------------------------------------------------------------------------
export const expeditions = mysqlTable("expeditions", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: FKs with restrict to prevent guide/trail deletion while expeditions exist
  guideId: int("guideId").notNull().references(() => users.id, { onDelete: "restrict" }),
  trailId: int("trailId").notNull().references(() => trails.id, { onDelete: "restrict" }),
  title: varchar("title", { length: 256 }),
  description: text("description"),
  startDate: timestamp("startDate").notNull(),
  endDate: timestamp("endDate"),
  startTime: varchar("startTime", { length: 8 }),
  endTime: varchar("endTime", { length: 8 }),
  capacity: int("capacity").default(10),
  // DB-PERF-04: enrolledCount removed — use expedition_availability view instead
  price: decimal("price", { precision: 10, scale: 2 }),
  meetingPoint: text("meetingPoint"),
  guideNotes: text("guideNotes"),
  /* display-only: not queryable */ includedItems: json("includedItems").$type<string[]>(),
  /* display-only: not queryable */ images: json("images").$type<string[]>(),
  status: mysqlEnum("status", ["draft", "published", "active", "full", "closed", "cancelled", "completed"]).default("draft"),
  completedAt: timestamp("completedAt"),
  contestationEndDate: timestamp("contestationEndDate"),
  ...timestamps,
}, (t) => [
  index("idx_expeditions_guide").on(t.guideId),
  index("idx_expeditions_trail").on(t.trailId),
  index("idx_expeditions_status").on(t.status),
  index("idx_expeditions_startDate").on(t.startDate),
]);

export type Expedition = typeof expeditions.$inferSelect;
export type InsertExpedition = typeof expeditions.$inferInsert;

// ---------------------------------------------------------------------------
// favorites
// ---------------------------------------------------------------------------
export const favorites = mysqlTable("favorites", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: FKs
  userId: int("userId").notNull().references(() => users.id, { onDelete: "cascade" }),
  trailId: int("trailId").notNull().references(() => trails.id, { onDelete: "cascade" }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (t) => [
  uniqueIndex("idx_favorites_user_trail").on(t.userId, t.trailId),
]);

export type Favorite = typeof favorites.$inferSelect;
export type InsertFavorite = typeof favorites.$inferInsert;

// ---------------------------------------------------------------------------
// expedition_participants
// ---------------------------------------------------------------------------
export const expeditionParticipants = mysqlTable("expedition_participants", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: FKs
  expeditionId: int("expeditionId").notNull().references(() => expeditions.id, { onDelete: "restrict" }),
  userId: int("userId").notNull().references(() => users.id, { onDelete: "set null" }),
  status: mysqlEnum("status", ["interested", "confirmed", "cancelled"]).default("interested"),
  ...timestamps,
}, (t) => [
  index("idx_exp_participants_expedition").on(t.expeditionId),
  index("idx_exp_participants_user").on(t.userId),
]);

export type ExpeditionParticipant = typeof expeditionParticipants.$inferSelect;
export type InsertExpeditionParticipant = typeof expeditionParticipants.$inferInsert;

// ---------------------------------------------------------------------------
// system_events
// ---------------------------------------------------------------------------
export const systemEvents = mysqlTable("system_events", {
  id: int("id").autoincrement().primaryKey(),
  type: varchar("type", { length: 64 }).notNull(),
  message: text("message").notNull(),
  severity: mysqlEnum("severity", ["info", "warning", "error"]).default("info"),
  actorId: int("actorId"),
  /* display-only: not queryable */ metadata: json("metadata").$type<Record<string, unknown>>(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type SystemEvent = typeof systemEvents.$inferSelect;
export type InsertSystemEvent = typeof systemEvents.$inferInsert;

// ---------------------------------------------------------------------------
// cadastur_registry  (DB-SEC-03, DB-PERF-01, DB-ARCH-04)
// ---------------------------------------------------------------------------
export const cadasturRegistry = mysqlTable("cadastur_registry", {
  id: int("id").autoincrement().primaryKey(),
  certificateNumber: varchar("certificateNumber", { length: 64 }).notNull().unique(),
  fullName: varchar("fullName", { length: 256 }).notNull(),
  uf: varchar("uf", { length: 2 }).notNull(),
  city: varchar("city", { length: 128 }),
  phone: varchar("phone", { length: 32 }),
  // DB-SEC-03: masked variants for public API responses
  phoneMasked: varchar("phoneMasked", { length: 20 }),
  email: varchar("email", { length: 320 }),
  // DB-SEC-03: masked variant; use this for unauthenticated requests
  emailMasked: varchar("emailMasked", { length: 255 }),
  website: text("website"),
  validUntil: timestamp("validUntil"),
  /* display-only: not queryable */ languages: json("languages").$type<string[]>(),
  // DB-PERF-02: operatingCities moved to cadastur_operating_cities table for queryability
  /* display-only: not queryable — see cadastur_operating_cities table */ operatingCities: json("operatingCities").$type<string[]>(),
  // DB-PERF-02: categories moved to cadastur_categories table for queryability
  /* display-only: not queryable — see cadastur_categories table */ categories: json("categories").$type<string[]>(),
  /* display-only: not queryable */ segments: json("segments").$type<string[]>(),
  isDriverGuide: int("isDriverGuide").default(0),
  // DB-ARCH-04: importedAt tracks when this row was synced from the government dataset
  importedAt: timestamp("importedAt").defaultNow().notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (t) => [
  // DB-PERF-01: indexes for the guide search hot path
  index("idx_cadastur_fullname").on(t.fullName),
  index("idx_cadastur_uf").on(t.uf),
  index("idx_cadastur_city").on(t.city),
  index("idx_cadastur_uf_city").on(t.uf, t.city),
  index("idx_cadastur_valid").on(t.validUntil),
  index("idx_cadastur_uf_fullname").on(t.uf, t.fullName),
  // DB-SEC-03: for internal auth-gated lookups by exact email
  index("idx_cadastur_email").on(t.email),
]);

export type CadasturRegistry = typeof cadasturRegistry.$inferSelect;
export type InsertCadasturRegistry = typeof cadasturRegistry.$inferInsert;

// ---------------------------------------------------------------------------
// DB-PERF-02: cadastur_operating_cities (normalized from JSON operatingCities)
// ---------------------------------------------------------------------------
export const cadasturOperatingCities = mysqlTable("cadastur_operating_cities", {
  id: int("id").autoincrement().primaryKey(),
  registryId: int("registryId").notNull().references(() => cadasturRegistry.id, { onDelete: "cascade" }),
  city: varchar("city", { length: 100 }).notNull(),
  uf: varchar("uf", { length: 2 }).notNull(),
}, (t) => [
  index("idx_coc_registry").on(t.registryId),
  index("idx_coc_city_uf").on(t.city, t.uf),
]);

export type CadasturOperatingCity = typeof cadasturOperatingCities.$inferSelect;
export type InsertCadasturOperatingCity = typeof cadasturOperatingCities.$inferInsert;

// ---------------------------------------------------------------------------
// DB-PERF-02: cadastur_categories (normalized from JSON categories)
// ---------------------------------------------------------------------------
export const cadasturCategories = mysqlTable("cadastur_categories", {
  id: int("id").autoincrement().primaryKey(),
  registryId: int("registryId").notNull().references(() => cadasturRegistry.id, { onDelete: "cascade" }),
  category: varchar("category", { length: 100 }).notNull(),
}, (t) => [
  index("idx_cc_registry").on(t.registryId),
  index("idx_cc_category").on(t.category),
]);

export type CadasturCategory = typeof cadasturCategories.$inferSelect;
export type InsertCadasturCategory = typeof cadasturCategories.$inferInsert;

// ---------------------------------------------------------------------------
// blog_posts  (DB-PERF-02, DB-ARCH-01)
// ---------------------------------------------------------------------------
export const blogPosts = mysqlTable("blog_posts", {
  id: int("id").autoincrement().primaryKey(),
  slug: varchar("slug", { length: 256 }).notNull().unique(),
  title: varchar("title", { length: 256 }).notNull(),
  subtitle: text("subtitle"),
  content: text("content").notNull(),
  excerpt: text("excerpt"),
  category: mysqlEnum("category", [
    "trilhas-destinos",
    "guias-praticos",
    "planejamento-seguranca",
    "equipamentos",
    "conservacao-ambiental",
    "historias-inspiracao",
  ]).default("trilhas-destinos"),
  imageUrl: text("imageUrl"),
  /* display-only: not queryable */ images: json("images").$type<string[]>(),
  // DB-SEC-02: FK set null so author deletion preserves the article
  authorId: int("authorId").references(() => users.id, { onDelete: "set null" }),
  authorName: varchar("authorName", { length: 128 }),
  readingTime: int("readingTime").default(5),
  // DB-PERF-02: relatedTrailIds moved to blog_post_trails join table
  /* display-only: not queryable — see blog_post_trails table */ relatedTrailIds: json("relatedTrailIds").$type<number[]>(),
  // DB-PERF-02: tags moved to blog_post_tags table
  /* display-only: not queryable — see blog_post_tags table */ tags: json("tags").$type<string[]>(),
  metaTitle: varchar("metaTitle", { length: 256 }),
  metaDescription: text("metaDescription"),
  featured: int("featured").default(0),
  viewCount: int("viewCount").default(0),
  status: mysqlEnum("status", ["draft", "published"]).default("draft"),
  publishedAt: timestamp("publishedAt"),
  ...timestamps,
}, (t) => [
  index("idx_blog_status").on(t.status),
  index("idx_blog_category").on(t.category),
  index("idx_blog_featured").on(t.featured),
  index("idx_blog_published").on(t.publishedAt),
]);

export type BlogPost = typeof blogPosts.$inferSelect;
export type InsertBlogPost = typeof blogPosts.$inferInsert;

// ---------------------------------------------------------------------------
// DB-PERF-02: blog_post_tags (normalized from JSON tags)
// ---------------------------------------------------------------------------
export const blogPostTags = mysqlTable("blog_post_tags", {
  id: int("id").autoincrement().primaryKey(),
  postId: int("postId").notNull().references(() => blogPosts.id, { onDelete: "cascade" }),
  tag: varchar("tag", { length: 100 }).notNull(),
}, (t) => [
  index("idx_bpt_post").on(t.postId),
  index("idx_bpt_tag").on(t.tag),
]);

export type BlogPostTag = typeof blogPostTags.$inferSelect;
export type InsertBlogPostTag = typeof blogPostTags.$inferInsert;

// ---------------------------------------------------------------------------
// DB-PERF-02: blog_post_trails (normalized from JSON relatedTrailIds)
// ---------------------------------------------------------------------------
export const blogPostTrails = mysqlTable("blog_post_trails", {
  postId: int("postId").notNull().references(() => blogPosts.id, { onDelete: "cascade" }),
  trailId: int("trailId").notNull().references(() => trails.id, { onDelete: "cascade" }),
}, (t) => [
  uniqueIndex("idx_bptr_post_trail").on(t.postId, t.trailId),
  index("idx_bptr_trail").on(t.trailId),
]);

export type BlogPostTrail = typeof blogPostTrails.$inferSelect;
export type InsertBlogPostTrail = typeof blogPostTrails.$inferInsert;

// ---------------------------------------------------------------------------
// guide_verification  (DB-SEC-01, DB-SEC-02)
// ---------------------------------------------------------------------------
export const guideVerification = mysqlTable("guide_verification", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: cascade — delete verification when user is deleted
  userId: int("userId").notNull().unique().references(() => users.id, { onDelete: "cascade" }),
  status: mysqlEnum("status", ["pending", "approved", "rejected", "suspended"]).default("pending").notNull(),
  documentType: mysqlEnum("documentType", ["cpf", "cnpj"]).default("cpf"),
  // DB-SEC-01 /* ENCRYPTED */ — AES-256-GCM encrypted at application layer via server/lib/crypto.ts
  documentNumber: varchar("documentNumber", { length: 256 }),
  pixKeyType: mysqlEnum("pixKeyType", ["cpf", "cnpj", "email", "phone", "random"]),
  // DB-SEC-01 /* ENCRYPTED */ — AES-256-GCM encrypted at application layer via server/lib/crypto.ts
  pixKey: varchar("pixKey", { length: 512 }),
  pixKeyHolderName: varchar("pixKeyHolderName", { length: 256 }),
  // DB-SEC-01 /* ENCRYPTED */ — AES-256-GCM encrypted at application layer via server/lib/crypto.ts
  pixKeyDocument: varchar("pixKeyDocument", { length: 256 }),
  pixKeyVerified: int("pixKeyVerified").default(0),
  bankCode: varchar("bankCode", { length: 8 }),
  bankName: varchar("bankName", { length: 128 }),
  agencyNumber: varchar("agencyNumber", { length: 16 }),
  accountNumber: varchar("accountNumber", { length: 32 }),
  accountType: mysqlEnum("accountType", ["checking", "savings"]).default("checking"),
  accountHolderName: varchar("accountHolderName", { length: 256 }),
  accountHolderDocument: varchar("accountHolderDocument", { length: 32 }),
  documentUrl: text("documentUrl"),
  bankProofUrl: text("bankProofUrl"),
  mpUserId: varchar("mpUserId", { length: 128 }),
  mpAccountStatus: varchar("mpAccountStatus", { length: 64 }),
  acceptedIntermediationTerms: int("acceptedIntermediationTerms").default(0),
  acceptedPayoutTerms: int("acceptedPayoutTerms").default(0),
  acceptedContestationPolicy: int("acceptedContestationPolicy").default(0),
  termsAcceptedAt: timestamp("termsAcceptedAt"),
  reviewedBy: int("reviewedBy"),
  reviewedAt: timestamp("reviewedAt"),
  rejectionReason: text("rejectionReason"),
  notes: text("notes"),
  ...timestamps,
});

export type GuideVerification = typeof guideVerification.$inferSelect;
export type InsertGuideVerification = typeof guideVerification.$inferInsert;

// ---------------------------------------------------------------------------
// cancellation_policies
// ---------------------------------------------------------------------------
export const cancellationPolicies = mysqlTable("cancellation_policies", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 128 }).notNull(),
  description: text("description"),
  fullRefundDays: int("fullRefundDays").default(7),
  partialRefundDays: int("partialRefundDays").default(3),
  partialRefundPercent: int("partialRefundPercent").default(50),
  noRefundDays: int("noRefundDays").default(0),
  isDefault: int("isDefault").default(0),
  ...timestamps,
});

export type CancellationPolicy = typeof cancellationPolicies.$inferSelect;
export type InsertCancellationPolicy = typeof cancellationPolicies.$inferInsert;

// ---------------------------------------------------------------------------
// reservations  (DB-SEC-02, DB-ARCH-01)
// ---------------------------------------------------------------------------
export const reservations = mysqlTable("reservations", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: restrict — don't delete expedition with active reservations
  expeditionId: int("expeditionId").notNull().references(() => expeditions.id, { onDelete: "restrict" }),
  // DB-SEC-02: set null — allow user account deletion, preserve financial record
  userId: int("userId").notNull().references(() => users.id, { onDelete: "set null" }),
  quantity: int("quantity").default(1).notNull(),
  unitPrice: decimal("unitPrice", { precision: 10, scale: 2 }).notNull(),
  totalAmount: decimal("totalAmount", { precision: 10, scale: 2 }).notNull(),
  status: mysqlEnum("status", [
    "created",
    "pending_payment",
    "paid",
    "awaiting_expedition",
    "expedition_in_progress",
    "completed_contestation",
    "in_dispute",
    "payout_sent",
    "cancelled",
    "refunded",
    "no_show",
  ]).default("created").notNull(),
  expeditionCompletedAt: timestamp("expeditionCompletedAt"),
  guideConfirmedCompletion: int("guideConfirmedCompletion").default(0),
  userConfirmedCompletion: int("userConfirmedCompletion").default(0),
  contestationEndsAt: timestamp("contestationEndsAt"),
  payoutScheduledAt: timestamp("payoutScheduledAt"),
  payoutCompletedAt: timestamp("payoutCompletedAt"),
  mpPreferenceId: varchar("mpPreferenceId", { length: 128 }),
  mpPaymentId: varchar("mpPaymentId", { length: 128 }),
  mpExternalReference: varchar("mpExternalReference", { length: 128 }),
  paymentMethod: mysqlEnum("paymentMethod", ["card", "pix", "boleto", "account_money"]),
  expiresAt: timestamp("expiresAt"),
  paidAt: timestamp("paidAt"),
  cancelledAt: timestamp("cancelledAt"),
  cancellationReason: text("cancellationReason"),
  cancelledBy: mysqlEnum("cancelledBy", ["user", "guide", "admin", "system"]),
  refundedAt: timestamp("refundedAt"),
  refundAmount: decimal("refundAmount", { precision: 10, scale: 2 }),
  mpRefundId: varchar("mpRefundId", { length: 128 }),
  // DB-ARCH-01: soft delete — use UPDATE SET deletedAt instead of DELETE
  deletedAt: timestamp("deletedAt"),
  ...timestamps,
}, (t) => [
  index("idx_reservations_expedition").on(t.expeditionId),
  index("idx_reservations_user").on(t.userId),
  index("idx_reservations_status").on(t.status),
  index("idx_reservations_deleted").on(t.deletedAt),
]);

export type Reservation = typeof reservations.$inferSelect;
export type InsertReservation = typeof reservations.$inferInsert;

// ---------------------------------------------------------------------------
// payments  (DB-SEC-02, DB-ARCH-01)
// ---------------------------------------------------------------------------
export const payments = mysqlTable("payments", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: restrict — financial records must never be orphaned
  reservationId: int("reservationId").notNull().references(() => reservations.id, { onDelete: "restrict" }),
  mpPaymentId: varchar("mpPaymentId", { length: 128 }).notNull(),
  status: mysqlEnum("status", ["pending", "approved", "rejected", "refunded", "partially_refunded", "cancelled"]).default("pending").notNull(),
  grossAmount: decimal("grossAmount", { precision: 10, scale: 2 }).notNull(),
  platformFee: decimal("platformFee", { precision: 10, scale: 2 }).notNull(),
  mpFee: decimal("mpFee", { precision: 10, scale: 2 }),
  netAmount: decimal("netAmount", { precision: 10, scale: 2 }).notNull(),
  paymentMethod: mysqlEnum("paymentMethod", ["card", "pix", "boleto", "account_money"]),
  paymentTypeId: varchar("paymentTypeId", { length: 64 }),
  currency: varchar("currency", { length: 3 }).default("BRL"),
  /* display-only: not queryable */ metadata: json("metadata").$type<Record<string, unknown>>(),
  // DB-ARCH-01: soft delete
  deletedAt: timestamp("deletedAt"),
  ...timestamps,
});

export type Payment = typeof payments.$inferSelect;
export type InsertPayment = typeof payments.$inferInsert;

// ---------------------------------------------------------------------------
// payouts  (DB-SEC-02, DB-ARCH-01)
// ---------------------------------------------------------------------------
export const payouts = mysqlTable("payouts", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: restrict — financial records must never be orphaned
  guideId: int("guideId").notNull().references(() => users.id, { onDelete: "restrict" }),
  reservationId: int("reservationId").references(() => reservations.id, { onDelete: "restrict" }),
  status: mysqlEnum("status", ["scheduled", "processing", "sent", "failed", "completed", "blocked"]).default("scheduled").notNull(),
  grossAmount: decimal("grossAmount", { precision: 10, scale: 2 }).notNull(),
  platformFee: decimal("platformFee", { precision: 10, scale: 2 }).notNull(),
  gatewayFee: decimal("gatewayFee", { precision: 10, scale: 2 }),
  netAmount: decimal("netAmount", { precision: 10, scale: 2 }).notNull(),
  currency: varchar("currency", { length: 3 }).default("BRL"),
  pixKey: varchar("pixKey", { length: 256 }),
  pixKeyType: varchar("pixKeyType", { length: 32 }),
  pixTransactionId: varchar("pixTransactionId", { length: 128 }),
  pixReceiptUrl: text("pixReceiptUrl"),
  pixEndToEndId: varchar("pixEndToEndId", { length: 64 }),
  scheduledDate: timestamp("scheduledDate").notNull(),
  processedAt: timestamp("processedAt"),
  completedAt: timestamp("completedAt"),
  /* display-only: not queryable */ paymentIds: json("paymentIds").$type<number[]>(),
  failureReason: text("failureReason"),
  retryCount: int("retryCount").default(0),
  // DB-ARCH-01: soft delete
  deletedAt: timestamp("deletedAt"),
  ...timestamps,
}, (t) => [
  index("idx_payouts_guide").on(t.guideId),
  index("idx_payouts_status").on(t.status),
]);

export type Payout = typeof payouts.$inferSelect;
export type InsertPayout = typeof payouts.$inferInsert;

// ---------------------------------------------------------------------------
// payment_audit_log  (DB-SEC-02, DB-SEC-04)
// ---------------------------------------------------------------------------
export const paymentAuditLog = mysqlTable("payment_audit_log", {
  id: int("id").autoincrement().primaryKey(),
  entityType: mysqlEnum("entityType", ["reservation", "payment", "payout", "guide_verification"]).notNull(),
  entityId: int("entityId").notNull(),
  action: varchar("action", { length: 64 }).notNull(),
  previousValue: text("previousValue"),
  newValue: text("newValue"),
  actorId: int("actorId"),
  actorType: mysqlEnum("actorType", ["user", "guide", "admin", "system"]).default("system"),
  ipAddress: varchar("ipAddress", { length: 64 }),
  userAgent: text("userAgent"),
  // DB-SEC-04: sanitized to allowlist keys, max 4096 chars, stored as text not json
  payload: text("payload"),
  // DB-SEC-04: origin of the log entry
  source: varchar("source", { length: 50 }).default("system"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
}, (t) => [
  // DB-SEC-04: index for retention cleanup (purge rows older than 365 days)
  index("idx_audit_created").on(t.createdAt),
  index("idx_audit_entity").on(t.entityType, t.entityId),
]);

export type PaymentAuditLog = typeof paymentAuditLog.$inferSelect;
export type InsertPaymentAuditLog = typeof paymentAuditLog.$inferInsert;

// ---------------------------------------------------------------------------
// platform_settings
// ---------------------------------------------------------------------------
export const platformSettings = mysqlTable("platform_settings", {
  id: int("id").autoincrement().primaryKey(),
  key: varchar("key", { length: 128 }).notNull().unique(),
  value: text("value").notNull(),
  description: text("description"),
  updatedBy: int("updatedBy"),
  ...timestamps,
});

export type PlatformSetting = typeof platformSettings.$inferSelect;
export type InsertPlatformSetting = typeof platformSettings.$inferInsert;

// ---------------------------------------------------------------------------
// contestations  (DB-SEC-02, DB-ARCH-01)
// ---------------------------------------------------------------------------
export const contestations = mysqlTable("contestations", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: restrict — disputes must reference valid reservations
  reservationId: int("reservationId").notNull().references(() => reservations.id, { onDelete: "restrict" }),
  // DB-SEC-02: set null — allow user deletion while preserving dispute record
  userId: int("userId").notNull().references(() => users.id, { onDelete: "set null" }),
  guideId: int("guideId").notNull(),
  status: mysqlEnum("status", ["open", "under_review", "resolved_user", "resolved_guide", "closed"]).default("open").notNull(),
  reason: mysqlEnum("reason", [
    "expedition_not_completed",
    "different_from_description",
    "safety_issues",
    "guide_no_show",
    "poor_service",
    "other",
  ]).notNull(),
  description: text("description").notNull(),
  /* display-only: not queryable */ evidenceUrls: json("evidenceUrls").$type<string[]>(),
  guideResponse: text("guideResponse"),
  guideResponseAt: timestamp("guideResponseAt"),
  /* display-only: not queryable */ guideEvidenceUrls: json("guideEvidenceUrls").$type<string[]>(),
  resolution: text("resolution"),
  resolvedBy: int("resolvedBy"),
  resolvedAt: timestamp("resolvedAt"),
  refundAmount: decimal("refundAmount", { precision: 10, scale: 2 }),
  // DB-ARCH-01: soft delete
  deletedAt: timestamp("deletedAt"),
  ...timestamps,
});

export type Contestation = typeof contestations.$inferSelect;
export type InsertContestation = typeof contestations.$inferInsert;

// ---------------------------------------------------------------------------
// reviews  (DB-SEC-02, DB-PERF-07)
// ---------------------------------------------------------------------------
export const reviews = mysqlTable("reviews", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: set null — allow user deletion, preserve reviews
  userId: int("userId").notNull().references(() => users.id, { onDelete: "set null" }),
  targetType: mysqlEnum("targetType", ["trail", "guide"]).notNull(),
  targetId: int("targetId").notNull(),
  // DB-PERF-07: rating validated at DB level (0–5)
  rating: int("rating").notNull(),
  comment: text("comment").notNull(),
  helpfulCount: int("helpfulCount").default(0),
  isVerified: int("isVerified").default(0),
  reservationId: int("reservationId"),
  status: mysqlEnum("status", ["pending", "approved", "rejected", "flagged"]).default("approved").notNull(),
  moderatedBy: int("moderatedBy"),
  moderatedAt: timestamp("moderatedAt"),
  moderationReason: text("moderationReason"),
  ...timestamps,
}, (t) => [
  // DB-PERF-07: primary query pattern — load reviews for a trail or guide
  index("idx_reviews_target").on(t.targetType, t.targetId),
  index("idx_reviews_user").on(t.userId),
  index("idx_reviews_rating").on(t.rating),
  // DB-PERF-07: one review per user per target
  uniqueIndex("uniq_review").on(t.userId, t.targetType, t.targetId),
]);

export type Review = typeof reviews.$inferSelect;
export type InsertReview = typeof reviews.$inferInsert;

// ---------------------------------------------------------------------------
// review_images  (DB-SEC-02)
// ---------------------------------------------------------------------------
export const reviewImages = mysqlTable("review_images", {
  id: int("id").autoincrement().primaryKey(),
  // DB-SEC-02: cascade — images are owned by their review
  reviewId: int("reviewId").notNull().references(() => reviews.id, { onDelete: "cascade" }),
  imageUrl: text("imageUrl").notNull(),
  thumbnailUrl: text("thumbnailUrl"),
  displayOrder: int("displayOrder").default(0),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type ReviewImage = typeof reviewImages.$inferSelect;
export type InsertReviewImage = typeof reviewImages.$inferInsert;

// ---------------------------------------------------------------------------
// rating_stats
// ---------------------------------------------------------------------------
export const ratingStats = mysqlTable("rating_stats", {
  id: int("id").autoincrement().primaryKey(),
  targetType: mysqlEnum("targetType", ["trail", "guide"]).notNull(),
  targetId: int("targetId").notNull(),
  averageRating: decimal("averageRating", { precision: 3, scale: 2 }).default("0.00"),
  totalReviews: int("totalReviews").default(0),
  count1Star: int("count1Star").default(0),
  count2Star: int("count2Star").default(0),
  count3Star: int("count3Star").default(0),
  count4Star: int("count4Star").default(0),
  count5Star: int("count5Star").default(0),
  reviewsWithPhotos: int("reviewsWithPhotos").default(0),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
}, (t) => [
  uniqueIndex("uniq_rating_stats_target").on(t.targetType, t.targetId),
]);

export type RatingStats = typeof ratingStats.$inferSelect;
export type InsertRatingStats = typeof ratingStats.$inferInsert;

// ---------------------------------------------------------------------------
// guide_financial_info  (Story 5: separate financial routing data)
// Stores Pix key for payment routing, decoupled from identity verification.
// DB-SEC-01: pixKey stored AES-256-GCM encrypted via server/lib/crypto.ts
// DB-SEC-02: cascade — delete financial info when guide account is deleted
// ---------------------------------------------------------------------------
export const guideFinancialInfo = mysqlTable("guide_financial_info", {
  id: int("id").autoincrement().primaryKey(),
  guideId: int("guide_id").notNull().unique().references(() => users.id, { onDelete: "cascade" }),
  pixKeyType: mysqlEnum("pix_key_type", ["cpf", "cnpj", "email", "phone", "random"]),
  // DB-SEC-01 /* ENCRYPTED */ — AES-256-GCM encrypted at application layer
  pixKey: varchar("pix_key", { length: 512 }),
  pixKeyHolderName: varchar("pix_key_holder_name", { length: 256 }),
  pixKeyVerified: int("pix_key_verified").default(0),
  paymentEnabled: int("payment_enabled").default(0),
  ...timestamps,
});

export type GuideFinancialInfo = typeof guideFinancialInfo.$inferSelect;
export type InsertGuideFinancialInfo = typeof guideFinancialInfo.$inferInsert;
