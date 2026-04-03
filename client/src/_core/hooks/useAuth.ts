import { getLoginUrl } from "@/const";
import { staticGetCurrentUser, staticLogout } from "@/lib/staticAuth";
import { trpc } from "@/lib/trpc";
import { TRPCClientError } from "@trpc/client";
import { useCallback, useEffect, useMemo, useState } from "react";

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

  return Object.values(safeUser).some((value) => value !== null) ? safeUser : null;
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
      console.warn("Skipping manus-runtime-user-info persistence: payload too large");
      window.localStorage.removeItem("manus-runtime-user-info");
      return;
    }

    window.localStorage.setItem("manus-runtime-user-info", payload);
  } catch (error) {
    console.error("Failed to persist manus-runtime-user-info", error);
    try {
      window.localStorage.removeItem("manus-runtime-user-info");
    } catch {
      // ignore cleanup failure
    }
  }
}

export function useAuth(options?: UseAuthOptions) {
  const { redirectOnUnauthenticated = false, redirectPath = getLoginUrl() } =
    options ?? {};
  const utils = trpc.useUtils();

  const meQuery = trpc.auth.me.useQuery(undefined, {
    retry: false,
    refetchOnWindowFocus: false,
    enabled: !STATIC_NO_API,
  });

  const logoutMutation = trpc.auth.logout.useMutation({
    onSuccess: () => {
      utils.auth.me.setData(undefined, null);
    },
  });

  const logout = useCallback(async () => {
    if (STATIC_NO_API) {
      staticLogout();
      window.location.href = import.meta.env.BASE_URL;
      return;
    }
    try {
      await logoutMutation.mutateAsync();
    } catch (error: unknown) {
      if (
        error instanceof TRPCClientError &&
        error.data?.code === "UNAUTHORIZED"
      ) {
        return;
      }
      throw error;
    } finally {
      utils.auth.me.setData(undefined, null);
      await utils.auth.me.invalidate();
      if (typeof window !== "undefined") {
        try {
          window.localStorage.removeItem("manus-runtime-user-info");
        } catch {
          // ignore cleanup failure
        }
      }
    }
  }, [logoutMutation, utils]);

  const [staticTick, setStaticTick] = useState(0);

  useEffect(() => {
    if (!STATIC_NO_API) return;
    const handler = () => setStaticTick((t) => t + 1);
    window.addEventListener("staticAuthUpdated", handler);
    return () => window.removeEventListener("staticAuthUpdated", handler);
  }, []);

  const staticUser = STATIC_NO_API ? staticGetCurrentUser() : null;

  const state = useMemo(() => {
    const user = STATIC_NO_API ? staticUser : (meQuery.data ?? null);

    return {
      user,
      loading: STATIC_NO_API ? false : (meQuery.isLoading || logoutMutation.isPending),
      error: STATIC_NO_API ? null : (meQuery.error ?? logoutMutation.error ?? null),
      isAuthenticated: Boolean(user),
    };
  }, [
    staticTick,
    staticUser,
    meQuery.data,
    meQuery.error,
    meQuery.isLoading,
    logoutMutation.error,
    logoutMutation.isPending,
  ]);

  useEffect(() => {
    persistRuntimeUserInfo(state.user);
  }, [state.user]);

  useEffect(() => {
    if (!redirectOnUnauthenticated) return;
    if (state.loading) return;
    if (state.user) return;
    if (typeof window === "undefined") return;
    if (window.location.pathname === redirectPath) return;

    window.location.href = redirectPath;
  }, [
    redirectOnUnauthenticated,
    redirectPath,
    state.loading,
    state.user,
  ]);

  return {
    ...state,
    refresh: () => meQuery.refetch(),
    logout,
  };
}
