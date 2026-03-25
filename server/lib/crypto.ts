/**
 * DB-SEC-01: AES-256-GCM field-level encryption for sensitive PII columns.
 *
 * Usage:
 *   import { encrypt, decrypt } from './crypto';
 *
 *   // Before writing to DB:
 *   const encryptedPix = encrypt(plainTextPixKey);
 *
 *   // After reading from DB:
 *   const plainTextPix = decrypt(encryptedPix);
 *
 * Key requirement: DB_ENCRYPTION_KEY env var must be a 64-character hex string
 * (= 32 bytes = 256 bits).  Generate with:
 *   node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
 *
 * Ciphertext format stored in the database:
 *   <iv-hex>:<authTag-hex>:<ciphertext-hex>
 * This self-contained format means each encrypted value carries its own IV,
 * so no IV-reuse issues even if the same plaintext is encrypted twice.
 */

import { createCipheriv, createDecipheriv, randomBytes } from "node:crypto";

const ALGORITHM = "aes-256-gcm";
const IV_BYTES = 12; // 96-bit IV recommended for GCM
const TAG_BYTES = 16;
const SEPARATOR = ":";

function getKey(): Buffer {
  const hex = process.env.DB_ENCRYPTION_KEY;
  if (!hex || hex.length !== 64) {
    throw new Error(
      "DB_ENCRYPTION_KEY must be set to a 64-character hex string (32 bytes). " +
      "Generate one with: node -e \"console.log(require('crypto').randomBytes(32).toString('hex'))\""
    );
  }
  return Buffer.from(hex, "hex");
}

/**
 * Encrypts a plaintext string using AES-256-GCM.
 * Returns a colon-delimited string: iv:authTag:ciphertext (all hex-encoded).
 * Returns null when value is null or undefined.
 */
export function encrypt(value: string | null | undefined): string | null {
  if (value == null) return null;

  const key = getKey();
  const iv = randomBytes(IV_BYTES);
  const cipher = createCipheriv(ALGORITHM, key, iv);

  const ciphertext = Buffer.concat([cipher.update(value, "utf8"), cipher.final()]);
  const authTag = cipher.getAuthTag();

  return [iv.toString("hex"), authTag.toString("hex"), ciphertext.toString("hex")].join(SEPARATOR);
}

/**
 * Decrypts a ciphertext string produced by encrypt().
 * Returns the original plaintext, or null if the input is null.
 * Throws if authentication tag verification fails (tampered data).
 */
export function decrypt(ciphertext: string | null | undefined): string | null {
  if (ciphertext == null) return null;

  const parts = ciphertext.split(SEPARATOR);
  if (parts.length !== 3) {
    throw new Error("Invalid ciphertext format — expected iv:authTag:ciphertext");
  }

  const [ivHex, tagHex, ctHex] = parts;
  const key = getKey();
  const iv = Buffer.from(ivHex, "hex");
  const authTag = Buffer.from(tagHex, "hex");
  const ct = Buffer.from(ctHex, "hex");

  if (iv.length !== IV_BYTES) {
    throw new Error("Invalid IV length in ciphertext");
  }
  if (authTag.length !== TAG_BYTES) {
    throw new Error("Invalid auth tag length in ciphertext");
  }

  const decipher = createDecipheriv(ALGORITHM, key, iv);
  decipher.setAuthTag(authTag);

  const plaintext = Buffer.concat([decipher.update(ct), decipher.final()]);
  return plaintext.toString("utf8");
}

/**
 * Returns true if DB_ENCRYPTION_KEY is set and well-formed.
 * Use this to gate encryption in scripts where the key may be unavailable.
 */
export function isEncryptionAvailable(): boolean {
  const hex = process.env.DB_ENCRYPTION_KEY;
  return typeof hex === "string" && hex.length === 64;
}
