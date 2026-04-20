import { Backpack } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

interface Props {
  children: React.ReactNode;
  title?: string;
}

export function ArticlePracticalBox({ children, title = "Experiência no Campo" }: Props) {
  return (
    <Card className="my-8 border-l-4 border-l-green-600 border-green-100 bg-green-50/40">
      <CardContent className="p-5">
        <div className="flex items-center gap-2 mb-3">
          <Backpack className="h-5 w-5 text-green-700 shrink-0" />
          <h3 className="font-semibold text-green-800 text-sm uppercase tracking-wide">
            {title}
          </h3>
        </div>
        <div className="text-sm text-green-900/80 leading-relaxed space-y-2">{children}</div>
      </CardContent>
    </Card>
  );
}
