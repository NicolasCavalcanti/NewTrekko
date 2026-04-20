import { Router, Request, Response } from "express";
import { sdk } from "../_core/sdk";
import * as db from "../db";
import { maskPixKey } from "../lib/pix-validation";
import { checkCpfPixKeyMismatch } from "../lib/fraud-detection";

const VALID_PIX_TYPES = ["cpf", "cnpj", "email", "phone", "random"] as const;
type PixKeyType = (typeof VALID_PIX_TYPES)[number];

function isValidPixType(v: unknown): v is PixKeyType {
  return VALID_PIX_TYPES.includes(v as PixKeyType);
}

// GET /api/financial-info/:guide_id
export async function getFinancialInfo(req: Request, res: Response) {
  let user;
  try {
    user = await sdk.authenticateRequest(req);
  } catch {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const guideId = parseInt(req.params.guide_id, 10);
  if (isNaN(guideId)) return res.status(400).json({ error: "Invalid guide_id" });

  if (user.role !== "admin" && user.id !== guideId) {
    return res.status(403).json({ error: "Forbidden" });
  }

  const info = await db.getGuideFinancialInfoDecrypted(guideId);
  if (!info) return res.status(404).json({ error: "Not found" });

  const maskedKey =
    info.pixKey && info.pixKeyType
      ? maskPixKey(info.pixKeyType as PixKeyType, info.pixKey)
      : null;

  return res.json({
    id: info.id,
    guideId: info.guideId,
    pixKeyType: info.pixKeyType,
    pixKey: maskedKey,
    pixKeyHolderName: info.pixKeyHolderName,
    pixKeyStatus: info.pixKeyStatus,
    paymentEnabled: info.paymentEnabled,
    createdAt: info.createdAt,
    updatedAt: info.updatedAt,
  });
}

// POST /api/financial-info
export async function createFinancialInfo(req: Request, res: Response) {
  let user;
  try {
    user = await sdk.authenticateRequest(req);
  } catch {
    return res.status(401).json({ error: "Unauthorized" });
  }

  if (user.userType !== "guide") {
    return res.status(403).json({ error: "Apenas guias podem cadastrar informações financeiras." });
  }

  const { pixKeyType, pixKey, pixKeyHolderName } = req.body ?? {};
  if (!pixKeyType || !pixKey || !pixKeyHolderName) {
    return res.status(400).json({ error: "pixKeyType, pixKey e pixKeyHolderName são obrigatórios." });
  }
  if (!isValidPixType(pixKeyType)) {
    return res.status(400).json({ error: "Tipo de chave Pix inválido." });
  }

  try {
    await db.saveGuideFinancialInfo(user.id, { pixKeyType, pixKey, pixKeyHolderName });

    const fraud = await checkCpfPixKeyMismatch(user.id, pixKeyType, pixKey);
    if (fraud.flagged) {
      await db.setGuidePixKeyStatus(user.id, "pending");
      await db.createAuditLog({
        entityType: "guide_financial_info",
        entityId: user.id,
        action: "pix_cpf_mismatch",
        payload: { reason: fraud.reason },
        source: "fraud_detection",
      });
    }

    await db.checkAndUpdatePaymentEligibility(user.id);
    const info = await db.getGuideFinancialInfo(user.id);

    return res.status(201).json({
      success: true,
      pixKeyStatus: info?.pixKeyStatus,
      paymentEnabled: info?.paymentEnabled,
      flagged: fraud.flagged,
    });
  } catch (err: any) {
    return res.status(500).json({ error: err.message ?? "Internal server error" });
  }
}

// PATCH /api/financial-info
export async function updateFinancialInfo(req: Request, res: Response) {
  let user;
  try {
    user = await sdk.authenticateRequest(req);
  } catch {
    return res.status(401).json({ error: "Unauthorized" });
  }

  if (user.userType !== "guide") {
    return res.status(403).json({ error: "Apenas guias podem atualizar informações financeiras." });
  }

  const { pixKeyType, pixKey, pixKeyHolderName } = req.body ?? {};
  if (!pixKeyType || !pixKey || !pixKeyHolderName) {
    return res.status(400).json({ error: "pixKeyType, pixKey e pixKeyHolderName são obrigatórios." });
  }
  if (!isValidPixType(pixKeyType)) {
    return res.status(400).json({ error: "Tipo de chave Pix inválido." });
  }

  try {
    await db.updateGuideFinancialInfo(user.id, { pixKeyType, pixKey, pixKeyHolderName });

    const fraud = await checkCpfPixKeyMismatch(user.id, pixKeyType, pixKey);
    if (fraud.flagged) {
      await db.setGuidePixKeyStatus(user.id, "pending");
      await db.createAuditLog({
        entityType: "guide_financial_info",
        entityId: user.id,
        action: "pix_cpf_mismatch",
        payload: { reason: fraud.reason },
        source: "fraud_detection",
      });
    }

    await db.checkAndUpdatePaymentEligibility(user.id);
    const info = await db.getGuideFinancialInfo(user.id);

    return res.json({
      success: true,
      pixKeyStatus: info?.pixKeyStatus,
      paymentEnabled: info?.paymentEnabled,
      flagged: fraud.flagged,
    });
  } catch (err: any) {
    if (err.message?.includes("Nenhuma chave PIX")) {
      return res.status(404).json({ error: err.message });
    }
    return res.status(500).json({ error: err.message ?? "Internal server error" });
  }
}

const router = Router();
router.get("/:guide_id", getFinancialInfo);
router.post("/", createFinancialInfo);
router.patch("/", updateFinancialInfo);

export { router as financialInfoRouter };
