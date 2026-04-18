import { createContext, useContext, useState, useCallback, type ReactNode } from "react";

interface AdReadinessContextValue {
  readyForLocation: string | null;
  markContentReady: (path: string) => void;
}

const AdReadinessContext = createContext<AdReadinessContextValue>({
  readyForLocation: null,
  markContentReady: () => {},
});

export function AdReadinessProvider({ children }: { children: ReactNode }) {
  const [readyForLocation, setReadyForLocation] = useState<string | null>(null);
  const markContentReady = useCallback(
    (path: string) => setReadyForLocation(path),
    []
  );

  return (
    <AdReadinessContext.Provider value={{ readyForLocation, markContentReady }}>
      {children}
    </AdReadinessContext.Provider>
  );
}

export function useAdReadiness() {
  return useContext(AdReadinessContext);
}
