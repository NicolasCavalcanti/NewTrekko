/**
 * DB-PERF-05: Buffered blog post view counter.
 *
 * Problem: incrementing viewCount on every request causes a write operation
 * for each page view, creating lock contention on a predominantly-read table.
 *
 * Solution: accumulate counts in memory and flush to the DB every FLUSH_INTERVAL_MS.
 * One batched INSERT … ON DUPLICATE KEY UPDATE replaces N individual UPDATEs.
 *
 * Usage:
 *   import { viewCounter } from './viewCounter';
 *   viewCounter.track(postId);          // call on each page view
 *
 * The flush loop and SIGTERM handler are started by calling viewCounter.start(getDb).
 * This is called once from server/_core/index.ts at startup.
 */

const FLUSH_INTERVAL_MS = 5 * 60 * 1000; // 5 minutes

type GetDb = () => Promise<{ execute: (query: any) => Promise<any> } | null>;

class ViewCounter {
  private counts = new Map<number, number>();
  private timer: NodeJS.Timeout | null = null;
  private getDb: GetDb | null = null;

  /** Register one page view for the given blog post id. */
  track(postId: number): void {
    this.counts.set(postId, (this.counts.get(postId) ?? 0) + 1);
  }

  /**
   * Start the background flush loop and register the SIGTERM handler.
   * @param getDb  The same getDb() factory used by the rest of the app.
   */
  start(getDb: GetDb): void {
    this.getDb = getDb;
    this.timer = setInterval(() => void this.flush(), FLUSH_INTERVAL_MS);
    // Allow the process to exit even while the timer is running.
    if (this.timer.unref) this.timer.unref();

    process.on("SIGTERM", () => void this.flushAndExit());
  }

  /** Flush all buffered counts to the database and clear the in-memory map. */
  async flush(): Promise<void> {
    if (this.counts.size === 0 || !this.getDb) return;

    const snapshot = new Map(this.counts);
    this.counts.clear();

    const db = await this.getDb();
    if (!db) {
      // Re-merge the snapshot back so counts are not lost on transient failures.
      for (const [id, count] of snapshot) {
        this.counts.set(id, (this.counts.get(id) ?? 0) + count);
      }
      return;
    }

    // Build a batch INSERT … ON DUPLICATE KEY UPDATE.
    // One query regardless of how many posts were viewed.
    const rows = Array.from(snapshot.entries());

    try {
      // Use the raw mysql2 pool for a plain parameterised query.
      // getRawPool() returns the Pool created in db.ts (DB-PERF-06).
      const { getRawPool } = await import("../db");
      const rawPool = getRawPool();
      if (!rawPool) return;

      const escapedRows = rows
        .map(([id, count]) => `(${Number(id)}, ${Number(count)})`)
        .join(", ");
      await rawPool.query(
        `INSERT INTO blog_posts (id, viewCount) VALUES ${escapedRows}
         ON DUPLICATE KEY UPDATE viewCount = viewCount + VALUES(viewCount)`
      );
    } catch (err) {
      console.error("[ViewCounter] Flush failed:", err);
      // Re-merge on error so counts survive the next interval.
      for (const [id, count] of snapshot) {
        this.counts.set(id, (this.counts.get(id) ?? 0) + count);
      }
    }
  }

  private async flushAndExit(): Promise<void> {
    console.log("[ViewCounter] SIGTERM received — flushing view counts before exit…");
    await this.flush();
    process.exit(0);
  }
}

export const viewCounter = new ViewCounter();
