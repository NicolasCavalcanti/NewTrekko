import { describe, expect, it, vi, beforeEach } from "vitest";

vi.mock("./db", () => ({
  getGuideVerificationDecrypted: vi.fn(),
}));

import * as db from "./db";
import { checkCpfPixKeyMismatch } from "./lib/fraud-detection";

const mockGetDecrypted = db.getGuideVerificationDecrypted as ReturnType<typeof vi.fn>;

describe("checkCpfPixKeyMismatch", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("does not flag non-CPF key types", async () => {
    const result = await checkCpfPixKeyMismatch(1, "email", "guide@example.com");
    expect(result.flagged).toBe(false);
    expect(mockGetDecrypted).not.toHaveBeenCalled();
  });

  it("does not flag when guide has no verification record", async () => {
    mockGetDecrypted.mockResolvedValue(undefined);
    const result = await checkCpfPixKeyMismatch(1, "cpf", "12345678901");
    expect(result.flagged).toBe(false);
  });

  it("does not flag when verification record has no documentNumber", async () => {
    mockGetDecrypted.mockResolvedValue({ documentNumber: undefined });
    const result = await checkCpfPixKeyMismatch(1, "cpf", "12345678901");
    expect(result.flagged).toBe(false);
  });

  it("does not flag when CPF digits match (formatted input)", async () => {
    mockGetDecrypted.mockResolvedValue({ documentNumber: "123.456.789-01" });
    const result = await checkCpfPixKeyMismatch(1, "cpf", "12345678901");
    expect(result.flagged).toBe(false);
  });

  it("does not flag when both CPFs have formatting but same digits", async () => {
    mockGetDecrypted.mockResolvedValue({ documentNumber: "123.456.789-01" });
    const result = await checkCpfPixKeyMismatch(1, "cpf", "123.456.789-01");
    expect(result.flagged).toBe(false);
  });

  it("flags when CPF digits differ", async () => {
    mockGetDecrypted.mockResolvedValue({ documentNumber: "111.111.111-11" });
    const result = await checkCpfPixKeyMismatch(1, "cpf", "99999999999");
    expect(result.flagged).toBe(true);
    expect(result.reason).toContain("CPF da chave Pix não corresponde");
  });

  it("flags even when formatting differs but digits clearly mismatch", async () => {
    mockGetDecrypted.mockResolvedValue({ documentNumber: "000.000.000-00" });
    const result = await checkCpfPixKeyMismatch(1, "cpf", "12345678901");
    expect(result.flagged).toBe(true);
  });

  it("does not flag cnpj key type (only CPF is checked)", async () => {
    const result = await checkCpfPixKeyMismatch(1, "cnpj", "12345678000190");
    expect(result.flagged).toBe(false);
    expect(mockGetDecrypted).not.toHaveBeenCalled();
  });

  it("does not flag phone key type", async () => {
    const result = await checkCpfPixKeyMismatch(1, "phone", "+5511999999999");
    expect(result.flagged).toBe(false);
  });

  it("does not flag random key type", async () => {
    const result = await checkCpfPixKeyMismatch(1, "random", "some-uuid-key");
    expect(result.flagged).toBe(false);
  });
});
