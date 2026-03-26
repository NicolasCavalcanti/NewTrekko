/**
 * Unified data hooks for the Trails page.
 *
 * When VITE_STATIC_MODE=true (GitHub Pages build) they read from the
 * pre-generated /data/trails.json file and do filtering client-side.
 * Otherwise they delegate to the tRPC backend as usual.
 */

import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';
import { trpc } from '@/lib/trpc';

const STATIC_MODE = import.meta.env.VITE_STATIC_MODE === 'true';
const BASE = import.meta.env.BASE_URL ?? '/';

type StaticTrail = {
  id: number;
  name: string;
  slug: string | null;
  uf: string;
  city: string | null;
  region: string | null;
  park: string | null;
  distanceKm: string | null;
  elevationGain: number | null;
  maxAltitude: number | null;
  difficulty: string | null;
  description: string | null;
  shortDescription: string | null;
  hookText: string | null;
  ctaText: string | null;
  guideRequired: number;
  entranceFee: string | null;
  waterPoints: string[] | null;
  campingPoints: string[] | null;
  bestSeason: string | null;
  estimatedTime: string | null;
  trailType: string | null;
  imageUrl: string | null;
  images: string[] | null;
  highlights: string[] | null;
  wiklocUrl: string | null;
  wiklocGpxUrl: string | null;
  status: string;
};

function normalize(str: string) {
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

function useAllStaticTrails() {
  return useQuery<StaticTrail[]>({
    queryKey: ['static-trails'],
    queryFn: async () => {
      const url = `${BASE}data/trails.json`.replace('//', '/');
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Failed to load trails.json: ${res.status}`);
      return res.json();
    },
    enabled: STATIC_MODE,
    staleTime: Infinity,
  });
}

export function useTrailsList(params: {
  search?: string;
  uf?: string;
  difficulty?: string;
  maxDistance?: number;
  page?: number;
  limit?: number;
}) {
  const page = params.page ?? 1;
  const limit = params.limit ?? 12;

  const staticQuery = useAllStaticTrails();

  const staticResult = useMemo(() => {
    if (!STATIC_MODE || !staticQuery.data) return undefined;

    let result = staticQuery.data;

    if (params.search) {
      const term = normalize(params.search);
      result = result.filter(
        (t) =>
          normalize(t.name).includes(term) ||
          normalize(t.city ?? '').includes(term) ||
          normalize(t.region ?? '').includes(term),
      );
    }

    if (params.uf) {
      result = result.filter((t) => t.uf === params.uf);
    }

    if (params.difficulty) {
      result = result.filter((t) => t.difficulty === params.difficulty);
    }

    if (params.maxDistance) {
      result = result.filter(
        (t) => t.distanceKm != null && parseFloat(t.distanceKm) <= params.maxDistance!,
      );
    }

    const total = result.length;
    const paged = result.slice((page - 1) * limit, page * limit);
    return { trails: paged, total };
  }, [staticQuery.data, params.search, params.uf, params.difficulty, params.maxDistance, page, limit]);

  const trpcQuery = trpc.trails.list.useQuery(
    { ...params, page, limit },
    { enabled: !STATIC_MODE },
  );

  if (STATIC_MODE) {
    return {
      data: staticResult,
      isLoading: staticQuery.isLoading,
      error: staticQuery.error,
    };
  }

  return {
    data: trpcQuery.data,
    isLoading: trpcQuery.isLoading,
    error: trpcQuery.error,
  };
}

export function useTrailById(id: number) {
  const staticQuery = useAllStaticTrails();

  const staticTrail = useMemo(() => {
    if (!STATIC_MODE || !staticQuery.data) return undefined;
    const trail = staticQuery.data.find((t) => t.id === id);
    return trail ? { trail, relatedExpeditions: [] } : undefined;
  }, [staticQuery.data, id]);

  const trpcQuery = trpc.trails.getById.useQuery(
    { id },
    { enabled: !STATIC_MODE && id > 0 },
  );

  if (STATIC_MODE) {
    return {
      data: staticTrail,
      isLoading: staticQuery.isLoading && !staticTrail,
      error: staticQuery.error,
    };
  }

  return {
    data: trpcQuery.data,
    isLoading: trpcQuery.isLoading,
    error: trpcQuery.error,
  };
}
