import { describe, expect, it, vi, beforeEach } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

// Mock the database functions
vi.mock("./db", () => ({
  getDb: vi.fn().mockResolvedValue({}),
  getTrails: vi.fn().mockResolvedValue({ trails: [], total: 0 }),
  getTrailById: vi.fn().mockResolvedValue({ id: 1, name: "Test Trail", city: "Rio", uf: "RJ", difficulty: "moderate" }),
  getExpeditionsByTrailId: vi.fn().mockResolvedValue([]),
  getExpeditions: vi.fn().mockResolvedValue({ expeditions: [], total: 0 }),
  getGuides: vi.fn().mockResolvedValue({ guides: [], total: 0 }),
  getGuideById: vi.fn().mockResolvedValue(null),
  getGuideProfile: vi.fn().mockResolvedValue(null),
  getGuideExpeditions: vi.fn().mockResolvedValue([]),
  getUserFavorites: vi.fn().mockResolvedValue([]),
  isFavorite: vi.fn().mockResolvedValue(false),
  addFavorite: vi.fn().mockResolvedValue(undefined),
  removeFavorite: vi.fn().mockResolvedValue(undefined),
  upsertUser: vi.fn().mockResolvedValue(undefined),
  getUserByOpenId: vi.fn().mockResolvedValue(null),
  getAdminMetrics: vi.fn().mockResolvedValue({ trails: 10, expeditions: 5, guides: 3, reservations: 20, revenue: 1500 }),
  getSystemEvents: vi.fn().mockResolvedValue([]),
  createSystemEvent: vi.fn().mockResolvedValue(undefined),
  seedSampleData: vi.fn().mockResolvedValue(undefined),
  seedInitialData: vi.fn().mockResolvedValue(undefined),
  getAllExpeditions: vi.fn().mockResolvedValue({ expeditions: [], total: 0 }),
  updateExpedition: vi.fn().mockResolvedValue(undefined),
  deleteExpedition: vi.fn().mockResolvedValue(undefined),
  getGuideFinancialInfoDecrypted: vi.fn(),
  getAuditLogsForEntity: vi.fn().mockResolvedValue([]),
  setGuidePixKeyStatus: vi.fn().mockResolvedValue(undefined),
  createAuditLog: vi.fn().mockResolvedValue(1),
  createPayout: vi.fn().mockResolvedValue(1),
  getGuideFinancialInfo: vi.fn(),
  getScheduledPayouts: vi.fn().mockResolvedValue([]),
  getPayoutById: vi.fn(),
  updatePayout: vi.fn().mockResolvedValue(undefined),
  getPlatformSetting: vi.fn().mockResolvedValue('3'),
  checkAndUpdatePaymentEligibility: vi.fn().mockResolvedValue({ eligible: true }),
}));

vi.mock('./lib/payout-service', () => ({
  executePayoutWithRetry: vi.fn().mockResolvedValue({ status: 'sent', transactionId: 'tx-test-123' }),
}));

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function createPublicContext(): TrpcContext {
  return {
    user: null,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: vi.fn(),
    } as unknown as TrpcContext["res"],
  };
}

function createUserContext(): TrpcContext {
  const user: AuthenticatedUser = {
    id: 1,
    openId: "test-user",
    email: "test@example.com",
    name: "Test User",
    loginMethod: "manus",
    role: "user",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  return {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: vi.fn(),
    } as unknown as TrpcContext["res"],
  };
}

function createAdminContext(): TrpcContext {
  const user: AuthenticatedUser = {
    id: 1,
    openId: "admin-user",
    email: "admin@example.com",
    name: "Admin User",
    loginMethod: "manus",
    role: "admin",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  return {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: vi.fn(),
    } as unknown as TrpcContext["res"],
  };
}

describe("admin.metrics", () => {
  it("denies access to unauthenticated users", async () => {
    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.admin.metrics()).rejects.toThrow();
  });

  it("denies access to regular users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.admin.metrics()).rejects.toThrow();
  });

  it("allows admin users to view metrics", async () => {
    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.admin.metrics();

    expect(result).toHaveProperty("trails");
    expect(result).toHaveProperty("expeditions");
    expect(result).toHaveProperty("guides");
    expect(result).toHaveProperty("reservations");
    expect(result).toHaveProperty("revenue");
  });
});

