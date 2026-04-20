import { ShieldCheck, RefreshCw, CalendarCheck } from "lucide-react";

interface Props {
  publishedAt?: Date | string | null;
  reviewedAt?: Date | string | null;
  reviewerName?: string | null;
  isHighValue?: boolean;
}

function formatDate(value: Date | string | null | undefined) {
  if (!value) return null;
  return new Date(value).toLocaleDateString("pt-BR", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export function ArticleTrustBlock({ publishedAt, reviewedAt, reviewerName, isHighValue }: Props) {
  const published = formatDate(publishedAt);
  const reviewed = formatDate(reviewedAt);

  if (!published && !reviewed && !isHighValue) return null;

  return (
    <div className="flex flex-wrap items-center gap-x-5 gap-y-2 text-xs text-muted-foreground bg-green-50/60 border border-green-100 rounded-lg px-4 py-3 my-6">
      {isHighValue && (
        <span className="flex items-center gap-1.5 font-medium text-green-700">
          <ShieldCheck className="h-4 w-4 shrink-0" />
          Conteúdo verificado
        </span>
      )}

      {published && (
        <span className="flex items-center gap-1.5">
          <CalendarCheck className="h-4 w-4 shrink-0" />
          Publicado em {published}
        </span>
      )}

      {reviewed && (
        <span className="flex items-center gap-1.5">
          <RefreshCw className="h-4 w-4 shrink-0" />
          Atualizado em {reviewed}
          {reviewerName && (
            <span className="text-green-700 font-medium">por {reviewerName}</span>
          )}
        </span>
      )}
    </div>
  );
}
