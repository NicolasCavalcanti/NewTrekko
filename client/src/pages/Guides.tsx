import { useState, useEffect } from "react";
import { useLocation } from "wouter";
import { Helmet } from "react-helmet-async";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useDebounce } from "@/_core/hooks/useDebounce";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useGuidesList, useGuideCities } from "@/hooks/useGuides";
import { AdUnit, AD_SLOTS } from "@/components/AdUnit";
import {
  Search, Users, Shield, Loader2, ChevronLeft, ChevronRight,
  MapPin, Phone, Mail, Globe, CheckCircle2, AlertTriangle,
  BookOpen, Award, Star, UserCheck
} from "lucide-react";

const BRAZILIAN_STATES = [
  "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
  "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
];

const HOW_TO_STEPS = [
  {
    icon: Shield,
    title: "Verifique o CADASTUR",
    description:
      "Confirme o número de cadastro diretamente no portal do Ministério do Turismo em cadastur.turismo.gov.br. Um guia certificado tem cobertura de seguro obrigatória e responde legalmente pela condução.",
  },
  {
    icon: BookOpen,
    title: "Leia o perfil com atenção",
    description:
      "Observe as especializações declaradas: trilhas de longa duração, rapel, cachoeiras, wildlife. Guia especializado em alta montanha não é o mesmo que guia de parque urbano.",
  },
  {
    icon: Star,
    title: "Consulte avaliações reais",
    description:
      "Priorize guias com avaliações detalhadas de outros trilheiros. Comentários que descrevem situações concretas — segurança em mau tempo, comunicação em emergências — são mais confiáveis que notas genéricas.",
  },
  {
    icon: UserCheck,
    title: "Converse antes de contratar",
    description:
      "Um bom guia faz perguntas sobre seu condicionamento físico, experiência anterior e objetivos. Fuja de quem vende o serviço sem nenhuma triagem — segurança começa no planejamento.",
  },
  {
    icon: AlertTriangle,
    title: "Atenção ao escopo do serviço",
    description:
      "Verifique o que está incluso: transporte, alimentação, equipamento de segurança, seguro de acidentes pessoais. Contrato por escrito protege as duas partes.",
  },
  {
    icon: Award,
    title: "Valorize a experiência local",
    description:
      "Guias que vivem na região conhecem variações sazonais, condições reais do terreno e alternativas de rota. Esse conhecimento não consta em nenhum aplicativo.",
  },
];

