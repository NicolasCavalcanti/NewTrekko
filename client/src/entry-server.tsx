import React from "react";
import { renderToString } from "react-dom/server";
import { HelmetProvider } from "react-helmet-async";
import type { HelmetServerState } from "react-helmet-async";
import {
  QueryClient,
  QueryClientProvider,
  dehydrate,
  hydrate,
} from "@tanstack/react-query";
import { trpc } from "@/lib/trpc";
import { httpBatchLink } from "@trpc/client";
import superjson from "superjson";
import { Router, Route, Switch } from "wouter";
import { memoryLocation } from "wouter/memory-location";
import { ThemeProvider } from "./contexts/ThemeContext";

// Import pages directly (not lazy) to avoid React.lazy/Suspense issues with renderToString
import TrailDetail from "./pages/TrailDetail";
import BlogPost from "./pages/BlogPost";
import GuideDetail from "./pages/GuideDetail";

export type HelmetContext = { helmet?: HelmetServerState };

export type RenderResult = {
  html: string;
  helmetContext: HelmetContext;
  dehydratedState: ReturnType<typeof dehydrate>;
};

export async function render(
  url: string,
  preloadedState?: unknown
): Promise<RenderResult> {
  // Guard localStorage for SSR
  if (typeof globalThis.localStorage === "undefined") {
    (globalThis as any).localStorage = {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {},
    };
  }

  const helmetContext: HelmetContext = {};

  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: Infinity,
        retry: false,
        gcTime: 0,
      },
    },
  });

  if (preloadedState) {
    hydrate(queryClient, preloadedState as any);
  }

  const trpcClient = trpc.createClient({
    links: [
      httpBatchLink({
        url: "http://localhost:5000/api/trpc",
        transformer: superjson,
      }),
    ],
  });

  const { hook } = memoryLocation({ path: url, static: true });

  const html = renderToString(
    <HelmetProvider context={helmetContext}>
      <trpc.Provider client={trpcClient} queryClient={queryClient}>
        <QueryClientProvider client={queryClient}>
          <ThemeProvider defaultTheme="light">
            <Router hook={hook}>
              <Switch>
                <Route path="/trilha/:id" component={TrailDetail} />
                <Route path="/blog/:slug" component={BlogPost} />
                <Route path="/guia/:id" component={GuideDetail} />
              </Switch>
            </Router>
          </ThemeProvider>
        </QueryClientProvider>
      </trpc.Provider>
    </HelmetProvider>
  );

  return {
    html,
    helmetContext,
    dehydratedState: dehydrate(queryClient),
  };
}
