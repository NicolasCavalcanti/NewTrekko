/**
 * Unified data hooks for the Blog pages.
 *
 * When VITE_STATIC_MODE=true (GitHub Pages build) they read from the
 * pre-generated /data/blog.json file and do filtering client-side.
 * Otherwise they delegate to the tRPC backend as usual.
 */

import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';
import { trpc } from '@/lib/trpc';

const STATIC_MODE = import.meta.env.VITE_STATIC_MODE === 'true';
const BASE = import.meta.env.BASE_URL ?? '/';

export type StaticBlogPost = {
  id: number;
  slug: string;
  title: string;
  subtitle: string | null;
  content: string;
  excerpt: string | null;
  category: string | null;
  imageUrl: string | null;
  images: string[] | null;
  authorId: number | null;
  authorName: string | null;
  authorSlug: string | null;
  readingTime: number | null;
  relatedTrailIds: number[] | null;
  tags: string[] | null;
  metaTitle: string | null;
  metaDescription: string | null;
  featured: number;
  viewCount: number;
  status: string;
  publishedAt: string | null;
  createdAt: string;
  updatedAt: string;
};

function normalize(str: string) {
  return str
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase();
}

function useAllStaticPosts() {
  return useQuery<StaticBlogPost[]>({
    queryKey: ['static-blog'],
    queryFn: async () => {
      const url = `${BASE}data/blog.json`.replace('//', '/');
      const res = await fetch(url);
      if (!res.ok) return [] as StaticBlogPost[];
      return res.json() as Promise<StaticBlogPost[]>;
    },
    enabled: STATIC_MODE,
    staleTime: Infinity,
  });
}

/** Public export for pages that need all published posts (e.g. author profile). */
export function useAllStaticPostsPublic() {
  const query = useAllStaticPosts();
  const published = query.data?.filter((p) => p.status === 'published') ?? undefined;
  return { data: published, isLoading: query.isLoading };
}

export function useBlogList(params: {
  search?: string;
  category?: string;
  featured?: boolean;
  page?: number;
  limit?: number;
}) {
  const page = params.page ?? 1;
  const limit = params.limit ?? 12;

  const staticQuery = useAllStaticPosts();

  const staticResult = useMemo(() => {
    if (!STATIC_MODE || !staticQuery.data) return undefined;

    let result = staticQuery.data.filter((p) => p.status === 'published');

    if (params.search) {
      const term = normalize(params.search);
      result = result.filter(
        (p) =>
          normalize(p.title).includes(term) ||
          normalize(p.excerpt ?? '').includes(term),
      );
    }
    if (params.category) {
      result = result.filter((p) => p.category === params.category);
    }
    if (params.featured) {
      result = result.filter((p) => p.featured === 1);
    }

    const total = result.length;
    const paged = result.slice((page - 1) * limit, page * limit);
    return { posts: paged, total };
  }, [staticQuery.data, params.search, params.category, params.featured, page, limit]);

  const trpcQuery = trpc.blog.list.useQuery(
    { ...params, page, limit },
    { enabled: !STATIC_MODE },
  );

  if (STATIC_MODE) {
    return { data: staticResult, isLoading: staticQuery.isLoading };
  }
  return { data: trpcQuery.data, isLoading: trpcQuery.isLoading };
}

export function useBlogPostBySlug(slug: string) {
  const staticQuery = useAllStaticPosts();

  const staticPost = useMemo(() => {
    if (!STATIC_MODE || !staticQuery.data) return undefined;
    return staticQuery.data.find((p) => p.slug === slug && p.status === 'published') ?? null;
  }, [staticQuery.data, slug]);

  const trpcQuery = trpc.blog.getBySlug.useQuery(
    { slug },
    { enabled: !STATIC_MODE && !!slug },
  );

  if (STATIC_MODE) {
    return {
      data: staticPost,
      isLoading: staticQuery.isLoading && staticPost === undefined,
      error: staticQuery.error,
    };
  }
  return {
    data: trpcQuery.data,
    isLoading: trpcQuery.isLoading,
    error: trpcQuery.error,
  };
}

export function useBlogRelated(postId: number | undefined, category: string | undefined) {
  const staticQuery = useAllStaticPosts();

  const staticRelated = useMemo(() => {
    if (!STATIC_MODE || !staticQuery.data || !postId || !category) return undefined;
    return staticQuery.data
      .filter((p) => p.id !== postId && p.category === category && p.status === 'published')
      .slice(0, 3);
  }, [staticQuery.data, postId, category]);

  const trpcQuery = trpc.blog.getRelated.useQuery(
    { postId: postId ?? 0, category: category ?? '' },
    { enabled: !STATIC_MODE && !!postId && !!category },
  );

  if (STATIC_MODE) {
    return { data: staticRelated, isLoading: staticQuery.isLoading };
  }
  return { data: trpcQuery.data, isLoading: trpcQuery.isLoading };
}
