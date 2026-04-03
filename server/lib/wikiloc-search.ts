/**
 * Wikiloc trail auto-search.
 * Requires WIKILOC_API_KEY env var. Returns null immediately if not set.
 * Timeout: 3s (per RF-07).
 */

// Wikiloc sport IDs relevant to trekking / hiking
const TREKKING_SPORTS = new Set([2, 7, 26]); // 2=hiking 7=trekking 26=mountain

function normalize(str: string): string {
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

function nameSimilarity(a: string, b: string): number {
  const na = normalize(a);
  const nb = normalize(b);
  if (na === nb) return 1;
  if (na.includes(nb) || nb.includes(na)) return 0.8;
  const wa = new Set(na.split(/\s+/).filter((w) => w.length > 3));
  const wb = new Set(nb.split(/\s+/).filter((w) => w.length > 3));
  if (wa.size === 0 && wb.size === 0) return 0;
  const overlap = [...wa].filter((w) => wb.has(w)).length;
  return overlap / Math.max(wa.size, wb.size);
}

export interface WiklocResult {
  wiklocId: string;
  wiklocUrl: string;
  gpxUrl: string;
}

export async function searchWikiloc(trail: {
  name: string;
  city: string | null;
  uf: string | null;
  distanceKm?: number | null;
  latitude?: number | null;
  longitude?: number | null;
}): Promise<WiklocResult | null> {
  const apiKey = process.env.WIKILOC_API_KEY;
  if (!apiKey) return null;

  const query = [trail.name, trail.city, trail.uf, 'Brasil']
    .filter(Boolean)
    .join(' ');

  const url = new URL('https://api.wikiloc.com/wikiloc/public/activities');
  url.searchParams.set('apiKey', apiKey);
  url.searchParams.set('sports', 'hiking,trekking');
  url.searchParams.set('q', query);
  url.searchParams.set('pageSize', '7');
  if (trail.latitude && trail.longitude) {
    url.searchParams.set('near', `${trail.latitude},${trail.longitude}`);
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 3000);

  try {
    const res = await fetch(url.toString(), {
      signal: controller.signal,
      headers: { 'User-Agent': 'Trekko/1.0 (https://trekko.com.br)' },
    });
    clearTimeout(timeout);
    if (!res.ok) return null;

    const data = (await res.json()) as any;
    const results: any[] = data.trails ?? data.activities ?? data.results ?? [];

    let best: { id: string; score: number } | null = null;

    for (const r of results) {
      const id = String(r.id ?? r.id_trail ?? '');
      if (!id) continue;

      // Name similarity (weight 0.6)
      const nameSim = nameSimilarity(trail.name, r.name ?? '') * 0.6;

      // Sport match (weight 0.2)
      const sportId = r.sport?.id ?? r.type_trail ?? 0;
      const sportMatch = TREKKING_SPORTS.has(Number(sportId)) ? 0.2 : 0;

      // Distance similarity within 30% tolerance (weight 0.2)
      let distScore = 0;
      const resultKm = r.length ? r.length / 1000 : r.distance_km;
      if (trail.distanceKm && resultKm) {
        const ratio = Math.abs(resultKm - trail.distanceKm) / trail.distanceKm;
        if (ratio < 0.3) distScore = (0.3 - ratio) / 0.3 * 0.2;
      }

      const score = nameSim + sportMatch + distScore;
      if (!best || score > best.score) {
        best = { id, score };
      }
    }

    if (!best || best.score < 0.35) return null;

    const wiklocId = best.id;
    const slug = normalize(trail.name).replace(/\s+/g, '-');
    return {
      wiklocId,
      wiklocUrl: `https://pt.wikiloc.com/trilhas-trekking/${slug}-${wiklocId}`,
      gpxUrl: `https://www.wikiloc.com/wikiloc/download.do?id=${wiklocId}`,
    };
  } catch {
    clearTimeout(timeout);
    return null;
  }
}
