import { describe, expect, it, vi, beforeEach } from "vitest";

vi.mock("./_core/sdk", () => ({
  sdk: { authenticateRequest: vi.fn() },
}));

vi.mock("./db", () => ({
  getGuideFinancialInfoDecrypted: vi.fn(),
  getGuideFinancialInfo: vi.fn(),
  saveGuideFinancialInfo: vi.fn(),
  updateGuideFinancialInfo: vi.fn(),
  setGuidePixKeyStatus: vi.fn(),
  createAuditLog: vi.fn().mockResolvedValue(1),
  checkAndUpdatePaymentEligibility: vi.fn().mockResolvedValue({ eligible: true }),
}));

vi.mock("./lib/fraud-detection", () => ({
  checkCpfPixKeyMismatch: vi.fn().mockResolvedValue({ flagged: false }),
}));

import { sdk } from "./_core/sdk";
import * as db from "./db";
import { checkCpfPixKeyMismatch } from "./lib/fraud-detection";
import {
  getFinancialInfo,
  createFinancialInfo,
  updateFinancialInfo,
} from "./routes/financial-info";
import type { Request, Response } from "express";

const mockAuth = sdk.authenticateRequest as ReturnType<typeof vi.fn>;
const mockGetDecrypted = db.getGuideFinancialInfoDecrypted as ReturnType<typeof vi.fn>;
const mockGetInfo = db.getGuideFinancialInfo as ReturnType<typeof vi.fn>;
const mockSave = db.saveGuideFinancialInfo as ReturnType<typeof vi.fn>;
const mockUpdate = db.updateGuideFinancialInfo as ReturnType<typeof vi.fn>;
const mockSetStatus = db.setGuidePixKeyStatus as ReturnType<typeof vi.fn>;
const mockCreateAudit = db.createAuditLog as ReturnType<typeof vi.fn>;
const mockFraud = checkCpfPixKeyMismatch as ReturnType<typeof vi.fn>;

function makeRes(): Response {
  const res: any = {};
  res.status = vi.fn().mockReturnValue(res);
  res.json = vi.fn().mockReturnValue(res);
  return res;
}

function req(override: Partial<Request> = {}): Request {
  return { headers: {}, params: {}, body: {}, query: {}, ...override } as unknown as Request;
}

const guideUser = {
  id: 2,
  openId: "guide-1",
  role: "user",
  userType: "guide",
  email: "guide@example.com",
  name: "Guide",
  loginMethod: "email",
  cadasturNumber: null,
  cadasturValidated: 0,
  bio: null,
  photoUrl: null,
  createdAt: new Date(),
  updatedAt: new Date(),
  lastSignedIn: new Date(),
  passwordHash: null,
  archivedAt: null,
};

const adminUser = { ...guideUser, id: 1, role: "admin", userType: "trekker" };

const sampleFinancialInfo = {
  id: 10,
  guideId: 2,
  pixKeyType: "email",
  pixKey: "guide@example.com",
  pixKeyHolderName: "Guide User",
  pixKeyStatus: "valid",
  pixKeyVerified: 1,
  paymentEnabled: 1,
  createdAt: new Date(),
  updatedAt: new Date(),
};

beforeEach(() => {
  vi.clearAllMocks();
  mockFraud.mockResolvedValue({ flagged: false });
  mockGetInfo.mockResolvedValue({ pixKeyStatus: "valid", paymentEnabled: 1 });
  (db.checkAndUpdatePaymentEligibility as ReturnType<typeof vi.fn>).mockResolvedValue({ eligible: true });
});

// ─── GET /api/financial-info/:guide_id ────────────────────────────────────────

describe("GET /api/financial-info/:guide_id", () => {
  it("returns 401 when not authenticated", async () => {
    mockAuth.mockRejectedValue(new Error("Unauthorized"));
    const res = makeRes();
    await getFinancialInfo(req({ params: { guide_id: "2" } as any }), res);
    expect(res.status).toHaveBeenCalledWith(401);
  });

  it("returns 400 for non-numeric guide_id", async () => {
    mockAuth.mockResolvedValue(adminUser);
    const res = makeRes();
    await getFinancialInfo(req({ params: { guide_id: "abc" } as any }), res);
    expect(res.status).toHaveBeenCalledWith(400);
  });

  it("returns 403 when guide requests another guide's info", async () => {
    mockAuth.mockResolvedValue(guideUser); // id=2
    const res = makeRes();
    await getFinancialInfo(req({ params: { guide_id: "99" } as any }), res);
    expect(res.status).toHaveBeenCalledWith(403);
  });

  it("returns 404 when no financial info exists", async () => {
    mockAuth.mockResolvedValue(guideUser);
    mockGetDecrypted.mockResolvedValue(undefined);
    const res = makeRes();
    await getFinancialInfo(req({ params: { guide_id: "2" } as any }), res);
    expect(res.status).toHaveBeenCalledWith(404);
  });

  it("returns masked info for guide viewing their own record", async () => {
    mockAuth.mockResolvedValue(guideUser);
    mockGetDecrypted.mockResolvedValue(sampleFinancialInfo);
    const res = makeRes();
    await getFinancialInfo(req({ params: { guide_id: "2" } as any }), res);
    expect(res.json).toHaveBeenCalledWith(
      expect.objectContaining({
        guideId: 2,
        pixKeyType: "email",
        pixKey: expect.stringContaining("****@"),
        pixKeyStatus: "valid",
      })
    );
  });

  it("allows admin to view any guide's info", async () => {
    mockAuth.mockResolvedValue(adminUser); // id=1, viewing guideId=2
    mockGetDecrypted.mockResolvedValue(sampleFinancialInfo);
    const res = makeRes();
    await getFinancialInfo(req({ params: { guide_id: "2" } as any }), res);
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ guideId: 2 }));
  });
});

