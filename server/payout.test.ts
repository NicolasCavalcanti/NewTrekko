import { describe, it, expect, vi, beforeEach } from 'vitest';
import {
  executePayoutWithRetry,
  setPixGateway,
  type PixGatewayFn,
} from './lib/payout-service';

vi.mock('./db', () => ({
  getPayoutById: vi.fn(),
  updatePayout: vi.fn().mockResolvedValue(undefined),
  getGuideFinancialInfoDecrypted: vi.fn(),
  getPlatformSetting: vi.fn().mockResolvedValue('3'),
  createAuditLog: vi.fn().mockResolvedValue(1),
}));

import * as db from './db';

const mockPayout = {
  id: 101,
  guideId: 2,
  status: 'scheduled',
  grossAmount: '1000.00',
  platformFee: '100.00',
  netAmount: '900.00',
  currency: 'BRL',
  scheduledDate: new Date(),
  retryCount: 0,
  pixKey: null,
  pixKeyType: null,
  failureReason: null,
};

const mockFinancialInfo = {
  id: 1,
  guideId: 2,
  pixKeyType: 'email',
  pixKey: 'guia@example.com',
  pixKeyHolderName: 'Guia Teste',
  pixKeyStatus: 'valid',
  pixKeyVerified: 1,
  paymentEnabled: 1,
  createdAt: new Date(),
  updatedAt: new Date(),
};

const successGateway: PixGatewayFn = async () => ({
  success: true,
  transactionId: 'tx-abc-123',
  endToEndId: 'e2e-abc-123',
});

const failGateway: PixGatewayFn = async () => ({
  success: false,
  error: 'Destino não encontrado',
});

// ---------------------------------------------------------------------------
// Story 10 — Execute payment using Pix key
// ---------------------------------------------------------------------------
describe('executePayoutWithRetry — success path (Story 10)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(db.getPayoutById).mockResolvedValue(mockPayout as any);
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue(mockFinancialInfo as any);
    setPixGateway(successGateway);
  });

  it('transitions payout to sent on gateway success', async () => {
    const result = await executePayoutWithRetry(101);

    expect(result.status).toBe('sent');
    expect(result.transactionId).toBe('tx-abc-123');
  });

  it('calls gateway with correct Pix key and amount', async () => {
    const captured: any[] = [];
    setPixGateway(async (params) => {
      captured.push(params);
      return { success: true, transactionId: 'tx-ok' };
    });

    await executePayoutWithRetry(101);

    expect(captured[0]).toMatchObject({
      guideId: 2,
      amount: 900,
      pixKeyType: 'email',
      pixKey: 'guia@example.com',
      externalRef: 'payout-101',
    });
  });

  it('snapshots masked Pix key on payout record (LGPD — no plaintext at rest)', async () => {
    await executePayoutWithRetry(101);

    expect(db.updatePayout).toHaveBeenCalledWith(
      101,
      expect.objectContaining({ pixKey: '****@example.com' })
    );
  });

  it('stores transactionId and endToEndId after success', async () => {
    await executePayoutWithRetry(101);

    expect(db.updatePayout).toHaveBeenCalledWith(
      101,
      expect.objectContaining({
        status: 'sent',
        pixTransactionId: 'tx-abc-123',
        pixEndToEndId: 'e2e-abc-123',
      })
    );
  });

  it('creates audit log on success', async () => {
    await executePayoutWithRetry(101);

    expect(db.createAuditLog).toHaveBeenCalledWith(
      expect.objectContaining({
        entityType: 'payout',
        entityId: 101,
        action: 'payout_sent',
        newValue: 'tx-abc-123',
      })
    );
  });
});

