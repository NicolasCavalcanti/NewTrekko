/**
 * Unified data hooks for the Guides page.
 *
 * When VITE_STATIC_MODE=true (GitHub Pages build) they read from the
 * pre-generated /data/guides.json file and do filtering client-side.
 * Otherwise they delegate to the tRPC backend as usual.
 */

import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';
import { trpc } from '@/lib/trpc';

const STATIC_MODE = import.meta.env.VITE_STATIC_MODE === 'true';
const BASE = import.meta.env.BASE_URL ?? '/';

type StaticGuide = {
  id: number;
  name: string | null;
  cadasturNumber: string;
  uf: string | null;
  city: string | null;
  phone: string | null;
  email: string | null;
  website: string | null;
  categories: string[] | null;
  validUntil: string | null;
  isVerified: boolean;
  isDriverGuide: boolean;
};

function normalize(str: string) {
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

/** Shared fetch — result is cached for the lifetime of the page. */
function useAllStaticGuides() {
  return useQuery<StaticGuide[]>({
    queryKey: ['static-guides'],
    queryFn: async () => {
      const url = `${BASE}data/guides.json`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Failed to load ${url}: ${res.status}`);
      return res.json();
    },
    enabled: STATIC_MODE,
    staleTime: Infinity,
  });
}

export function useGuidesList(params: {
  search?: string;
  cadasturCode?: string;
  uf?: string;
  city?: string;
  page: number;
  limit: number;
}) {
  // Always call both hooks — React rules of hooks require unconditional calls.
  // STATIC_MODE is a compile-time constant so only one path is ever active.
  const staticQuery = useAllStaticGuides();
  const trpcQuery = trpc.guides.list.useQuery(params, {
    enabled: !STATIC_MODE,
    staleTime: 60_000,
  });

  const staticResult = useMemo(() => {
    if (!STATIC_MODE || !staticQuery.data) return undefined;

    let result = staticQuery.data;

    if (params.search) {
      const term = normalize(params.search);
      result = result.filter((g) => g.name && normalize(g.name).startsWith(term));
    }
    if (params.cadasturCode) {
      result = result.filter((g) =>
        g.cadasturNumber.startsWith(params.cadasturCode!),
      );
    }
    if (params.uf) {
      result = result.filter((g) => g.uf === params.uf);
    }
    if (params.city && params.city !== 'all') {
      result = result.filter(
        (g) => g.city?.toLowerCase() === params.city!.toLowerCase(),
      );
    }

    const total = result.length;
    const offset = (params.page - 1) * params.limit;
    return { guides: result.slice(offset, offset + params.limit), total };
  }, [
    staticQuery.data,
    params.search,
    params.cadasturCode,
    params.uf,
    params.city,
    params.page,
    params.limit,
  ]);

  if (STATIC_MODE) {
    return { data: staticResult, isLoading: staticQuery.isLoading };
  }
  return { data: trpcQuery.data, isLoading: trpcQuery.isLoading };
}

export function useGuideCities(uf?: string) {
  const staticQuery = useAllStaticGuides();
  const trpcQuery = trpc.guides.getCities.useQuery(
    { uf: uf && uf !== 'all' ? uf : undefined },
    { enabled: !STATIC_MODE },
  );

  const staticCities = useMemo(() => {
    if (!STATIC_MODE || !staticQuery.data || !uf || uf === 'all') return undefined;
    const citySet = new Set<string>();
    for (const g of staticQuery.data) {
      if (g.uf === uf && g.city) citySet.add(g.city);
    }
    return Array.from(citySet).sort((a, b) => a.localeCompare(b, 'pt-BR'));
  }, [staticQuery.data, uf]);

  if (STATIC_MODE) {
    return { data: staticCities, isLoading: staticQuery.isLoading };
  }
  return { data: trpcQuery.data, isLoading: trpcQuery.isLoading };
}