// ─── POST /api/financial-info ─────────────────────────────────────────────────

describe("POST /api/financial-info", () => {
  it("returns 401 when unauthenticated", async () => {
    mockAuth.mockRejectedValue(new Error("Unauthorized"));
    const res = makeRes();
    await createFinancialInfo(req(), res);
    expect(res.status).toHaveBeenCalledWith(401);
  });

  it("returns 403 for non-guide user", async () => {
    mockAuth.mockResolvedValue(adminUser); // userType='trekker'
    const res = makeRes();
    await createFinancialInfo(req(), res);
    expect(res.status).toHaveBeenCalledWith(403);
  });

  it("returns 400 when required fields are missing", async () => {
    mockAuth.mockResolvedValue(guideUser);
    const res = makeRes();
    await createFinancialInfo(req({ body: { pixKeyType: "email" } }), res);
    expect(res.status).toHaveBeenCalledWith(400);
  });

  it("returns 400 for invalid pixKeyType", async () => {
    mockAuth.mockResolvedValue(guideUser);
    const res = makeRes();
    await createFinancialInfo(
      req({ body: { pixKeyType: "bitcoin", pixKey: "abc", pixKeyHolderName: "X" } }),
      res,
    );
    expect(res.status).toHaveBeenCalledWith(400);
  });

  it("saves info and returns 201 on success (no fraud)", async () => {
    mockAuth.mockResolvedValue(guideUser);
    mockSave.mockResolvedValue(undefined);
    const res = makeRes();
    await createFinancialInfo(
      req({ body: { pixKeyType: "email", pixKey: "g@e.com", pixKeyHolderName: "Guide" } }),
      res,
    );
    expect(mockSave).toHaveBeenCalledWith(2, expect.objectContaining({ pixKeyType: "email" }));
    expect(res.status).toHaveBeenCalledWith(201);
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ success: true, flagged: false }));
  });

  it("flags and downgrades status on CPF mismatch", async () => {
    mockAuth.mockResolvedValue(guideUser);
    mockSave.mockResolvedValue(undefined);
    mockFraud.mockResolvedValue({
      flagged: true,
      reason: "CPF da chave Pix não corresponde ao CPF cadastrado no perfil.",
    });
    const res = makeRes();
    await createFinancialInfo(
      req({ body: { pixKeyType: "cpf", pixKey: "11111111111", pixKeyHolderName: "Guide" } }),
      res,
    );
    expect(mockSetStatus).toHaveBeenCalledWith(2, "pending");
    expect(mockCreateAudit).toHaveBeenCalledWith(
      expect.objectContaining({ action: "pix_cpf_mismatch", source: "fraud_detection" }),
    );
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ flagged: true }));
  });
});

// ─── PATCH /api/financial-info ────────────────────────────────────────────────

describe("PATCH /api/financial-info", () => {
  it("returns 401 when unauthenticated", async () => {
    mockAuth.mockRejectedValue(new Error("Unauthorized"));
    const res = makeRes();
    await updateFinancialInfo(req(), res);
    expect(res.status).toHaveBeenCalledWith(401);
  });

  it("returns 403 for non-guide user", async () => {
    mockAuth.mockResolvedValue(adminUser);
    const res = makeRes();
    await updateFinancialInfo(req(), res);
    expect(res.status).toHaveBeenCalledWith(403);
  });

  it("returns 400 when required fields are missing", async () => {
    mockAuth.mockResolvedValue(guideUser);
    const res = makeRes();
    await updateFinancialInfo(req({ body: { pixKeyType: "email" } }), res);
    expect(res.status).toHaveBeenCalledWith(400);
  });

  it("returns 404 when no existing record (db throws)", async () => {
    mockAuth.mockResolvedValue(guideUser);
    mockUpdate.mockRejectedValue(new Error("Nenhuma chave PIX cadastrada"));
    const res = makeRes();
    await updateFinancialInfo(
      req({ body: { pixKeyType: "email", pixKey: "g@e.com", pixKeyHolderName: "G" } }),
      res,
    );
    expect(res.status).toHaveBeenCalledWith(404);
  });

  it("updates info and returns 200 on success (no fraud)", async () => {
    mockAuth.mockResolvedValue(guideUser);
    mockUpdate.mockResolvedValue(undefined);
    const res = makeRes();
    await updateFinancialInfo(
      req({ body: { pixKeyType: "phone", pixKey: "11999999999", pixKeyHolderName: "Guide" } }),
      res,
    );
    expect(mockUpdate).toHaveBeenCalledWith(2, expect.objectContaining({ pixKeyType: "phone" }));
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ success: true, flagged: false }));
  });

  it("flags and downgrades status on CPF mismatch during update", async () => {
    mockAuth.mockResolvedValue(guideUser);
    mockUpdate.mockResolvedValue(undefined);
    mockFraud.mockResolvedValue({
      flagged: true,
      reason: "CPF da chave Pix não corresponde ao CPF cadastrado no perfil.",
    });
    const res = makeRes();
    await updateFinancialInfo(
      req({ body: { pixKeyType: "cpf", pixKey: "22222222222", pixKeyHolderName: "Guide" } }),
      res,
    );
    expect(mockSetStatus).toHaveBeenCalledWith(2, "pending");
    expect(mockCreateAudit).toHaveBeenCalledWith(
      expect.objectContaining({ action: "pix_cpf_mismatch" }),
    );
    expect(res.json).toHaveBeenCalledWith(expect.objectContaining({ flagged: true }));
  });
});