export default function Guides() {
  const [, navigate] = useLocation();
  const [searchText, setSearchText] = useState("");
  const [cadasturCode, setCadasturCode] = useState("");
  const [selectedUF, setSelectedUF] = useState("");
  const [selectedCity, setSelectedCity] = useState("");
  const [page, setPage] = useState(1);

  const debouncedSearch = useDebounce(searchText, 300);
  const debouncedCadasturCode = useDebounce(cadasturCode, 300);

  const { data: cities, isLoading: citiesLoading } = useGuideCities(
    selectedUF && selectedUF !== "all" ? selectedUF : undefined,
  );

  useEffect(() => {
    setSelectedCity("");
    setPage(1);
  }, [selectedUF]);

  useEffect(() => {
    setPage(1);
  }, [debouncedSearch, debouncedCadasturCode]);

  const { data, isLoading } = useGuidesList({
    search: debouncedSearch || undefined,
    cadasturCode: debouncedCadasturCode || undefined,
    uf: selectedUF && selectedUF !== "all" ? selectedUF : undefined,
    city: selectedCity && selectedCity !== "all" ? selectedCity : undefined,
    page,
    limit: 12,
  });

  const totalPages = Math.ceil((data?.total || 0) / 12);

  return (
    <div className="min-h-screen flex flex-col">
      <Helmet>
        <title>Guias de Trilha Certificados CADASTUR — Como Escolher e Contratar | Trekko</title>
        <meta
          name="description"
          content="Aprenda por que contratar um guia de trilha certificado pelo CADASTUR faz diferença na segurança e na experiência. Diretório com mais de 30 mil profissionais verificados em todo o Brasil."
        />
        <link rel="canonical" href="https://trekko.com.br/guias" />
        <meta property="og:type" content="website" />
        <meta property="og:title" content="Guias de Trilha Certificados CADASTUR — Trekko" />
        <meta
          property="og:description"
          content="Encontre guias de trilha certificados pelo CADASTUR em todo o Brasil. Profissionais verificados para garantir segurança e qualidade na sua experiência na natureza."
        />
        <meta property="og:url" content="https://trekko.com.br/guias" />
        <meta property="og:image" content="https://trekko.com.br/og-image.jpg" />
        <meta property="og:site_name" content="Trekko" />
        <meta property="og:locale" content="pt_BR" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Guias de Trilha Certificados CADASTUR — Trekko" />
        <meta
          name="twitter:description"
          content="Encontre guias de trilha certificados pelo CADASTUR em todo o Brasil."
        />
        <meta name="twitter:image" content="https://trekko.com.br/og-image.jpg" />
      </Helmet>
      <Header />

      <main className="flex-1">

        {/* ── Hero editorial ── */}
        <section className="bg-gradient-to-b from-primary/10 to-background py-12 md:py-16">
          <div className="container max-w-3xl">
            <div className="flex items-center gap-2 text-primary text-sm font-medium mb-3">
              <Shield className="w-4 h-4" />
              <span>Certificação CADASTUR — Ministério do Turismo</span>
            </div>
            <h1 className="font-heading text-3xl md:text-4xl lg:text-5xl font-bold text-foreground mb-4 leading-tight">
              Por que contratar um guia de trilha certificado?
            </h1>
            <p className="text-lg text-muted-foreground mb-6 leading-relaxed">
              Trilhar com um guia profissional vai muito além de ter alguém para mostrar o caminho.
              Um bom guia conhece as condições reais do terreno, sabe agir em emergências,
              carrega equipamento de primeiros socorros e — no caso dos certificados pelo CADASTUR —
              está legalmente habilitado e coberto por seguro obrigatório.
            </p>
            <p className="text-muted-foreground leading-relaxed">
              No Brasil, o ecoturismo e as trilhas de aventura cresceram mais de 40% na última
              década. Com isso, cresceu também o número de condutores sem qualificação formal.
              Saber identificar um profissional de verdade pode ser a diferença entre uma
              experiência memorável e um incidente grave.
            </p>
          </div>
        </section>

        {/* ── O que é CADASTUR ── */}
        <section className="py-12 border-b border-border">
          <div className="container max-w-3xl">
            <div className="flex items-start gap-4 mb-6">
              <div className="p-2 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex-shrink-0 mt-1">
                <Award className="w-5 h-5 text-amber-600" />
              </div>
              <div>
                <h2 className="font-heading text-2xl font-bold text-foreground mb-3">
                  O que é o CADASTUR e por que ele importa
                </h2>
                <p className="text-muted-foreground leading-relaxed mb-4">
                  O <strong>CADASTUR</strong> é o Sistema de Cadastro de Pessoas Físicas e Jurídicas
                  que atuam no setor de turismo, mantido pelo Ministério do Turismo. Para guias de
                  turismo, o cadastro é <strong>obrigatório por lei</strong> (Lei 11.771/2008) e
                  precisa ser renovado a cada dois anos.
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                  {[
                    {
                      label: "Seguro obrigatório",
                      detail:
                        "O guia cadastrado é obrigado a manter apólice de seguro de responsabilidade civil, cobrindo acidentes durante a condução.",
                    },
                    {
                      label: "Habilitação legal",
                      detail:
                        "Somente guias com CADASTUR ativo podem cobrar por serviços de condução turística no Brasil. Exercer sem cadastro é infração administrativa.",
                    },
                    {
                      label: "Rastreabilidade",
                      detail:
                        "Em caso de acidente ou reclamação, o número CADASTUR permite identificar e responsabilizar o profissional perante os órgãos de turismo.",
                    },
                  ].map(({ label, detail }) => (
                    <div key={label} className="bg-muted/50 rounded-lg p-4">
                      <p className="font-semibold text-foreground text-sm mb-1">{label}</p>
                      <p className="text-xs text-muted-foreground leading-relaxed">{detail}</p>
                    </div>
                  ))}
                </div>
                <p className="text-sm text-muted-foreground mt-4">
                  Todos os guias listados neste diretório possuem número CADASTUR válido, extraído
                  diretamente da base oficial do Ministério do Turismo.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* ── Como escolher um guia ── */}
        <section className="py-12 bg-muted/30 border-b border-border">
          <div className="container max-w-3xl">
            <div className="mb-8">
              <h2 className="font-heading text-2xl font-bold text-foreground mb-2">
                Como escolher um guia de trilha
              </h2>
              <p className="text-muted-foreground">
                Certificação é o ponto de partida, não o critério único. Considere estes fatores
                antes de confirmar uma contratação.
              </p>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              {HOW_TO_STEPS.map(({ icon: Icon, title, description }) => (
                <div key={title} className="flex items-start gap-3">
                  <div className="p-2 rounded-lg bg-primary/10 flex-shrink-0 mt-0.5">
                    <Icon className="w-4 h-4 text-primary" />
                  </div>
                  <div>
                    <p className="font-semibold text-foreground text-sm mb-1">{title}</p>
                    <p className="text-xs text-muted-foreground leading-relaxed">{description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── Ad slot — entre editorial e diretório ── */}
        <div className="container max-w-3xl py-4">
          <AdUnit slot={AD_SLOTS.GUIDES_AFTER_EDITORIAL} />
        </div>

        {/* ── Diretório de guias ── */}
        <section className="py-10 bg-muted/30">
          <div className="container">
            <div className="mb-6">
              <h2 className="font-heading text-2xl font-bold text-foreground mb-1">
                Diretório de Guias Certificados
              </h2>
              <p className="text-muted-foreground text-sm">
                {data?.total
                  ? `${data.total.toLocaleString("pt-BR")} guias certificados pelo CADASTUR em todo o Brasil`
                  : "Carregando..."}
              </p>
            </div>

            {/* Filtros */}
            <Card className="mb-6">
              <CardContent className="p-4">
                <div className="grid grid-cols-1 md:grid-cols-6 gap-4">
                  <div className="md:col-span-2">
                    <label className="text-sm font-medium text-foreground mb-1 block">Nome do guia</label>
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                      <Input
                        placeholder="Buscar por nome..."
                        className="pl-10"
                        value={searchText}
                        onChange={(e) => setSearchText(e.target.value)}
                      />
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">Ignora maiúsculas e acentos</p>
                  </div>
                  <div>
                    <label className="text-sm font-medium text-foreground mb-1 block">Código CADASTUR</label>
                    <div className="relative">
                      <Shield className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                      <Input
                        placeholder="Ex: 12345678"
                        className="pl-10"
                        value={cadasturCode}
                        onChange={(e) => setCadasturCode(e.target.value)}
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
                    <label className="text-sm font-medium text-foreground mb-1 block">Cidade</label>
                    <Select
                      value={selectedCity}
                      onValueChange={setSelectedCity}
                      disabled={!selectedUF || selectedUF === "all" || citiesLoading}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder={citiesLoading ? "Carregando..." : "Todas"} />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Todas</SelectItem>
                        {cities?.map((city) => (
                          <SelectItem key={city} value={city}>{city}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {(!selectedUF || selectedUF === "all") && (
                      <p className="text-xs text-muted-foreground mt-1">Selecione um estado primeiro</p>
                    )}
                  </div>
                  <div className="flex items-end">
                    <Button className="w-full" onClick={() => setPage(1)}>
                      <Search className="w-4 h-4 mr-2" />
                      Buscar
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Legenda */}
            <div className="flex flex-wrap items-center gap-4 mb-6 text-sm">
              <div className="flex items-center gap-2">
                <Badge variant="default" className="bg-primary">
                  <CheckCircle2 className="w-3 h-3 mr-1" />
                  Verificado
                </Badge>
                <span className="text-muted-foreground">Cadastrado no Trekko</span>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="border-amber-500 text-amber-600">
                  <Shield className="w-3 h-3 mr-1" />
                  CADASTUR
                </Badge>
                <span className="text-muted-foreground">Certificação oficial do Ministério do Turismo</span>
              </div>
            </div>

            {/* Resultados */}
            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
              </div>
            ) : data?.guides.length === 0 ? (
              <div className="text-center py-12">
                <Users className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
                <h3 className="font-heading text-xl font-semibold mb-2">Nenhum guia encontrado</h3>
                <p className="text-muted-foreground">Tente ajustar os filtros de busca</p>
              </div>
            ) : (
              <>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {data?.guides.map((guide) => (
                    <Card
                      key={guide.id}
                      className={`overflow-hidden cursor-pointer hover:shadow-lg transition-shadow ${guide.isVerified ? "ring-2 ring-primary/20" : ""}`}
                      onClick={() => navigate(`/guia/${guide.cadasturNumber}`)}
                    >
                      <CardContent className="p-6">
                        <div className="flex items-start gap-4">
                          <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                            <span className="text-xl font-semibold text-primary">
                              {guide.name?.charAt(0).toUpperCase() || "G"}
                            </span>
                          </div>
                          <div className="flex-1 min-w-0">
                            <h3 className="font-heading font-semibold text-base mb-1 truncate" title={guide.name}>
                              {guide.name || "Guia"}
                            </h3>
                            <div className="flex flex-wrap gap-1 mb-2">
                              {guide.isVerified && (
                                <Badge variant="default" className="bg-primary text-xs">
                                  <CheckCircle2 className="w-3 h-3 mr-1" />
                                  Verificado
                                </Badge>
                              )}
                              <Badge variant="outline" className="border-amber-500 text-amber-600 text-xs">
                                <Shield className="w-3 h-3 mr-1" />
                                CADASTUR
                              </Badge>
                            </div>
                            <div className="flex items-center gap-1 text-sm text-muted-foreground mb-1">
                              <MapPin className="w-3 h-3" />
                              <span className="truncate">
                                {guide.city ? `${guide.city}, ${guide.uf}` : guide.uf}
                              </span>
                            </div>
                            {guide.categories && guide.categories.length > 0 && (
                              <div className="flex flex-wrap gap-1 mt-2">
                                {guide.categories.slice(0, 2).map((cat, i) => (
                                  <Badge key={i} variant="secondary" className="text-xs">
                                    {cat}
                                  </Badge>
                                ))}
                                {guide.categories.length > 2 && (
                                  <Badge variant="secondary" className="text-xs">
                                    +{guide.categories.length - 2}
                                  </Badge>
                                )}
                              </div>
                            )}
                          </div>
                        </div>
                        <div className="mt-4 pt-4 border-t border-border space-y-1">
                          {guide.phone && (
                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                              <Phone className="w-3 h-3" />
                              <span className="truncate">{guide.phone}</span>
                            </div>
                          )}
                          {guide.email && (
                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                              <Mail className="w-3 h-3" />
                              <span className="truncate">{guide.email}</span>
                            </div>
                          )}
                          {guide.website && (
                            <div className="flex items-center gap-2 text-xs text-muted-foreground">
                              <Globe className="w-3 h-3" />
                              <span className="truncate">{guide.website}</span>
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>

                {totalPages > 1 && (
                  <div className="flex items-center justify-center gap-2 mt-8">
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => setPage((p) => Math.max(1, p - 1))}
                      disabled={page === 1}
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </Button>
                    <span className="text-sm text-muted-foreground px-4">
                      Página {page} de {totalPages}
                    </span>
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                      disabled={page === totalPages}
                    >
                      <ChevronRight className="w-4 h-4" />
                    </Button>
                  </div>
                )}
              </>
            )}
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}