describe("admin.events", () => {
  it("denies access to unauthenticated users", async () => {
    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.admin.events({ limit: 10 })).rejects.toThrow();
  });

  it("denies access to regular users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.admin.events({ limit: 10 })).rejects.toThrow();
  });

  it("allows admin users to view events", async () => {
    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.admin.events({ limit: 10 });

    expect(Array.isArray(result)).toBe(true);
  });
});

describe("admin.seedData", () => {
  it("denies access to regular users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.admin.seedData()).rejects.toThrow();
  });

  it("allows admin users to seed data", async () => {
    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.admin.seedData();

    expect(result).toHaveProperty("success");
  });
});

describe("admin.expeditions", () => {
  it("denies list access to regular users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.admin.expeditions.list({ page: 1, limit: 10 })).rejects.toThrow();
  });

  it("allows admin to list expeditions", async () => {
    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.admin.expeditions.list({ page: 1, limit: 10 });

    expect(result).toHaveProperty("expeditions");
    expect(result).toHaveProperty("total");
  });
});

import * as db from "./db";
import * as payoutService from "./lib/payout-service";

// ---------------------------------------------------------------------------
// Story 8 — adminPayments.getGuidePixInfo (masked Pix key)
// ---------------------------------------------------------------------------
describe("adminPayments.getGuidePixInfo", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns masked Pix key for email type", async () => {
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue({
      id: 1,
      guideId: 5,
      pixKeyType: "email",
      pixKey: "guia@example.com",
      pixKeyHolderName: "Guia Teste",
      pixKeyVerified: 1,
      paymentEnabled: 1,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as any);

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.getGuidePixInfo({ guideId: 5 });

    expect(result).not.toBeNull();
    expect(result!.pixKey).toBe("****@example.com");
    expect(result!.pixKeyHolderName).toBe("Guia Teste");
  });

  it("returns null when guide has no financial info", async () => {
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue(undefined);

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.getGuidePixInfo({ guideId: 99 });

    expect(result).toBeNull();
  });

  it("masks CPF key correctly", async () => {
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue({
      id: 2,
      guideId: 5,
      pixKeyType: "cpf",
      pixKey: "52998224725",
      pixKeyHolderName: "João",
      pixKeyVerified: 1,
      paymentEnabled: 1,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as any);

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.getGuidePixInfo({ guideId: 5 });

    expect(result!.pixKey).toBe("***.***.***-25");
  });

  it("denies access to regular user", async () => {
    const caller = appRouter.createCaller(createUserContext());
    await expect(caller.adminPayments.getGuidePixInfo({ guideId: 5 })).rejects.toThrow();
  });
});

// ---------------------------------------------------------------------------
// Story 7 — adminPayments.getGuidePixAuditLog
// ---------------------------------------------------------------------------
describe("adminPayments.getGuidePixAuditLog", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns audit log entries for a guide", async () => {
    vi.mocked(db.getAuditLogsForEntity).mockResolvedValue([
      {
        id: 1,
        entityType: "guide_financial_info",
        entityId: 5,
        action: "pix_key_created",
        previousValue: null,
        newValue: JSON.stringify({ type: "email", key: "****@example.com" }),
        actorId: 5,
        actorType: "guide",
        source: "onboarding",
        createdAt: new Date("2026-01-01"),
      } as any,
    ]);

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.getGuidePixAuditLog({ guideId: 5 });

    expect(result).toHaveLength(1);
    expect(result[0].action).toBe("pix_key_created");
    expect(db.getAuditLogsForEntity).toHaveBeenCalledWith("guide_financial_info", 5);
  });

  it("returns empty array when no audit entries exist", async () => {
    vi.mocked(db.getAuditLogsForEntity).mockResolvedValue([]);

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.getGuidePixAuditLog({ guideId: 99 });

    expect(result).toHaveLength(0);
  });

  it("denies access to regular user", async () => {
    const caller = appRouter.createCaller(createUserContext());
    await expect(caller.adminPayments.getGuidePixAuditLog({ guideId: 5 })).rejects.toThrow();
  });
});

