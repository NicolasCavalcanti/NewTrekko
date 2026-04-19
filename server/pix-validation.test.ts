import { describe, expect, it } from "vitest";
import { validateCPF, validateCNPJ, validatePixKey, normalizePixKey } from "./lib/pix-validation";

// Well-known valid CPFs for testing (generated with mod-11 algorithm)
const VALID_CPF = "529.982.247-25";
const VALID_CPF_DIGITS = "52998224725";
const VALID_CNPJ = "11.222.333/0001-81";
const VALID_CNPJ_DIGITS = "11222333000181";

describe("validateCPF", () => {
  it("accepts a valid CPF with formatting", () => {
    expect(validateCPF(VALID_CPF)).toEqual({ valid: true });
  });

  it("accepts a valid CPF without formatting", () => {
    expect(validateCPF(VALID_CPF_DIGITS)).toEqual({ valid: true });
  });

  it("rejects CPF with too few digits", () => {
    const result = validateCPF("123456789");
    expect(result.valid).toBe(false);
    expect(result.error).toContain("11 dígitos");
  });

  it("rejects CPF with too many digits", () => {
    const result = validateCPF("123456789012");
    expect(result.valid).toBe(false);
  });

  it("rejects CPF with all identical digits", () => {
    const result = validateCPF("11111111111");
    expect(result.valid).toBe(false);
    expect(result.error).toContain("inválido");
  });

  it("rejects CPF with wrong check digits", () => {
    const result = validateCPF("52998224700"); // last two digits tampered
    expect(result.valid).toBe(false);
    expect(result.error).toContain("inválido");
  });

  it("rejects an empty string", () => {
    expect(validateCPF("").valid).toBe(false);
  });
});

describe("validateCNPJ", () => {
  it("accepts a valid CNPJ with formatting", () => {
    expect(validateCNPJ(VALID_CNPJ)).toEqual({ valid: true });
  });

  it("accepts a valid CNPJ without formatting", () => {
    expect(validateCNPJ(VALID_CNPJ_DIGITS)).toEqual({ valid: true });
  });

  it("rejects CNPJ with too few digits", () => {
    const result = validateCNPJ("1234567890123");
    expect(result.valid).toBe(false);
    expect(result.error).toContain("14 dígitos");
  });

  it("rejects CNPJ with all identical digits", () => {
    const result = validateCNPJ("00000000000000");
    expect(result.valid).toBe(false);
    expect(result.error).toContain("inválido");
  });

  it("rejects CNPJ with wrong check digits", () => {
    const result = validateCNPJ("11222333000100"); // check digits tampered
    expect(result.valid).toBe(false);
    expect(result.error).toContain("inválido");
  });
});

describe("validatePixKey", () => {
  it("accepts valid CPF key", () => {
    expect(validatePixKey("cpf", VALID_CPF)).toEqual({ valid: true });
  });

  it("rejects invalid CPF key", () => {
    const result = validatePixKey("cpf", "111.111.111-11");
    expect(result.valid).toBe(false);
  });

  it("accepts valid CNPJ key", () => {
    expect(validatePixKey("cnpj", VALID_CNPJ)).toEqual({ valid: true });
  });

  it("rejects invalid CNPJ key", () => {
    const result = validatePixKey("cnpj", "00.000.000/0000-00");
    expect(result.valid).toBe(false);
  });

  it("accepts valid email key", () => {
    expect(validatePixKey("email", "guia@example.com")).toEqual({ valid: true });
  });

  it("rejects malformed email key", () => {
    const result = validatePixKey("email", "not-an-email");
    expect(result.valid).toBe(false);
    expect(result.error).toContain("inválido");
  });

  it("accepts valid phone key (11 digits)", () => {
    expect(validatePixKey("phone", "11987654321")).toEqual({ valid: true });
  });

  it("accepts valid phone key (10 digits)", () => {
    expect(validatePixKey("phone", "1132165478")).toEqual({ valid: true });
  });

  it("accepts formatted phone key", () => {
    expect(validatePixKey("phone", "(11) 98765-4321")).toEqual({ valid: true });
  });

  it("rejects phone key with too few digits", () => {
    const result = validatePixKey("phone", "123456789");
    expect(result.valid).toBe(false);
    expect(result.error).toContain("dígitos");
  });

  it("accepts random key", () => {
    expect(validatePixKey("random", "a1b2c3d4-e5f6-7890-abcd-ef1234567890")).toEqual({ valid: true });
  });

  it("rejects empty Pix key regardless of type", () => {
    expect(validatePixKey("email", "").valid).toBe(false);
    expect(validatePixKey("random", "   ").valid).toBe(false);
  });
});

describe("normalizePixKey", () => {
  it("strips formatting from CPF", () => {
    expect(normalizePixKey("cpf", "529.982.247-25")).toBe("52998224725");
  });

  it("strips formatting from CNPJ", () => {
    expect(normalizePixKey("cnpj", "11.222.333/0001-81")).toBe("11222333000181");
  });

  it("strips formatting from phone", () => {
    expect(normalizePixKey("phone", "(11) 98765-4321")).toBe("11987654321");
  });

  it("lowercases and trims email", () => {
    expect(normalizePixKey("email", "  Guia@Example.COM  ")).toBe("guia@example.com");
  });

  it("trims random key", () => {
    expect(normalizePixKey("random", "  abc-123  ")).toBe("abc-123");
  });
});
