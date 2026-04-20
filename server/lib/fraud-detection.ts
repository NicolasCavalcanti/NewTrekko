import * as db from "../db";

function normalizeDigits(v: string): string {
  return v.replace(/\D/g, "");
}

/**
 * Story 15: Compare a CPF-type Pix key against the guide's registered CPF.
 * Returns flagged=true when the digits don't match.
 * Non-CPF key types always return flagged=false (nothing to compare).
 * Missing verification record → not flagged (guide hasn't submitted CPF yet).
 */
export async function checkCpfPixKeyMismatch(
  guideId: number,
  pixKeyType: string,
  pixKey: string,
): Promise<{ flagged: boolean; reason?: string }> {
  if (pixKeyType !== "cpf") return { flagged: false };

  const verification = await db.getGuideVerificationDecrypted(guideId);
  if (!verification?.documentNumber) return { flagged: false };

  const storedCpf = normalizeDigits(verification.documentNumber);
  const submittedCpf = normalizeDigits(pixKey);

  if (storedCpf !== submittedCpf) {
    return {
      flagged: true,
      reason: "CPF da chave Pix não corresponde ao CPF cadastrado no perfil.",
    };
  }

  return { flagged: false };
}