// ---------------------------------------------------------------------------
// Story 9 — adminPayments.setGuidePixKeyStatus (state machine)
// ---------------------------------------------------------------------------
describe("adminPayments.setGuidePixKeyStatus", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(db.setGuidePixKeyStatus).mockResolvedValue(undefined);
  });

  it("allows admin to set status to invalid", async () => {
    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.setGuidePixKeyStatus({
      guideId: 5,
      status: "invalid",
    });

    expect(result).toEqual({ success: true });
    expect(db.setGuidePixKeyStatus).toHaveBeenCalledWith(5, "invalid");
    expect(db.createAuditLog).toHaveBeenCalledWith(
      expect.objectContaining({
        entityType: "guide_financial_info",
        entityId: 5,
        action: "pix_key_status_set_invalid",
        actorType: "admin",
        source: "admin_portal",
      })
    );
    // Story 13: status change triggers eligibility re-check
    expect(db.checkAndUpdatePaymentEligibility).toHaveBeenCalledWith(5);
  });

  it("allows admin to set status to valid", async () => {
    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.setGuidePixKeyStatus({
      guideId: 5,
      status: "valid",
    });

    expect(result).toEqual({ success: true });
    expect(db.setGuidePixKeyStatus).toHaveBeenCalledWith(5, "valid");
  });

  it("allows admin to set status to pending", async () => {
    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.setGuidePixKeyStatus({
      guideId: 5,
      status: "pending",
    });

    expect(result).toEqual({ success: true });
    expect(db.setGuidePixKeyStatus).toHaveBeenCalledWith(5, "pending");
  });

  it("rejects unknown status values", async () => {
    const caller = appRouter.createCaller(createAdminContext());
    await expect(
      caller.adminPayments.setGuidePixKeyStatus({
        guideId: 5,
        status: "unknown" as any,
      })
    ).rejects.toThrow();
  });

  it("denies access to regular user", async () => {
    const caller = appRouter.createCaller(createUserContext());
    await expect(
      caller.adminPayments.setGuidePixKeyStatus({ guideId: 5, status: "invalid" })
    ).rejects.toThrow();
  });
});

// ---------------------------------------------------------------------------
// Story 10 — adminPayments.triggerPayout
// ---------------------------------------------------------------------------
describe("adminPayments.triggerPayout", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(db.getGuideFinancialInfo).mockResolvedValue({
      id: 1,
      guideId: 5,
      pixKeyType: "email",
      pixKey: "encrypted_guia@example.com",
      pixKeyHolderName: "Guia Teste",
      pixKeyStatus: "valid",
      pixKeyVerified: 1,
      paymentEnabled: 1,
      createdAt: new Date(),
      updatedAt: new Date(),
    } as any);
    vi.mocked(payoutService.executePayoutWithRetry).mockResolvedValue({
      status: "sent",
      transactionId: "tx-test-123",
    });
  });

  it("creates payout and executes it immediately", async () => {
    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.triggerPayout({
      guideId: 5,
      grossAmount: 1000,
      platformFeePercent: 10,
    });

    expect(result.status).toBe("sent");
    expect(result.transactionId).toBe("tx-test-123");
    expect(db.createPayout).toHaveBeenCalledWith(
      expect.objectContaining({
        guideId: 5,
        grossAmount: "1000",
        platformFee: "100",
        netAmount: "900",
        currency: "BRL",
      })
    );
    expect(payoutService.executePayoutWithRetry).toHaveBeenCalledWith(1);
  });

  it("throws when guide has no valid Pix key", async () => {
    vi.mocked(db.getGuideFinancialInfo).mockResolvedValue(undefined);

    const caller = appRouter.createCaller(createAdminContext());
    await expect(
      caller.adminPayments.triggerPayout({ guideId: 5, grossAmount: 1000 })
    ).rejects.toThrow("chave Pix válida");
  });

  it("throws when guide Pix key status is not valid", async () => {
    vi.mocked(db.getGuideFinancialInfo).mockResolvedValue({
      id: 1, guideId: 5, pixKeyType: "email",
      pixKey: "enc", pixKeyHolderName: "X",
      pixKeyStatus: "invalid",
    } as any);

    const caller = appRouter.createCaller(createAdminContext());
    await expect(
      caller.adminPayments.triggerPayout({ guideId: 5, grossAmount: 1000 })
    ).rejects.toThrow("chave Pix válida");
  });

  it("denies access to regular user", async () => {
    const caller = appRouter.createCaller(createUserContext());
    await expect(
      caller.adminPayments.triggerPayout({ guideId: 5, grossAmount: 1000 })
    ).rejects.toThrow();
  });
});

