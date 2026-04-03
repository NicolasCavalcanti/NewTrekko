/**
 * TrailMap — lazy-loaded Wikiloc map integration (RF-01 to RF-10).
 *
 * States:
 *  idle      → component not yet in viewport
 *  searching → resolveWiklocMap query running
 *  found     → wiklocId resolved, embed shown
 *  fallback  → no result, Wikiloc search card shown
 */
import { useEffect, useRef, useState } from "react";
import { Map, Download, ExternalLink, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { trpc } from "@/lib/trpc";
import { toast } from "sonner";

const STATIC_NO_API =
  import.meta.env.VITE_STATIC_MODE === "true" &&
  !import.meta.env.VITE_API_URL;

interface TrailMapProps {
  trailId: number;
  trailName: string;
  /** Pre-fetched wiklocUrl from trail data (may be null in static mode). */
  wiklocUrl?: string | null;
  /** Pre-fetched gpxUrl from trail data. */
  gpxUrl?: string | null;
}

function extractWiklocId(url: string): string | null {
  const m = url.match(/-(\d+)$/);
  return m ? m[1] : null;
}

export function TrailMap({ trailId, trailName, wiklocUrl, gpxUrl }: TrailMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [inViewport, setInViewport] = useState(false);
  const [downloading, setDownloading] = useState(false);

  // Pre-computed from trail data (avoids extra network round-trip when already known)
  const existingId = wiklocUrl ? extractWiklocId(wiklocUrl) : null;

  // Intersection Observer — trigger when container is within 200 px of viewport
  useEffect(() => {
    if (existingId || STATIC_NO_API) {
      setInViewport(true);
      return;
    }
    const el = containerRef.current;
    if (!el) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setInViewport(true);
          observer.disconnect();
        }
      },
      { rootMargin: "200px" }
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, [existingId]);

  // Only run the resolveWiklocMap query once in viewport, and only if no local ID
  const resolveQuery = trpc.trails.resolveWiklocMap.useQuery(
    { trailId },
    { enabled: !STATIC_NO_API && inViewport && !existingId, staleTime: Infinity }
  );

  // Derive final values
  const wiklocId: string | null =
    existingId ??
    resolveQuery.data?.wiklocId ??
    null;

  const finalWiklocUrl: string | null =
    wiklocUrl ??
    resolveQuery.data?.wiklocUrl ??
    null;

  const finalGpxUrl: string | null =
    gpxUrl ??
    resolveQuery.data?.gpxUrl ??
    null;

  const embedUrl = wiklocId
    ? `https://www.wikiloc.com/wikiloc/embedv2.do?id=${wiklocId}`
    : null;

  const isSearching = !STATIC_NO_API && inViewport && !existingId && resolveQuery.isLoading;
  const settled = existingId ? true : resolveQuery.isFetched || STATIC_NO_API;

  const handleDownload = async () => {
    if (!finalGpxUrl) return;
    setDownloading(true);
    const apiBase = import.meta.env.VITE_API_URL ?? "";
    try {
      const res = await fetch(`${apiBase}/api/trilhas/${trailId}/mapa-offline`);
      if (!res.ok) throw new Error((await res.json()).error || "Erro ao baixar mapa");
      const blob = await res.blob();
      const blobUrl = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = blobUrl;
      a.download =
        res.headers.get("Content-Disposition")?.split('filename="')[1]?.replace('"', "") ||
        `trekko-mapa-offline-${trailName}.gpx`;
      document.body.appendChild(a);
      a.click();
      URL.revokeObjectURL(blobUrl);
      document.body.removeChild(a);
      toast.success("Mapa offline baixado com sucesso!");
    } catch (err: any) {
      toast.error(err.message || "Erro ao baixar mapa offline");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div ref={containerRef}>
      {/* schema.org/Map for SEO */}
      {finalWiklocUrl && (
        <script type="application/ld+json">{JSON.stringify({
          "@context": "https://schema.org",
          "@type": "Map",
          "name": `Mapa da Trilha ${trailName}`,
          "url": finalWiklocUrl,
          "mapType": "https://schema.org/SeismicMap",
        })}</script>
      )}

      {/* Searching state */}
      {isSearching && (
        <div className="flex flex-col items-center justify-center gap-3 py-12 text-muted-foreground">
          <Loader2 className="w-8 h-8 animate-spin text-forest" />
          <span className="text-sm">Buscando mapa da trilha no Wikiloc…</span>
        </div>
      )}

      {/* Wikiloc embed */}
      {!isSearching && settled && embedUrl && (
        <>
          <div className="relative w-full rounded-lg overflow-hidden border border-muted mb-4">
            <iframe
              src={embedUrl}
              className="w-full"
              style={{ height: 450 }}
              loading="lazy"
              title={`Mapa da Trilha ${trailName}`}
              allowFullScreen
            />
          </div>

          <div className="flex flex-wrap items-center gap-3 mb-3">
            {finalGpxUrl && (
              <Button
                onClick={handleDownload}
                disabled={downloading}
                className="bg-forest hover:bg-forest-light"
              >
                {downloading ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <Download className="w-4 h-4 mr-2" />
                )}
                Baixar GPX offline
              </Button>
            )}
            {finalWiklocUrl && (
              <Button asChild variant="outline">
                <a href={finalWiklocUrl} target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="w-4 h-4 mr-2" />
                  Ver trilha no Wikiloc
                </a>
              </Button>
            )}
          </div>

          <p className="text-xs text-muted-foreground flex items-center gap-1">
            Traçado e mapa GPX baseados em trilha do{" "}
            <a
              href={finalWiklocUrl ?? "https://pt.wikiloc.com"}
              target="_blank"
              rel="noopener noreferrer"
              className="text-forest hover:text-forest-light inline-flex items-center gap-1"
            >
              Wikiloc
              <ExternalLink className="w-3 h-3" />
            </a>
          </p>
        </>
      )}

      {/* Fallback — no map found */}
      {!isSearching && settled && !embedUrl && (
        <div className="rounded-lg border border-orange-200 bg-orange-50 p-6 text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            <Map className="w-6 h-6 text-orange-500" />
            <span className="font-semibold text-orange-800">
              Mapa GPX disponível no Wikiloc
            </span>
          </div>
          <p className="text-sm text-muted-foreground mb-5">
            O traçado completo e o arquivo GPX para download desta trilha estão disponíveis no Wikiloc.
          </p>
          <Button asChild className="bg-orange-500 hover:bg-orange-600 text-white">
            <a
              href={`https://pt.wikiloc.com/pesquisar/trilhas?q=${encodeURIComponent(trailName)}&act=trekking`}
              target="_blank"
              rel="noopener noreferrer"
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              Ver mapa no Wikiloc
            </a>
          </Button>
        </div>
      )}
    </div>
  );
}
