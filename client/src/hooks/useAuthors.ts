import { useQuery } from '@tanstack/react-query';
import { useMemo } from 'react';

const BASE = import.meta.env.BASE_URL ?? '/';

export type Author = {
  slug: string;
  name: string;
  title: string;
  shortBio: string;
  bio: string;
  cadasturNumber: string | null;
  specialty: string[];
  yearsExperience: number;
  trailsCount: number;
  location: string;
  photoUrl: string | null;
  social: {
    instagram: string | null;
    website: string | null;
  };
  postIds: number[];
};

function useAllAuthors() {
  return useQuery<Author[]>({
    queryKey: ['static-authors'],
    queryFn: async () => {
      const url = `${BASE}data/authors.json`.replace('//', '/');
      const res = await fetch(url);
      if (!res.ok) return [] as Author[];
      return res.json() as Promise<Author[]>;
    },
    staleTime: Infinity,
  });
}

export function useAuthorBySlug(slug: string) {
  const query = useAllAuthors();
  const author = useMemo(
    () => query.data?.find((a) => a.slug === slug) ?? null,
    [query.data, slug],
  );
  return { data: author, isLoading: query.isLoading };
}

export function useAuthorById(postId: number) {
  const query = useAllAuthors();
  const author = useMemo(
    () => query.data?.find((a) => a.postIds.includes(postId)) ?? null,
    [query.data, postId],
  );
  return { data: author, isLoading: query.isLoading };
}

export function useAllAuthorsData() {
  return useAllAuthors();
}