// ---------------------------------------------------------------------------
// Story 11 — adminPayments.retryPayout
// ---------------------------------------------------------------------------
describe("adminPayments.retryPayout", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(payoutService.executePayoutWithRetry).mockResolvedValue({
      status: "sent",
      transactionId: "tx-retry-ok",
    });
  });

  it("retries a payout and returns result", async () => {
    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.retryPayout({ payoutId: 101 });

    expect(result.status).toBe("sent");
    expect(payoutService.executePayoutWithRetry).toHaveBeenCalledWith(101);
    expect(db.createAuditLog).toHaveBeenCalledWith(
      expect.objectContaining({ action: "payout_manual_retry", actorType: "admin" })
    );
  });

  it("denies access to regular user", async () => {
    const caller = appRouter.createCaller(createUserContext());
    await expect(caller.adminPayments.retryPayout({ payoutId: 101 })).rejects.toThrow();
  });
});

// ---------------------------------------------------------------------------
// Story 11 — adminPayments.processScheduledPayouts
// ---------------------------------------------------------------------------
describe("adminPayments.processScheduledPayouts", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("processes all scheduled payouts and returns summary", async () => {
    vi.mocked(db.getScheduledPayouts).mockResolvedValue([
      { id: 1 } as any,
      { id: 2 } as any,
    ]);
    vi.mocked(payoutService.executePayoutWithRetry)
      .mockResolvedValueOnce({ status: "sent", transactionId: "tx-1" })
      .mockResolvedValueOnce({ status: "failed", error: "timeout" });

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.processScheduledPayouts();

    expect(result.total).toBe(2);
    expect(result.sent).toBe(1);
    expect(result.failed).toBe(1);
  });

  it("returns zero summary when no payouts are scheduled", async () => {
    vi.mocked(db.getScheduledPayouts).mockResolvedValue([]);

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.processScheduledPayouts();

    expect(result.total).toBe(0);
    expect(result.sent).toBe(0);
  });

  it("creates batch audit log entry", async () => {
    vi.mocked(db.getScheduledPayouts).mockResolvedValue([]);

    const caller = appRouter.createCaller(createAdminContext());
    await caller.adminPayments.processScheduledPayouts();

    expect(db.createAuditLog).toHaveBeenCalledWith(
      expect.objectContaining({ action: "batch_payouts_processed", actorType: "admin" })
    );
  });

  it("denies access to regular user", async () => {
    const caller = appRouter.createCaller(createUserContext());
    await expect(caller.adminPayments.processScheduledPayouts()).rejects.toThrow();
  });
});

// ---------------------------------------------------------------------------
// Story 13 — adminPayments.checkEligibility
// ---------------------------------------------------------------------------
describe("adminPayments.checkEligibility", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns eligible=true when guide has valid Pix and active profile", async () => {
    vi.mocked(db.checkAndUpdatePaymentEligibility).mockResolvedValue({ eligible: true });

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.checkEligibility({ guideId: 5 });

    expect(result.eligible).toBe(true);
    expect(db.checkAndUpdatePaymentEligibility).toHaveBeenCalledWith(5);
  });

  it("returns eligible=false with reason when Pix key is missing", async () => {
    vi.mocked(db.checkAndUpdatePaymentEligibility).mockResolvedValue({
      eligible: false,
      reason: "No Pix key configured",
    });

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.checkEligibility({ guideId: 5 });

    expect(result.eligible).toBe(false);
    expect(result.reason).toBe("No Pix key configured");
  });

  it("returns eligible=false when Pix key status is invalid", async () => {
    vi.mocked(db.checkAndUpdatePaymentEligibility).mockResolvedValue({
      eligible: false,
      reason: "Pix key status: invalid",
    });

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.checkEligibility({ guideId: 5 });

    expect(result.eligible).toBe(false);
    expect(result.reason).toContain("invalid");
  });

  it("returns eligible=false for archived account", async () => {
    vi.mocked(db.checkAndUpdatePaymentEligibility).mockResolvedValue({
      eligible: false,
      reason: "Account archived",
    });

    const caller = appRouter.createCaller(createAdminContext());
    const result = await caller.adminPayments.checkEligibility({ guideId: 5 });

    expect(result.eligible).toBe(false);
    expect(result.reason).toBe("Account archived");
  });

  it("denies access to regular user", async () => {
    const caller = appRouter.createCaller(createUserContext());
    await expect(caller.adminPayments.checkEligibility({ guideId: 5 })).rejects.toThrow();
  });
});
