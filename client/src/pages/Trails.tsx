import { useState, useEffect } from "react";
import { useLocation, useSearch } from "wouter";
import { Helmet } from "react-helmet-async";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { trpc } from "@/lib/trpc";
import { useTrailsList, useTrailById } from "@/hooks/useTrails";
import {
  Search, Mountain, MapPin, Calendar, Users, Loader2,
  ChevronLeft, ChevronRight, User, DollarSign, CheckCircle2,
  XCircle, Clock, AlertCircle, Compass, Shield, Route, Download,
} from "lucide-react";
import { format } from "date-fns";
import { ptBR } from "date-fns/locale";
import { USE_SUPABASE } from "@/lib/supabase";
import { sbListPublicExpeditions, type Expedition as SbExpedition } from "@/lib/supabaseExpeditions";

const BRAZILIAN_STATES = [
  "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
  "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
];

const DIFFICULTIES = [
  { value: "easy", label: "Fácil" },
  { value: "moderate", label: "Moderada" },
  { value: "hard", label: "Difícil" },
  { value: "expert", label: "Especialista" },
];

const STATUS_LABELS: Record<string, { label: string; color: string; icon: React.ReactNode }> = {
  active: { label: "Ativa", color: "bg-green-100 text-green-700 border-green-200", icon: <CheckCircle2 className="w-3 h-3" /> },
  full: { label: "Lotada", color: "bg-blue-100 text-blue-700 border-blue-200", icon: <Users className="w-3 h-3" /> },
  closed: { label: "Encerrada", color: "bg-gray-100 text-gray-700 border-gray-200", icon: <XCircle className="w-3 h-3" /> },
  cancelled: { label: "Cancelada", color: "bg-red-100 text-red-700 border-red-200", icon: <AlertCircle className="w-3 h-3" /> },
  draft: { label: "Rascunho", color: "bg-yellow-100 text-yellow-700 border-yellow-200", icon: <Clock className="w-3 h-3" /> },
};

const VALUE_PROPS = [
  {
    icon: Compass,
    title: "Curadoria Editorial",
    description:
      "Cada trilha é verificada e documentada com informações técnicas precisas: distância, ganho de elevação, tempo estimado, pontos de água e dicas de segurança.",
  },
  {
    icon: Shield,
    title: "Guias Certificados CADASTUR",
    description:
      "Conectamos você a profissionais habilitados pelo Ministério do Turismo, com experiência comprovada nas trilhas que conduzem.",
  },
  {
    icon: Download,
    title: "GPX e Mapas Offline",
    description:
      "Baixe a rota GPX antes de sair de casa e navegue com segurança mesmo sem sinal de celular. Disponível para a maioria das trilhas cadastradas.",
  },
  {
    icon: Calendar,
    title: "Expedições Organizadas",
    description:
      "Encontre grupos com data definida, guia confirmado e vagas abertas. Perfeito para quem quer aventura sem se preocupar com a logística.",
  },
];

const DIFFICULTY_GUIDE = [
  {
    level: "Fácil",
    color: "bg-green-100 text-green-800 border-green-200",
    dotColor: "bg-green-500",
    description:
      "Até 8 km, terreno regular e ganho de altitude baixo. Ideal para iniciantes, crianças e quem quer uma caminhada leve no fim de semana.",
  },
  {
    level: "Moderada",
    color: "bg-yellow-100 text-yellow-800 border-yellow-200",
    dotColor: "bg-yellow-500",
    description:
      "Entre 8 e 20 km, com terreno irregular e algum ganho de altitude. Requer boa disposição física, calçado adequado e hidratação constante.",
  },
  {
    level: "Difícil",
    color: "bg-orange-100 text-orange-800 border-orange-200",
    dotColor: "bg-orange-500",
    description:
      "Mais de 15 km ou ganho elevado de altitude. Exige boa capacidade aeróbica, equipamentos de trekking e, em muitos casos, guia profissional.",
  },
  {
    level: "Especialista",
    color: "bg-red-100 text-red-800 border-red-200",
    dotColor: "bg-red-500",
    description:
      "Trilhas técnicas, remotas ou com condições extremas. Recomendado somente para experientes com equipamento completo e acompanhamento especializado.",
  },
];