// ---------------------------------------------------------------------------
// Story 11 — Retry logic and failure logging
// ---------------------------------------------------------------------------
describe('executePayoutWithRetry — failure and retry (Story 11)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(db.getPayoutById).mockResolvedValue(mockPayout as any);
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue(mockFinancialInfo as any);
    vi.mocked(db.getPlatformSetting).mockResolvedValue('3');
    setPixGateway(failGateway);
  });

  it('increments retryCount and reschedules on first failure', async () => {
    const result = await executePayoutWithRetry(101);

    expect(result.status).toBe('scheduled');
    expect(result.error).toBe('Destino não encontrado');
    expect(db.updatePayout).toHaveBeenCalledWith(
      101,
      expect.objectContaining({ status: 'scheduled', retryCount: 1 })
    );
  });

  it('logs failure in audit on every failed attempt', async () => {
    await executePayoutWithRetry(101);

    expect(db.createAuditLog).toHaveBeenCalledWith(
      expect.objectContaining({
        action: 'payout_attempt_failed',
        entityType: 'payout',
        entityId: 101,
      })
    );
  });

  it('marks payout as failed after max retries', async () => {
    vi.mocked(db.getPayoutById).mockResolvedValue({
      ...mockPayout,
      retryCount: 3,
      status: 'scheduled',
    } as any);

    const result = await executePayoutWithRetry(101);

    expect(result.status).toBe('failed');
    expect(db.updatePayout).toHaveBeenCalledWith(
      101,
      expect.objectContaining({ status: 'failed' })
    );
  });

  it('logs max-retries-exceeded audit entry when exhausted', async () => {
    vi.mocked(db.getPayoutById).mockResolvedValue({
      ...mockPayout,
      retryCount: 3,
    } as any);

    await executePayoutWithRetry(101);

    expect(db.createAuditLog).toHaveBeenCalledWith(
      expect.objectContaining({ action: 'payout_max_retries_exceeded' })
    );
  });

  it('respects payout_max_retries platform setting', async () => {
    vi.mocked(db.getPlatformSetting).mockResolvedValue('1');
    vi.mocked(db.getPayoutById).mockResolvedValue({
      ...mockPayout,
      retryCount: 1,
    } as any);

    const result = await executePayoutWithRetry(101);

    expect(result.status).toBe('failed');
  });

  it('accepts overrideMaxRetries argument (bypasses platform setting)', async () => {
    vi.mocked(db.getPayoutById).mockResolvedValue({
      ...mockPayout,
      retryCount: 2,
    } as any);

    const result = await executePayoutWithRetry(101, 5); // max=5, count=2 → not exhausted

    expect(result.status).toBe('scheduled');
  });
});

// ---------------------------------------------------------------------------
// Story 10 — Guard: guide has no Pix key
// ---------------------------------------------------------------------------
describe('executePayoutWithRetry — missing or invalid Pix key', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(db.getPayoutById).mockResolvedValue(mockPayout as any);
    vi.mocked(db.getPlatformSetting).mockResolvedValue('3');
    setPixGateway(successGateway);
  });

  it('schedules retry when guide has no financial info', async () => {
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue(undefined);

    const result = await executePayoutWithRetry(101);

    expect(result.status).toBe('scheduled');
    expect(result.error).toContain('chave Pix');
  });

  it('blocks (not retried) when Pix key status is invalid', async () => {
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue({
      ...mockFinancialInfo,
      pixKeyStatus: 'invalid',
    } as any);

    const result = await executePayoutWithRetry(101);

    expect(result.status).toBe('blocked');
    expect(db.updatePayout).toHaveBeenCalledWith(
      101,
      expect.objectContaining({ status: 'blocked' })
    );
  });

  it('creates blocked audit log when Pix key is invalid', async () => {
    vi.mocked(db.getGuideFinancialInfoDecrypted).mockResolvedValue({
      ...mockFinancialInfo,
      pixKeyStatus: 'invalid',
    } as any);

    await executePayoutWithRetry(101);

    expect(db.createAuditLog).toHaveBeenCalledWith(
      expect.objectContaining({ action: 'payout_blocked_invalid_pix_key' })
    );
  });
});

// ---------------------------------------------------------------------------
// Guard: non-retriable statuses
// ---------------------------------------------------------------------------
describe('executePayoutWithRetry — non-retriable statuses', () => {
  it('throws when payout is already completed', async () => {
    vi.mocked(db.getPayoutById).mockResolvedValue({
      ...mockPayout,
      status: 'completed',
    } as any);

    await expect(executePayoutWithRetry(101)).rejects.toThrow('cannot be retried');
  });

  it('throws when payout is already sent', async () => {
    vi.mocked(db.getPayoutById).mockResolvedValue({
      ...mockPayout,
      status: 'sent',
    } as any);

    await expect(executePayoutWithRetry(101)).rejects.toThrow('cannot be retried');
  });

  it('throws when payout is not found', async () => {
    vi.mocked(db.getPayoutById).mockResolvedValue(undefined);

    await expect(executePayoutWithRetry(999)).rejects.toThrow('not found');
  });
});
