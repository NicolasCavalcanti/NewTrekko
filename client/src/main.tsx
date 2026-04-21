import { trpc } from "@/lib/trpc";
import { UNAUTHED_ERR_MSG } from '@shared/const';
import { QueryClient, QueryClientProvider, hydrate } from "@tanstack/react-query";
import { httpBatchLink, TRPCClientError } from "@trpc/client";
import { createRoot } from "react-dom/client";
import superjson from "superjson";
import App from "./App";
import { getLoginUrl } from "./const";
import "./index.css";

const queryClient = new QueryClient();

// Hydrate server-side prefetched data if available
const ssrState = (window as any).__DEHYDRATED_STATE__;
if (ssrState) {
  hydrate(queryClient, superjson.deserialize(ssrState));
}

const redirectToLoginIfUnauthorized = (error: unknown) => {
  if (!(error instanceof TRPCClientError)) return;
  if (typeof window === "undefined") return;

  const isUnauthorized = error.message === UNAUTHED_ERR_MSG;

  if (!isUnauthorized) return;

  window.location.href = getLoginUrl();
};

queryClient.getQueryCache().subscribe(event => {
  if (event.type === "updated" && event.action.type === "error") {
    const error = event.query.state.error;
    redirectToLoginIfUnauthorized(error);
    console.error("[API Query Error]", error);
  }
});

queryClient.getMutationCache().subscribe(event => {
  if (event.type === "updated" && event.action.type === "error") {
    const error = event.mutation.state.error;
    redirectToLoginIfUnauthorized(error);
    console.error("[API Mutation Error]", error);
  }
});

// Allow a deployed backend URL to be injected at build time so that the
// static GitHub Pages frontend can reach the API server.
const apiBase = (import.meta.env.VITE_API_URL ?? "").replace(/\/$/, "");

// True when deployed as a static site with no backend configured.
// In this state every tRPC call must be intercepted so we return a proper
// JSON error instead of letting GitHub Pages serve its HTML 404 page,
// which causes "Unexpected token '<'" parse crashes.
const STATIC_MODE = import.meta.env.VITE_STATIC_MODE === "true";
const STATIC_NO_API = STATIC_MODE;

/** Returns a well-formed tRPC batch error response for N operations. */
function makeStaticErrorResponse(url: string | URL | Request): Response {
  const href =
    typeof url === "string" ? url : url instanceof URL ? url.href : url.url;
  const path = href.split("/api/trpc/")[1]?.split("?")[0] ?? "";
  const batchSize = path ? path.split(",").length : 1;
  // Wrap in superjson format: tRPC's transformResult calls
  // transformer.deserialize(item.error), which expects { json, meta? }.
  const body = JSON.stringify(
    Array.from({ length: batchSize }, () => ({
      error: {
        json: {
          message: "Servidor não disponível nesta versão estática",
          code: -32603,
          data: { code: "INTERNAL_SERVER_ERROR", httpStatus: 503 },
        },
      },
    }))
  );
  return new Response(body, {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
}


const trpcClient = trpc.createClient({
  links: [
    httpBatchLink({
      url: `${apiBase}/api/trpc`,
      transformer: superjson,
      fetch(input, init) {
        if (STATIC_NO_API) return Promise.resolve(makeStaticErrorResponse(input));
        return globalThis.fetch(input, { ...(init ?? {}), credentials: "include" });
      },
    }),
  ],
});

createRoot(document.getElementById("root")!).render(
  <trpc.Provider client={trpcClient} queryClient={queryClient}>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </trpc.Provider>
);
