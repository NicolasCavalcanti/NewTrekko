import { getLoginUrl } from "@/const";
import { staticGetCurrentUser, staticLogout } from "@/lib/staticAuth";
import { USE_SUPABASE } from "@/lib/supabase";
import {
  supabaseGetCurrentUser,
  supabaseOnAuthChange,
  supabaseSignOut,
} from "@/lib/supabaseAuth";
import { trpc } from "@/lib/trpc";
import { TRPCClientError } from "@trpc/client";
import { useCallback, useEffect, useMemo, useState } from "react";

// STATIC_NO_API: no backend at all — use localStorage demo.
const STATIC_NO_API =
  import.meta.env.VITE_STATIC_MODE === "true" && !import.meta.env.VITE_API_URL;

type UseAuthOptions = {
  redirectOnUnauthenticated?: boolean;
  redirectPath?: string;
};

function getSafeRuntimeUserInfo(user: unknown) {
  if (!user || typeof user !== "object") return null;
  const source = user as Record<string, unknown>;
  const safeUser = {
    id: source.id ?? null,
    email: typeof source.email === "string" ? source.email : null,
    name:
      typeof source.name === "string"
        ? source.name
        : typeof source.fullName === "string"
          ? source.fullName
          : typeof source.displayName === "string"
            ? source.displayName
            : null,
    role: typeof source.role === "string" ? source.role : null,
  };
  return Object.values(safeUser).some((v) => v !== null) ? safeUser : null;
}

function persistRuntimeUserInfo(user: unknown) {
  if (typeof window === "undefined") return;
  try {
    const safeUser = getSafeRuntimeUserInfo(user);
    if (!safeUser) {
      window.localStorage.removeItem("manus-runtime-user-info");
      return;
    }
    const payload = JSON.stringify(safeUser);
    if (payload.length > 10000) {
      window.localStorage.removeItem("manus-runtime-user-info");
      return;
    }
    window.localStorage.setItem("manus-runtime-user-info", payload);
  } catch {
    try { window.localStorage.removeItem("manus-runtime-user-info"); } catch { /* ignore */ }
  }
}

export function useAuth(options?: UseAuthOptions) {
  const { redirectOnUnauthenticated = false, redirectPath = getLoginUrl() } =
    options ?? {};
  const utils = trpc.useUtils();

  // ── tRPC backend mode ──────────────────────────────────────────────────────
  const meQuery = trpc.auth.me.useQuery(undefined, {
    retry: false,
    refetchOnWindowFocus: false,
    enabled: !STATIC_NO_API && !USE_SUPABASE,
  });

  const logoutMutation = trpc.auth.logout.useMutation({
    onSuccess: () => { utils.auth.me.setData(undefined, null); },
  });

  // ── Supabase mode ──────────────────────────────────────────────────────────
  const [supabaseUser, setSupabaseUser] = useState<any>(null);
  const [supabaseLoading, setSupabaseLoading] = useState(USE_SUPABASE);

  useEffect(() => {
    if (!USE_SUPABASE) return;
    // Initial session check
    supabaseGetCurrentUser().then((u) => {
      setSupabaseUser(u);
      setSupabaseLoading(false);
    });
    // Subscribe to auth state changes (login, logout, token refresh)
    const unsub = supabaseOnAuthChange((u) => {
      setSupabaseUser(u);
      setSupabaseLoading(false);
    });
    return unsub;
  }, []);

  // ── Static/localStorage demo mode ─────────────────────────────────────────
  const [staticTick, setStaticTick] = useState(0);
  useEffect(() => {
    if (!STATIC_NO_API) return;
    const handler = () => setStaticTick((t) => t + 1);
    window.addEventListener("staticAuthUpdated", handler);
    return () => window.removeEventListener("staticAuthUpdated", handler);
  }, []);
  const staticUser = STATIC_NO_API ? staticGetCurrentUser() : null;

  // ── Logout ─────────────────────────────────────────────────────────────────
  const logout = useCallback(async () => {
    if (USE_SUPABASE) {
      await supabaseSignOut();
      setSupabaseUser(null);
      window.location.href = import.meta.env.BASE_URL;
      return;
    }
    if (STATIC_NO_API) {
      staticLogout();
      window.location.href = import.meta.env.BASE_URL;
      return;
    }
    try {
      await logoutMutation.mutateAsync();
    } catch (error: unknown) {
      if (error instanceof TRPCClientError && error.data?.code === "UNAUTHORIZED") return;
      throw error;
    } finally {
      utils.auth.me.setData(undefined, null);
      await utils.auth.me.invalidate();
      try { window.localStorage.removeItem("manus-runtime-user-info"); } catch { /* ignore */ }
    }
  }, [logoutMutation, utils]);

  // ── Unified state ──────────────────────────────────────────────────────────
  const state = useMemo(() => {
    let user: any;
    let loading: boolean;
    let error: any;

    if (USE_SUPABASE) {
      user = supabaseUser;
      loading = supabaseLoading;
      error = null;
    } else if (STATIC_NO_API) {
      user = staticUser;
      loading = false;
      error = null;
    } else {
      user = meQuery.data ?? null;
      loading = meQuery.isLoading || logoutMutation.isPending;
      error = meQuery.error ?? logoutMutation.error ?? null;
    }

    return { user, loading, error, isAuthenticated: Boolean(user) };
  }, [
    supabaseUser, supabaseLoading,
    staticTick, staticUser,
    meQuery.data, meQuery.error, meQuery.isLoading,
    logoutMutation.error, logoutMutation.isPending,
  ]);

  useEffect(() => { persistRuntimeUserInfo(state.user); }, [state.user]);

  useEffect(() => {
    if (!redirectOnUnauthenticated) return;
    if (state.loading) return;
    if (state.user) return;
    if (typeof window === "undefined") return;
    if (window.location.pathname === redirectPath) return;
    window.location.href = redirectPath;
  }, [redirectOnUnauthenticated, redirectPath, state.loading, state.user]);

  return { ...state, refresh: () => meQuery.refetch(), logout };
}
