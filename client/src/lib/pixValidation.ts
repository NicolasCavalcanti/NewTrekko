export type PixKeyType = "cpf" | "cnpj" | "email" | "phone" | "random";

export function isValidCPF(cpf: string): boolean {
  const digits = cpf.replace(/\D/g, "");
  if (digits.length !== 11) return false;
  if (/^(\d)\1{10}$/.test(digits)) return false;

  let sum = 0;
  for (let i = 0; i < 9; i++) sum += parseInt(digits[i]) * (10 - i);
  let rem = (sum * 10) % 11;
  if (rem === 10 || rem === 11) rem = 0;
  if (rem !== parseInt(digits[9])) return false;

  sum = 0;
  for (let i = 0; i < 10; i++) sum += parseInt(digits[i]) * (11 - i);
  rem = (sum * 10) % 11;
  if (rem === 10 || rem === 11) rem = 0;
  return rem === parseInt(digits[10]);
}

export function isValidCNPJ(cnpj: string): boolean {
  const digits = cnpj.replace(/\D/g, "");
  if (digits.length !== 14) return false;
  if (/^(\d)\1{13}$/.test(digits)) return false;

  const w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];
  const w2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2];

  let sum = 0;
  for (let i = 0; i < 12; i++) sum += parseInt(digits[i]) * w1[i];
  let rem = sum % 11 < 2 ? 0 : 11 - (sum % 11);
  if (rem !== parseInt(digits[12])) return false;

  sum = 0;
  for (let i = 0; i < 13; i++) sum += parseInt(digits[i]) * w2[i];
  rem = sum % 11 < 2 ? 0 : 11 - (sum % 11);
  return rem === parseInt(digits[13]);
}

export function validatePixKey(type: PixKeyType, value: string): string {
  if (!value.trim()) return "Chave Pix é obrigatória";

  const digits = value.replace(/\D/g, "");

  switch (type) {
    case "cpf":
      if (digits.length !== 11) return "CPF deve ter 11 dígitos";
      if (!isValidCPF(digits)) return "CPF inválido";
      return "";

    case "cnpj":
      if (digits.length !== 14) return "CNPJ deve ter 14 dígitos";
      if (!isValidCNPJ(digits)) return "CNPJ inválido";
      return "";

    case "email": {
      const normalized = value.trim().toLowerCase();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalized)) return "E-mail inválido";
      return "";
    }

    case "phone":
      if (digits.length !== 11)
        return "Telefone deve ter 11 dígitos com DDD (ex: 11999999999)";
      if (digits[2] !== "9")
        return "Telefone deve ser celular com 9 dígitos após o DDD";
      return "";

    case "random":
      if (
        !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(
          value.trim()
        )
      )
        return "Chave aleatória inválida. Use o formato UUID fornecido pelo seu banco.";
      return "";
  }
}

export function normalizePixKey(type: PixKeyType, value: string): string {
  switch (type) {
    case "cpf":
    case "cnpj":
    case "phone":
      return value.replace(/\D/g, "");
    case "email":
      return value.trim().toLowerCase();
    case "random":
      return value.trim().toLowerCase();
  }
}

export function formatCPF(value: string): string {
  const n = value.replace(/\D/g, "").slice(0, 11);
  return n
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}

export function formatCNPJ(value: string): string {
  const n = value.replace(/\D/g, "").slice(0, 14);
  return n
    .replace(/(\d{2})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1.$2")
    .replace(/(\d{3})(\d)/, "$1/$2")
    .replace(/(\d{4})(\d{1,2})$/, "$1-$2");
}

export function formatPhone(value: string): string {
  const n = value.replace(/\D/g, "").slice(0, 11);
  return n
    .replace(/(\d{2})(\d)/, "($1) $2")
    .replace(/(\d{5})(\d{1,4})$/, "$1-$2");
}

export function formatPixKeyValue(value: string, type: PixKeyType): string {
  switch (type) {
    case "cpf":
      return formatCPF(value);
    case "cnpj":
      return formatCNPJ(value);
    case "phone":
      return formatPhone(value);
    default:
      return value;
  }
}

export function getPixKeyPlaceholder(type: PixKeyType): string {
  switch (type) {
    case "cpf":
      return "000.000.000-00";
    case "cnpj":
      return "00.000.000/0000-00";
    case "email":
      return "seu@email.com";
    case "phone":
      return "(00) 00000-0000";
    case "random":
      return "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx";
  }
}