export default function Trails() {
  const [, navigate] = useLocation();
  const searchParams = useSearch();
  const params = new URLSearchParams(searchParams);

  const [activeTab, setActiveTab] = useState(params.get("tab") || "trilhas");
  const [searchText, setSearchText] = useState(params.get("q") || "");
  const [selectedUF, setSelectedUF] = useState(params.get("uf") || "");
  const [selectedDifficulty, setSelectedDifficulty] = useState(params.get("difficulty") || "");
  const [maxDistance, setMaxDistance] = useState(params.get("distance") || "");
  const [page, setPage] = useState(1);

  // Expedition filters
  const [expSearchText, setExpSearchText] = useState("");
  const [expUF, setExpUF] = useState("");
  const [expStartDate, setExpStartDate] = useState("");
  const [expEndDate, setExpEndDate] = useState("");
  const [expPage, setExpPage] = useState(1);

  const { data: trailsData, isLoading: trailsLoading } = useTrailsList({
    search: searchText || undefined,
    uf: selectedUF && selectedUF !== "all" ? selectedUF : undefined,
    difficulty: selectedDifficulty && selectedDifficulty !== "all" ? selectedDifficulty : undefined,
    maxDistance: maxDistance ? parseInt(maxDistance) : undefined,
    page,
    limit: 12,
  });

  // ── Supabase expeditions ────────────────────────────────────────────────────
  const [sbExpeditions, setSbExpeditions] = useState<SbExpedition[]>([]);
  const [sbExpLoading, setSbExpLoading] = useState(USE_SUPABASE);

  useEffect(() => {
    if (!USE_SUPABASE) return;
    setSbExpLoading(true);
    sbListPublicExpeditions(expSearchText || undefined)
      .then(setSbExpeditions)
      .finally(() => setSbExpLoading(false));
    const handler = () => {
      sbListPublicExpeditions(expSearchText || undefined).then(setSbExpeditions);
    };
    window.addEventListener("supabaseExpeditionsUpdated", handler);
    return () => window.removeEventListener("supabaseExpeditionsUpdated", handler);
  }, [expSearchText]);

  // ── tRPC expeditions (disabled in Supabase mode) ────────────────────────────
  const { data: expeditionsData, isLoading: trpcExpLoading } = trpc.expeditions.list.useQuery({
    search: expSearchText || undefined,
    uf: expUF && expUF !== "all" ? expUF : undefined,
    startDate: expStartDate ? new Date(expStartDate) : undefined,
    endDate: expEndDate ? new Date(expEndDate) : undefined,
    page: expPage,
    limit: 12,
  }, { enabled: !USE_SUPABASE });

  const displayExpeditions: any[] = USE_SUPABASE ? sbExpeditions : (expeditionsData?.expeditions ?? []);
  const expeditionsLoading = USE_SUPABASE ? sbExpLoading : trpcExpLoading;

  const totalTrailPages = Math.ceil((trailsData?.total || 0) / 12);
  const totalExpPages = USE_SUPABASE
    ? Math.ceil(sbExpeditions.length / 12)
    : Math.ceil((expeditionsData?.total || 0) / 12);

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Helmet>
        <title>Trilhas no Brasil: Catálogo Completo de Percursos e Expedições — Trekko</title>
        <meta name="description" content="Descubra centenas de trilhas em todo o Brasil. Filtre por estado, dificuldade e distância. Expedições guiadas com profissionais certificados CADASTUR." />
        <link rel="canonical" href="https://trekko.com.br/trilhas" />
        <meta property="og:type" content="website" />
        <meta property="og:title" content="Trilhas no Brasil: Catálogo Completo de Percursos e Expedições — Trekko" />
        <meta property="og:description" content="Descubra centenas de trilhas em todo o Brasil. Filtre por estado, dificuldade e distância. Expedições guiadas com profissionais certificados CADASTUR." />
        <meta property="og:url" content="https://trekko.com.br/trilhas" />
        <meta property="og:image" content="https://trekko.com.br/og-image.jpg" />
        <meta property="og:site_name" content="Trekko" />
        <meta property="og:locale" content="pt_BR" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Trilhas no Brasil: Catálogo Completo de Percursos e Expedições — Trekko" />
        <meta name="twitter:description" content="Descubra centenas de trilhas em todo o Brasil com guias certificados CADASTUR." />
        <meta name="twitter:image" content="https://trekko.com.br/og-image.jpg" />
      </Helmet>
      <Header />

      <main className="flex-1 py-8">
        <div className="container">

          {/* ── Editorial Hero ────────────────────────────────────────────────── */}
          <section className="relative bg-forest text-white rounded-2xl overflow-hidden mb-8">
            <div className="absolute inset-0 bg-gradient-to-br from-forest via-forest to-forest-light opacity-90" />
            <div className="absolute inset-0 opacity-5" style={{
              backgroundImage: "radial-gradient(circle at 2px 2px, white 1px, transparent 0)",
              backgroundSize: "32px 32px"
            }} />
            <div className="relative px-6 py-12 md:py-16 md:px-12 lg:px-16">
              <div className="max-w-3xl">
                <div className="flex items-center gap-2 text-white/60 mb-4">
                  <Route className="w-4 h-4" />
                  <span className="text-xs font-medium uppercase tracking-widest">Plataforma Nacional de Trilhas</span>
                </div>
                <h1 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold mb-5 text-white leading-tight">
                  Explore as Melhores<br className="hidden sm:block" /> Trilhas do Brasil
                </h1>
                <p className="text-base md:text-lg text-white/80 mb-4 leading-relaxed">
                  O Brasil é um dos países mais ricos em biodiversidade e paisagens naturais do mundo.
                  De norte a sul, são mais de 8,5 milhões de km² repletos de cerrado, mata atlântica,
                  pantanal, amazônia e litoral — um convite permanente para quem busca se reconectar
                  com a natureza.
                </p>
                <p className="text-sm md:text-base text-white/70 mb-8 leading-relaxed">
                  O Trekko reúne trilhas catalogadas em todos os estados, com informações técnicas
                  detalhadas, mapas GPX para download e guias certificados pelo Ministério do Turismo.
                  Seja uma caminhada de fim de semana ou uma expedição de vários dias em trilhas remotas,
                  aqui você encontra tudo que precisa para planejar com segurança.
                </p>

                {/* Stats bar */}
                <div className="flex flex-wrap gap-x-6 gap-y-3">
                  <div className="flex items-center gap-2">
                    <Mountain className="w-4 h-4 text-white/60" />
                    <span className="text-sm font-medium text-white">
                      {trailsData?.total ? `${trailsData.total}+ trilhas cadastradas` : "Centenas de trilhas"}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MapPin className="w-4 h-4 text-white/60" />
                    <span className="text-sm font-medium text-white">27 estados cobertos</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Shield className="w-4 h-4 text-white/60" />
                    <span className="text-sm font-medium text-white">Guias certificados CADASTUR</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Download className="w-4 h-4 text-white/60" />
                    <span className="text-sm font-medium text-white">GPX disponível para download</span>
                  </div>
                </div>
              </div>
            </div>
          </section>

          {/* ── Value Props ───────────────────────────────────────────────────── */}
          <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
            {VALUE_PROPS.map((vp) => (
              <div key={vp.title} className="bg-card border rounded-xl p-5 hover:shadow-md transition-shadow">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-3">
                  <vp.icon className="w-5 h-5 text-primary" />
                </div>
                <h3 className="font-heading font-semibold text-sm mb-2">{vp.title}</h3>
                <p className="text-xs text-muted-foreground leading-relaxed">{vp.description}</p>
              </div>
            ))}
          </section>

          {/* ── How to Choose ─────────────────────────────────────────────────── */}
          <section className="bg-muted/40 border rounded-xl p-6 mb-8">
            <div className="flex items-center gap-2 mb-3">
              <Compass className="w-5 h-5 text-primary" />
              <h2 className="font-heading text-lg font-semibold">Como escolher sua próxima trilha</h2>
            </div>
            <p className="text-sm text-muted-foreground mb-5 leading-relaxed max-w-3xl">
              Escolher a trilha certa faz toda a diferença na experiência. Leve em conta seu
              condicionamento físico, o tempo disponível, a época do ano e se prefere ir de forma
              independente ou com um grupo guiado. Use o guia abaixo como referência antes de aplicar
              os filtros — e lembre-se: toda aventura começa com um bom planejamento.
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
              {DIFFICULTY_GUIDE.map((g) => (
                <div key={g.level} className={`border rounded-lg p-4 ${g.color}`}>
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`w-2.5 h-2.5 rounded-full ${g.dotColor}`} />
                    <span className="text-xs font-semibold uppercase tracking-wide">{g.level}</span>
                  </div>
                  <p className="text-xs leading-relaxed opacity-80">{g.description}</p>
                </div>
              ))}
            </div>
          </section>

          {/* ── Catalog Divider ───────────────────────────────────────────────── */}
          <div id="catalogo" className="flex items-center gap-4 mb-6">
            <div className="flex-1 h-px bg-border" />
            <span className="font-heading text-sm font-semibold text-muted-foreground uppercase tracking-widest whitespace-nowrap px-2">
              Catálogo
            </span>
            <div className="flex-1 h-px bg-border" />
          </div>

          {/* ── Catalog Tabs ──────────────────────────────────────────────────── */}
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="mb-6">
              <TabsTrigger value="trilhas" className="flex items-center gap-2">
                <Mountain className="w-4 h-4" />
                Trilhas
              </TabsTrigger>
              <TabsTrigger value="expedicoes" className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                Expedições
              </TabsTrigger>
            </TabsList>

            {/* Trails Tab */}
            <TabsContent value="trilhas">
              {/* Search Filters */}
              <Card className="mb-6">
                <CardContent className="p-4">
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                    <div className="md:col-span-2">
                      <label className="text-sm font-medium text-foreground mb-1 block">Buscar</label>
                      <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <Input
                          placeholder="Nome da trilha..."
                          className="pl-10"
                          value={searchText}
                          onChange={(e) => setSearchText(e.target.value)}
                        />
                      </div>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-foreground mb-1 block">Estado</label>
                      <Select value={selectedUF} onValueChange={setSelectedUF}>
                        <SelectTrigger>
                          <SelectValue placeholder="Todos" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Todos</SelectItem>
                          {BRAZILIAN_STATES.map((uf) => (
                            <SelectItem key={uf} value={uf}>{uf}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-foreground mb-1 block">Dificuldade</label>
                      <Select value={selectedDifficulty} onValueChange={setSelectedDifficulty}>
                        <SelectTrigger>
                          <SelectValue placeholder="Todas" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Todas</SelectItem>
                          {DIFFICULTIES.map((d) => (
                            <SelectItem key={d.value} value={d.value}>{d.label}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-foreground mb-1 block">Distância máx.</label>
                      <Input
                        type="number"
                        placeholder="km"
                        value={maxDistance}
                        onChange={(e) => setMaxDistance(e.target.value)}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Results */}
              {trailsLoading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
              ) : !trailsData || trailsData.trails.length === 0 ? (
                <div className="text-center py-12">
                  <Mountain className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                  <h3 className="font-heading text-xl font-semibold mb-2">Nenhuma trilha encontrada</h3>
                  <p className="text-muted-foreground">Tente ajustar os filtros de busca</p>
                </div>
              ) : (
                <>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {trailsData?.trails.map((trail) => (
                      <Card
                        key={trail.id}
                        className="overflow-hidden cursor-pointer hover:shadow-lg transition-shadow group"
                        onClick={() => navigate(`/trilha/${trail.id}`)}
                      >
                        <div className="h-48 bg-gradient-to-br from-forest/20 to-forest-light/20 relative overflow-hidden">
                          {trail.imageUrl ? (
                            <img
                              src={trail.imageUrl}
                              alt={trail.name}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center">
                              <Mountain className="w-12 h-12 text-forest/40" />
                            </div>
                          )}
                          <div className="absolute top-2 right-2">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              trail.difficulty === 'easy' ? 'bg-green-500 text-white' :
                              trail.difficulty === 'moderate' ? 'bg-yellow-500 text-white' :
                              trail.difficulty === 'hard' ? 'bg-orange-500 text-white' :
                              'bg-red-500 text-white'
                            }`}>
                              {trail.difficulty === 'easy' ? 'Fácil' :
                               trail.difficulty === 'moderate' ? 'Moderada' :
                               trail.difficulty === 'hard' ? 'Difícil' : 'Especialista'}
                            </span>
                          </div>
                          {trail.guideRequired === 1 && (
                            <div className="absolute top-2 left-2">
                              <span className="px-2 py-1 rounded-full text-xs font-medium bg-orange-500 text-white">
                                Guia Obrigatório
                              </span>
                            </div>
                          )}
                        </div>
                        <CardContent className="p-4">
                          <h3 className="font-heading font-semibold text-lg mb-1">{trail.name}</h3>
                          <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
                            <MapPin className="w-4 h-4" />
                            <span>{trail.city}, {trail.uf}</span>
                          </div>
                          {trail.shortDescription && (
                            <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
                              {trail.shortDescription}
                            </p>
                          )}
                          <div className="flex items-center gap-4 text-xs text-muted-foreground">
                            {trail.distanceKm && (
                              <span className="flex items-center gap-1">
                                <Mountain className="w-3 h-3" />
                                {trail.distanceKm} km
                              </span>
                            )}
                            {trail.elevationGain && (
                              <span>↑ {trail.elevationGain}m</span>
                            )}
                            {trail.estimatedTime && (
                              <span>{trail.estimatedTime}</span>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>

                  {/* Pagination */}
                  {totalTrailPages > 1 && (
                    <div className="flex items-center justify-center gap-2 mt-8">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setPage(p => Math.max(1, p - 1))}
                        disabled={page === 1}
                      >
                        <ChevronLeft className="w-4 h-4" />
                      </Button>
                      <span className="text-sm text-muted-foreground px-4">
                        Página {page} de {totalTrailPages}
                      </span>
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setPage(p => Math.min(totalTrailPages, p + 1))}
                        disabled={page === totalTrailPages}
                      >
                        <ChevronRight className="w-4 h-4" />
                      </Button>
                    </div>
                  )}
                </>
              )}
            </TabsContent>

            {/* Expeditions Tab */}
            <TabsContent value="expedicoes">
              {/* Search Filters */}
              <Card className="mb-6">
                <CardContent className="p-4">
                  <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                    <div className="md:col-span-2">
                      <label className="text-sm font-medium text-foreground mb-1 block">Buscar</label>
                      <div className="relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                        <Input
                          placeholder="Trilha ou guia..."
                          className="pl-10"
                          value={expSearchText}
                          onChange={(e) => setExpSearchText(e.target.value)}
                        />
                      </div>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-foreground mb-1 block">Estado</label>
                      <Select value={expUF} onValueChange={setExpUF}>
                        <SelectTrigger>
                          <SelectValue placeholder="Todos" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">Todos</SelectItem>
                          {BRAZILIAN_STATES.map((uf) => (
                            <SelectItem key={uf} value={uf}>{uf}</SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <label className="text-sm font-medium text-foreground mb-1 block">Data início</label>
                      <Input
                        type="date"
                        value={expStartDate}
                        onChange={(e) => setExpStartDate(e.target.value)}
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium text-foreground mb-1 block">Data fim</label>
                      <Input
                        type="date"
                        value={expEndDate}
                        onChange={(e) => setExpEndDate(e.target.value)}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Results */}
              {expeditionsLoading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-8 h-8 animate-spin text-primary" />
                </div>
              ) : displayExpeditions.length === 0 ? (
                <div className="text-center py-12">
                  <Calendar className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                  <h3 className="font-heading text-xl font-semibold mb-2">Nenhuma expedição encontrada</h3>
                  <p className="text-muted-foreground">Tente ajustar os filtros ou volte mais tarde</p>
                </div>
              ) : (
                <>
                  <div className="space-y-4">
                    {displayExpeditions.map((expedition) => (
                      <ExpeditionCard key={expedition.id} expedition={expedition} />
                    ))}
                  </div>

                  {/* Pagination */}
                  {totalExpPages > 1 && (
                    <div className="flex items-center justify-center gap-2 mt-8">
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setExpPage(p => Math.max(1, p - 1))}
                        disabled={expPage === 1}
                      >
                        <ChevronLeft className="w-4 h-4" />
                      </Button>
                      <span className="text-sm text-muted-foreground px-4">
                        Página {expPage} de {totalExpPages}
                      </span>
                      <Button
                        variant="outline"
                        size="icon"
                        onClick={() => setExpPage(p => Math.min(totalExpPages, p + 1))}
                        disabled={expPage === totalExpPages}
                      >
                        <ChevronRight className="w-4 h-4" />
                      </Button>
                    </div>
                  )}
                </>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </main>

      <Footer />
    </div>
  );
}

function ExpeditionCard({ expedition }: { expedition: any }) {
  const [, navigate] = useLocation();
  // Static hook works in both Supabase and tRPC modes; tRPC query kept as
  // fallback for non-Supabase mode where numeric guideId is available.
  const { data: staticTrail } = useTrailById(expedition.trailId ?? 0);
  const { data: trailData } = trpc.trails.getById.useQuery(
    { id: expedition.trailId },
    { enabled: !USE_SUPABASE },
  );
  const { data: guideData } = trpc.user.getById.useQuery(
    { id: expedition.guideId },
    { enabled: !USE_SUPABASE && typeof expedition.guideId === "number" },
  );

  // Always prefer static trail image (available without a backend)
  const trailImageUrl = staticTrail?.trail?.imageUrl ?? trailData?.trail?.imageUrl ?? null;

  const capacity = expedition.capacity || 10;
  const availableSpots = expedition.availableSpots !== undefined
    ? expedition.availableSpots
    : capacity - (expedition.enrolledCount || 0);
  const enrolledCount = expedition.enrolledCount ?? (capacity - availableSpots);
  const status = expedition.status || 'active';
  const statusInfo = STATUS_LABELS[status] || STATUS_LABELS.active;

  return (
    <Card
      className="overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
      onClick={() => navigate(`/expedicao/${expedition.id}`)}
    >
      <CardContent className="p-0">
        <div className="flex flex-col lg:flex-row">
          {/* Trail Image */}
          <div className="lg:w-64 h-48 lg:h-auto bg-gradient-to-br from-forest/20 to-forest-light/20 relative flex-shrink-0">
            {trailImageUrl ? (
              <img
                src={trailImageUrl}
                alt={expedition.trailName ?? "Trilha"}
                className="w-full h-full object-cover"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center">
                <Mountain className="w-12 h-12 text-forest/40" />
              </div>
            )}
            {/* Status Badge */}
            <div className="absolute top-3 left-3">
              <Badge className={`${statusInfo.color} border flex items-center gap-1`}>
                {statusInfo.icon}
                {statusInfo.label}
              </Badge>
            </div>
          </div>

          {/* Content */}
          <div className="flex-1 p-6">
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="mb-4">
                <h3 className="font-heading font-semibold text-xl mb-2">
                  {expedition.title || expedition.trailName || trailData?.trail?.name || "Expedição"}
                </h3>
                <div className="flex flex-wrap items-center gap-3 text-sm text-muted-foreground">
                  {trailData?.trail && (
                    <span className="flex items-center gap-1">
                      <MapPin className="w-4 h-4 text-primary" />
                      {trailData.trail.city}, {trailData.trail.uf}
                    </span>
                  )}
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4 text-primary" />
                    {format(new Date(expedition.startDate), "dd 'de' MMMM 'de' yyyy", { locale: ptBR })}
                    {expedition.endDate && expedition.endDate !== expedition.startDate && (
                      <> - {format(new Date(expedition.endDate), "dd/MM/yyyy")}</>
                    )}
                  </span>
                </div>
              </div>

              {/* Guide Info */}
              <div className="flex items-center gap-3 mb-4 p-3 bg-muted/50 rounded-lg">
                <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center overflow-hidden">
                  {guideData?.photoUrl ? (
                    <img src={guideData.photoUrl} alt={guideData.name || ''} className="w-full h-full object-cover" />
                  ) : (
                    <User className="w-5 h-5 text-primary" />
                  )}
                </div>
                <div>
                  <p className="text-sm font-medium">Guia: {guideData?.name || expedition.guideName || 'Carregando...'}</p>
                  {guideData?.cadasturNumber && (
                    <p className="text-xs text-muted-foreground">CADASTUR: {guideData.cadasturNumber}</p>
                  )}
                </div>
              </div>

              {/* Stats */}
              <div className="flex flex-wrap items-center gap-6 mt-auto">
                {/* Capacity */}
                <div className="flex items-center gap-2">
                  <Users className="w-5 h-5 text-muted-foreground" />
                  <div>
                    <p className="text-sm font-medium">
                      {enrolledCount}/{capacity} inscritos
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {availableSpots > 0 ? `${availableSpots} vagas disponíveis` : 'Sem vagas'}
                    </p>
                  </div>
                </div>

                {/* Price */}
                {expedition.price && (
                  <div className="flex items-center gap-2">
                    <DollarSign className="w-5 h-5 text-muted-foreground" />
                    <div>
                      <p className="text-lg font-heading font-bold text-primary">
                        R$ {parseFloat(expedition.price).toFixed(2)}
                      </p>
                      <p className="text-xs text-muted-foreground">por pessoa</p>
                    </div>
                  </div>
                )}

                {/* CTA */}
                <div className="ml-auto">
                  <Button
                    size="lg"
                    disabled={status !== 'active' || availableSpots <= 0}
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(`/expedicao/${expedition.id}`);
                    }}
                  >
                    {status === 'full' || availableSpots <= 0 ? 'Lotada' :
                     status === 'closed' ? 'Encerrada' :
                     status === 'cancelled' ? 'Cancelada' : 'Ver Detalhes'}
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
