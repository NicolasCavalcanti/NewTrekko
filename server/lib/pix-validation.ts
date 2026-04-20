export type PixKeyType = 'cpf' | 'cnpj' | 'email' | 'phone' | 'random';

export function validateCPF(cpf: string): { valid: boolean; error?: string } {
  const digits = cpf.replace(/\D/g, '');
  if (digits.length !== 11) return { valid: false, error: 'CPF deve ter 11 dígitos' };
  // Reject sequences of identical digits (e.g. "00000000000")
  if (/^(\d)\1{10}$/.test(digits)) return { valid: false, error: 'CPF inválido' };

  let sum = 0;
  for (let i = 0; i < 9; i++) sum += parseInt(digits[i]) * (10 - i);
  let rem = sum % 11;
  if (parseInt(digits[9]) !== (rem < 2 ? 0 : 11 - rem)) return { valid: false, error: 'CPF inválido' };

  sum = 0;
  for (let i = 0; i < 10; i++) sum += parseInt(digits[i]) * (11 - i);
  rem = sum % 11;
  if (parseInt(digits[10]) !== (rem < 2 ? 0 : 11 - rem)) return { valid: false, error: 'CPF inválido' };

  return { valid: true };
}

export function validateCNPJ(cnpj: string): { valid: boolean; error?: string } {
  const digits = cnpj.replace(/\D/g, '');
  if (digits.length !== 14) return { valid: false, error: 'CNPJ deve ter 14 dígitos' };
  if (/^(\d)\1{13}$/.test(digits)) return { valid: false, error: 'CNPJ inválido' };

  const checkDigit = (d: string, weights: number[]) => {
    let sum = 0;
    for (let i = 0; i < weights.length; i++) sum += parseInt(d[i]) * weights[i];
    const rem = sum % 11;
    return rem < 2 ? 0 : 11 - rem;
  };

  if (parseInt(digits[12]) !== checkDigit(digits, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])) {
    return { valid: false, error: 'CNPJ inválido' };
  }
  if (parseInt(digits[13]) !== checkDigit(digits, [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])) {
    return { valid: false, error: 'CNPJ inválido' };
  }

  return { valid: true };
}

export function validatePixKey(pixKeyType: PixKeyType, pixKey: string): { valid: boolean; error?: string } {
  if (!pixKey || !pixKey.trim()) return { valid: false, error: 'Chave PIX é obrigatória' };

  switch (pixKeyType) {
    case 'cpf':
      return validateCPF(pixKey);
    case 'cnpj':
      return validateCNPJ(pixKey);
    case 'email': {
      const trimmed = pixKey.trim();
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed)) {
        return { valid: false, error: 'E-mail inválido' };
      }
      return { valid: true };
    }
    case 'phone': {
      const digits = pixKey.replace(/\D/g, '');
      if (digits.length < 10 || digits.length > 11) {
        return { valid: false, error: 'Telefone deve ter 10 ou 11 dígitos (DDD + número)' };
      }
      return { valid: true };
    }
    case 'random':
      return { valid: true };
    default:
      return { valid: false, error: 'Tipo de chave PIX inválido' };
  }
}

export function normalizePixKey(pixKeyType: PixKeyType, pixKey: string): string {
  switch (pixKeyType) {
    case 'cpf':
    case 'cnpj':
    case 'phone':
      return pixKey.replace(/\D/g, '');
    case 'email':
      return pixKey.trim().toLowerCase();
    case 'random':
      return pixKey.trim();
    default:
      return pixKey;
  }
}

// Story 8: Mask Pix key for safe display (LGPD compliance).
// Accepts the plaintext normalized value; never pass ciphertext.
export function maskPixKey(pixKeyType: PixKeyType, value: string): string {
  if (!value || !value.trim()) return '****';
  switch (pixKeyType) {
    case 'email': {
      const atIdx = value.indexOf('@');
      if (atIdx < 0) return '****';
      return `****@${value.slice(atIdx + 1)}`;
    }
    case 'cpf': {
      const d = value.replace(/\D/g, '');
      const suffix = d.length >= 11 ? d.slice(9, 11) : d.slice(-2).padStart(2, '*');
      return `***.***.***-${suffix}`;
    }
    case 'cnpj': {
      const d = value.replace(/\D/g, '');
      const suffix = d.length >= 14 ? d.slice(12, 14) : d.slice(-2).padStart(2, '*');
      return `**.***.****/****-${suffix}`;
    }
    case 'phone': {
      const d = value.replace(/\D/g, '');
      const suffix = d.length >= 4 ? d.slice(-4) : d.padStart(4, '*');
      return `(**) *****-${suffix}`;
    }
    case 'random':
      return value.length > 4 ? `${value.slice(0, 4)}****` : '****';
    default:
      return '****';
  }
}
