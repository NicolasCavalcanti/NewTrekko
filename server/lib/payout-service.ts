import * as db from '../db';
import { maskPixKey } from './pix-validation';

// ---------------------------------------------------------------------------
// Payment gateway abstraction (Story 10)
// ---------------------------------------------------------------------------

export type PayoutGatewayResult =
  | { success: true; transactionId: string; endToEndId?: string }
  | { success: false; error: string };

export type PixGatewayFn = (params: {
  guideId: number;
  amount: number;
  pixKeyType: string;
  pixKey: string;
  pixKeyHolderName: string;
  externalRef: string;
}) => Promise<PayoutGatewayResult>;

// Default stub — replaced at startup or injected in tests via setPixGateway()
let _gateway: PixGatewayFn = async () => ({
  success: false,
  error: 'Pix gateway not configured. Call setPixGateway() at startup.',
});

export function setPixGateway(fn: PixGatewayFn): void {
  _gateway = fn;
}

export function getPixGateway(): PixGatewayFn {
  return _gateway;
}

// ---------------------------------------------------------------------------
// Core payout execution (Story 10) with retry logic (Story 11)
// ---------------------------------------------------------------------------

const DEFAULT_MAX_RETRIES = 3;

export async function executePayoutWithRetry(
  payoutId: number,
  overrideMaxRetries?: number
): Promise<{ status: string; transactionId?: string; error?: string }> {
  const payout = await db.getPayoutById(payoutId);
  if (!payout) throw new Error(`Payout ${payoutId} not found`);

  if (!['scheduled', 'processing', 'failed'].includes(payout.status)) {
    throw new Error(
      `Payout ${payoutId} cannot be retried (status: ${payout.status})`
    );
  }

  const maxRetries =
    overrideMaxRetries ??
    Number((await db.getPlatformSetting('payout_max_retries')) ?? DEFAULT_MAX_RETRIES);

  // Story 11: already exhausted retries — block further attempts
  if ((payout.retryCount ?? 0) >= maxRetries) {
    await db.updatePayout(payoutId, {
      status: 'failed',
      failureReason: 'Número máximo de tentativas atingido',
    });
    await db.createAuditLog({
      entityType: 'payout',
      entityId: payoutId,
      action: 'payout_max_retries_exceeded',
      previousValue: String(payout.retryCount),
      newValue: String(maxRetries),
      actorType: 'system',
      source: 'payout_service',
    });
    return { status: 'failed', error: 'Número máximo de tentativas atingido' };
  }

  // Transition to processing
  await db.updatePayout(payoutId, { status: 'processing', processedAt: new Date() });

  // Story 10: load guide Pix key from guide_financial_info (decrypted)
  const financialInfo = await db.getGuideFinancialInfoDecrypted(payout.guideId);

  if (!financialInfo?.pixKey || !financialInfo?.pixKeyType) {
    return await _handleFailure(
      payoutId,
      'Guia não possui chave Pix configurada',
      payout.retryCount ?? 0,
      maxRetries,
      false // retriable — guide may configure key before next run
    );
  }

  // Story 9 guard: blocked key is not retriable
  if (financialInfo.pixKeyStatus === 'invalid') {
    await db.updatePayout(payoutId, {
      status: 'blocked',
      failureReason: 'Chave Pix do guia está inválida',
    });
    await db.createAuditLog({
      entityType: 'payout',
      entityId: payoutId,
      action: 'payout_blocked_invalid_pix_key',
      actorType: 'system',
      source: 'payout_service',
    });
    return { status: 'blocked', error: 'Chave Pix do guia está inválida' };
  }

  // Story 8: snapshot masked key on payout record for audit trail (LGPD — no plaintext at rest)
  await db.updatePayout(payoutId, {
    pixKey: maskPixKey(financialInfo.pixKeyType, financialInfo.pixKey),
    pixKeyType: financialInfo.pixKeyType,
  });

  // Story 10: call payment gateway
  const result = await _gateway({
    guideId: payout.guideId,
    amount: Number(payout.netAmount),
    pixKeyType: financialInfo.pixKeyType,
    pixKey: financialInfo.pixKey, // plaintext in-memory only — never persisted
    pixKeyHolderName: financialInfo.pixKeyHolderName ?? '',
    externalRef: `payout-${payoutId}`,
  });

  if (result.success) {
    await db.updatePayout(payoutId, {
      status: 'sent',
      pixTransactionId: result.transactionId,
      pixEndToEndId: result.endToEndId,
      processedAt: new Date(),
    });
    await db.createAuditLog({
      entityType: 'payout',
      entityId: payoutId,
      action: 'payout_sent',
      newValue: result.transactionId,
      actorType: 'system',
      source: 'payout_service',
    });
    return { status: 'sent', transactionId: result.transactionId };
  }

  // Story 11: log failure and schedule retry
  return await _handleFailure(
    payoutId,
    result.error,
    payout.retryCount ?? 0,
    maxRetries,
    true
  );
}

async function _handleFailure(
  payoutId: number,
  error: string,
  currentRetryCount: number,
  maxRetries: number,
  increment: boolean
): Promise<{ status: string; error: string }> {
  const newRetryCount = increment ? currentRetryCount + 1 : currentRetryCount;
  const exhausted = newRetryCount >= maxRetries;

  await db.updatePayout(payoutId, {
    status: exhausted ? 'failed' : 'scheduled', // re-schedule for next run if not exhausted
    failureReason: error,
    retryCount: newRetryCount,
  });

  // Story 11: log every failure
  await db.createAuditLog({
    entityType: 'payout',
    entityId: payoutId,
    action: exhausted ? 'payout_failed_max_retries' : 'payout_attempt_failed',
    newValue: JSON.stringify({ error, retryCount: newRetryCount, maxRetries }),
    actorType: 'system',
    source: 'payout_service',
  });

  return { status: exhausted ? 'failed' : 'scheduled', error };
}
