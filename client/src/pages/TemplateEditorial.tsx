import { Helmet } from "react-helmet-async";
import { Link } from "wouter";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  ChevronRight,
  CheckCircle2,
  Circle,
  BookOpen,
  Image,
  User,
  ShieldCheck,
  HelpCircle,
  Link2,
  Star,
  FileText,
  Backpack,
  RefreshCw,
  AlertTriangle,
} from "lucide-react";

interface Section {
  id: string;
  label: string;
  required: boolean;
  description: string;
  icon: React.ReactNode;
  minWords?: number;
}

const ARTICLE_SECTIONS: Section[] = [
  {
    id: "hero",
    label: "Imagem Hero",
    required: true,
    description:
      "Foto original ou licenciada da trilha/destino. Mínimo 1200×630 px, alt text descritivo, arquivo <200 KB.",
    icon: <Image className="h-4 w-4" />,
  },
  {
    id: "meta",
    label: "Título + Subtítulo",
    required: true,
    description:
      "Título principal em H1 (50–70 caracteres). Subtítulo complementar que amplia o contexto sem repetir o título.",
    icon: <FileText className="h-4 w-4" />,
  },
  {
    id: "byline",
    label: "Autoria & Metadados",
    required: true,
    description:
      "Foto do autor, nome com link para perfil, data de publicação, data da última revisão, tempo de leitura e CADASTUR (quando aplicável).",
    icon: <User className="h-4 w-4" />,
  },
  {
    id: "trust",
    label: "Bloco de Confiança (Trust Block)",
    required: true,
    description:
      'Barra de sinais editoriais: "Conteúdo verificado", data de publicação e data da última revisão com nome do revisor.',
    icon: <ShieldCheck className="h-4 w-4" />,
  },
  {
    id: "intro",
    label: "Introdução",
    required: true,
    description:
      "150–250 palavras. Deve responder QUEM, O QUE, ONDE, QUANDO e POR QUE em linguagem envolvente. Sem spoilers do conteúdo.",
    icon: <BookOpen className="h-4 w-4" />,
    minWords: 150,
  },
  {
    id: "context",
    label: "Seção de Contexto / Localização",
    required: true,
    description:
      "Onde fica, como chegar, mapa incorporado ou link para GPS. Infraestrutura e pontos de apoio (estacionamento, trilha de acesso, água).",
    icon: <BookOpen className="h-4 w-4" />,
    minWords: 200,
  },
  {
    id: "practical",
    label: "Bloco de Experiência Prática",
    required: true,
    description:
      'Callout destacado com relato de primeira mão ou verificação in loco do autor. Sinaliza experiência real — diferencial de E-E-A-T.',
    icon: <Backpack className="h-4 w-4" />,
  },
  {
    id: "guide",
    label: "Guia Detalhado / How-to",
    required: true,
    description:
      "Seção principal com subtítulos H2/H3. Inclui dados técnicos (distância, desnível, dificuldade), itinerário passo a passo e pontos de interesse.",
    icon: <BookOpen className="h-4 w-4" />,
    minWords: 600,
  },
  {
    id: "tips",
    label: "Dicas & Recomendações",
    required: true,
    description:
      "Lista formatada com dicas práticas: melhor época, equipamentos essenciais, alimentação, hospedagem próxima e dicas insider do autor.",
    icon: <Star className="h-4 w-4" />,
    minWords: 150,
  },
  {
    id: "safety",
    label: "Segurança & Meio Ambiente",
    required: true,
    description:
      "Riscos específicos da trilha/destino, sinalização de guia obrigatório (quando aplicável), Princípios LNT e contatos de emergência locais.",
    icon: <AlertTriangle className="h-4 w-4" />,
    minWords: 150,
  },
  {
    id: "internal-links",
    label: "Links Internos Relacionados",
    required: true,
    description:
      "Mínimo 4 links internos: trilhas relacionadas, guias certificados, outros artigos da categoria. Âncoras descritivas (sem 'clique aqui').",
    icon: <Link2 className="h-4 w-4" />,
  },
  {
    id: "faq",
    label: "Seção FAQ",
    required: true,
    description:
      "Mínimo 4 perguntas respondidas. Marcação JSON-LD FAQPage para rich snippets no Google. Perguntas baseadas em dúvidas reais da comunidade.",
    icon: <HelpCircle className="h-4 w-4" />,
  },
  {
    id: "author-bio",
    label: "Cartão de Autoria",
    required: true,
    description:
      "Foto, nome, título profissional, CADASTUR, localização, anos de experiência, bio curta (2–3 frases) e link para perfil completo.",
    icon: <User className="h-4 w-4" />,
  },
  {
    id: "review-note",
    label: "Nota de Revisão",
    required: true,
    description:
      "Data da última revisão editorial, nome do revisor e escopo da atualização (ex: \"condições de acesso verificadas em Março 2025\").",
    icon: <RefreshCw className="h-4 w-4" />,
  },
  {
    id: "cta",
    label: "CTA — Explorar Trekko",
    required: true,
    description:
      "Bloco de chamada para ação com links para Trilhas, Guias e Expedições. Ancoragem contextual ao tema do artigo.",
    icon: <ChevronRight className="h-4 w-4" />,
  },
  {
    id: "related",
    label: "Artigos Relacionados",
    required: true,
    description: "Grid com 3 artigos da mesma categoria ou tema próximo. Cards com imagem, título e tempo de leitura.",
    icon: <BookOpen className="h-4 w-4" />,
  },
];

const OPTIONAL_ELEMENTS = [
  {
    label: "Galeria de Imagens",
    description: "3–6 fotos adicionais com legendas descritivas. Recomendado para trilhas e destinos.",
  },
  {
    label: "Mapa Interativo / Embed",
    description: "Google Maps embed ou link para rastreio GPS (Wikiloc, AllTrails). Agrega muito valor para navegação.",
  },
  {
    label: "Tabela Comparativa",
    description: "Útil em artigos de equipamentos ou comparação de trilhas por dificuldade, custo ou época.",
  },
  {
    label: "Vídeo Incorporado",
    description: "Vídeo do YouTube do próprio autor ou de parceiro licenciado. Aumenta tempo na página.",
  },
  {
    label: "Checklist Imprimível",
    description: "Lista de checagem de equipamentos ou preparação para a trilha. Alto valor para o usuário.",
  },
  {
    label: "Aviso de Temporada",
    description:
      "Banner alertando sobre fechamento temporário, alta temporada ou restrições específicas do período atual.",
  },
];

const CHECKLIST = [
  "Mínimo de 2.000 palavras de conteúdo original",
  "Pelo menos 1 imagem hero + 2 imagens no corpo",
  "Autoria identificada com credenciais visíveis",
  "Data de publicação E data de revisão visíveis",
  "Trust Block ativo (isHighValue = true)",
  "Bloco de Experiência Prática preenchido",
  "Mínimo 4 links internos contextuais",
  "FAQ com mínimo 4 perguntas + JSON-LD FAQPage",
  "JSON-LD Article com author, datePublished, dateModified",
  "metaTitle (50–60 chars) e metaDescription (150–160 chars)",
  "Tags relevantes (3–7 tags)",
  "Artigos relacionados (3 artigos da mesma categoria)",
  "CTA block com links para trilhas e guias",
];

export default function TemplateEditorial() {
  return (
    <div className="min-h-screen flex flex-col">
      <Helmet>
        <title>Template Editorial — Padrão de Artigo High Value | Trekko</title>
        <meta
          name="description"
          content="Padrão editorial oficial da Trekko para artigos de alto valor. Estrutura obrigatória, elementos essenciais e checklist de publicação para conteúdo de ecoturismo e trekking."
        />
        <link rel="canonical" href="https://trekko.com.br/template-editorial" />
        <meta name="robots" content="index, follow" />
      </Helmet>

      <Header />

      <main className="flex-1">
        {/* Breadcrumb */}
        <nav className="bg-muted/50 border-b" aria-label="Breadcrumb">
          <div className="container py-3">
            <ol className="flex items-center gap-2 text-sm flex-wrap">
              <li>
                <Link href="/" className="text-muted-foreground hover:text-foreground transition-colors">
                  Início
                </Link>
              </li>
              <ChevronRight className="w-4 h-4 text-muted-foreground shrink-0" />
              <li>
                <Link href="/politica-editorial" className="text-muted-foreground hover:text-foreground transition-colors">
                  Política Editorial
                </Link>
              </li>
              <ChevronRight className="w-4 h-4 text-muted-foreground shrink-0" />
              <li>
                <span className="text-foreground font-medium">Template High Value</span>
              </li>
            </ol>
          </div>
        </nav>

        {/* Hero */}
        <section className="bg-gradient-to-br from-green-900 via-green-800 to-green-700 text-white py-16">
          <div className="container">
            <div className="max-w-3xl">
              <Badge className="bg-green-600/80 text-white border-0 mb-4">Padrão Editorial Trekko</Badge>
              <h1 className="font-heading text-4xl md:text-5xl font-bold mb-4 leading-tight">
                Template Oficial de Artigo High Value
              </h1>
              <p className="text-lg text-white/80 leading-relaxed">
                Estrutura obrigatória, elementos de confiança e checklist de publicação para artigos que
                maximizam valor para o leitor, autoridade de domínio e receita AdSense.
              </p>
              <div className="flex flex-wrap gap-4 mt-6 text-sm text-white/70">
                <span>Extensão mínima: <strong className="text-white">2.000 palavras</strong></span>
                <span>Seções obrigatórias: <strong className="text-white">{ARTICLE_SECTIONS.length}</strong></span>
                <span>Checklist: <strong className="text-white">{CHECKLIST.length} itens</strong></span>
              </div>
            </div>
          </div>
        </section>

        <div className="container py-12 max-w-5xl space-y-16">

          {/* 1. Estrutura oficial */}
          <section>
            <h2 className="text-2xl font-bold mb-2">1. Estrutura Oficial do Artigo</h2>
            <p className="text-muted-foreground mb-6">
              Todas as seções abaixo são <strong>obrigatórias</strong> em artigos classificados como{" "}
              <code className="bg-muted px-1.5 py-0.5 rounded text-sm">isHighValue = true</code>. A
              sequência deve ser respeitada para garantir fluxo de leitura e cobertura completa dos sinais
              E-E-A-T (Experiência, Expertise, Autoridade, Confiança).
            </p>

            <div className="space-y-3">
              {ARTICLE_SECTIONS.map((section, i) => (
                <Card key={section.id} className="border-green-100">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <div className="flex items-center justify-center w-7 h-7 rounded-full bg-green-100 text-green-700 font-bold text-xs shrink-0 mt-0.5">
                        {i + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-wrap items-center gap-2 mb-1">
                          <span className="font-semibold text-foreground">{section.label}</span>
                          <Badge
                            variant="outline"
                            className="text-xs border-green-300 text-green-700 gap-1"
                          >
                            {section.icon}
                            Obrigatório
                          </Badge>
                          {section.minWords && (
                            <Badge variant="secondary" className="text-xs">
                              mín. {section.minWords} palavras
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {section.description}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* 2. Elementos desejáveis */}
          <section>
            <h2 className="text-2xl font-bold mb-2">2. Elementos Desejáveis</h2>
            <p className="text-muted-foreground mb-6">
              Não obrigatórios, mas aumentam significativamente o tempo na página, o engajamento e a
              percepção de profundidade. Recomendados para artigos de destinos e trilhas principais.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {OPTIONAL_ELEMENTS.map((el) => (
                <Card key={el.label} className="border-slate-200">
                  <CardContent className="p-4">
                    <div className="flex items-start gap-3">
                      <Circle className="h-4 w-4 text-slate-400 shrink-0 mt-0.5" />
                      <div>
                        <p className="font-medium text-sm mb-1">{el.label}</p>
                        <p className="text-xs text-muted-foreground leading-relaxed">
                          {el.description}
                        </p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* 3. Padrões de extensão e SEO */}
          <section>
            <h2 className="text-2xl font-bold mb-6">3. Padrões de Extensão & SEO</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                { label: "Extensão mínima", value: "2.000 palavras", note: "Ideal: 2.500–3.500 palavras" },
                { label: "Meta Title", value: "50–60 caracteres", note: "Incluir palavra-chave principal" },
                { label: "Meta Description", value: "150–160 caracteres", note: "CTA implícito ao final" },
                { label: "Links internos", value: "Mínimo 4", note: "Âncoras descritivas e contextuais" },
                { label: "FAQ mínimo", value: "4 perguntas", note: "Recomendado: 6–8 perguntas" },
                { label: "Imagens", value: "Hero + 2 no corpo", note: "Alt text descritivo em todas" },
              ].map((item) => (
                <Card key={item.label} className="border-green-100 bg-green-50/30">
                  <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground mb-1">{item.label}</p>
                    <p className="text-xl font-bold text-green-800 mb-1">{item.value}</p>
                    <p className="text-xs text-muted-foreground">{item.note}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          </section>

          {/* 4. Elementos visuais e blocos de confiança */}
          <section>
            <h2 className="text-2xl font-bold mb-6">4. Elementos Visuais & Blocos de Confiança</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold mb-3 text-green-800">Elementos Visuais</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  {[
                    "Imagem hero 1200×630 px, formato paisagem",
                    "Imagens no corpo com figcaption/alt descritivos",
                    "Callout boxes com ícones (dicas, alertas, experiência)",
                    "Listas com marcadores para escaneabilidade",
                    "Tabelas quando comparar opções (equipamentos, trilhas)",
                    "Blockquotes para citações de especialistas",
                    "Cards de links internos com ícone e descrição",
                  ].map((item) => (
                    <li key={item} className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-green-600 shrink-0 mt-0.5" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-3 text-green-800">Blocos de Confiança (Trust Signals)</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  {[
                    "Trust Block com ícone ShieldCheck e datas visíveis",
                    "Badge CADASTUR no byline e no cartão do autor",
                    "Anos de experiência do autor em destaque",
                    "Bloco de Experiência Prática com relato de campo",
                    "Nota de revisão com nome do revisor e data",
                    "JSON-LD Article + FAQPage para rich snippets",
                    "Link para Política Editorial no footer",
                  ].map((item) => (
                    <li key={item} className="flex items-start gap-2">
                      <ShieldCheck className="h-4 w-4 text-green-600 shrink-0 mt-0.5" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </section>

          {/* 5. Checklist de publicação */}
          <section>
            <h2 className="text-2xl font-bold mb-2">5. Checklist de Publicação</h2>
            <p className="text-muted-foreground mb-6">
              Valide todos os itens antes de alterar o status para <code className="bg-muted px-1.5 py-0.5 rounded text-sm">published</code> e
              marcar <code className="bg-muted px-1.5 py-0.5 rounded text-sm">isHighValue = true</code>.
            </p>
            <Card className="border-green-100">
              <CardContent className="p-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {CHECKLIST.map((item) => (
                    <div key={item} className="flex items-start gap-2 text-sm">
                      <CheckCircle2 className="h-4 w-4 text-green-600 shrink-0 mt-0.5" />
                      <span className="text-muted-foreground">{item}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </section>

          {/* 6. Exemplo de template */}
          <section>
            <h2 className="text-2xl font-bold mb-2">6. Exemplo de Template (Esqueleto)</h2>
            <p className="text-muted-foreground mb-6">
              Estrutura de conteúdo de referência para artigos de trilhas e destinos. Adapte os títulos ao
              tema específico do artigo.
            </p>
            <Card className="border-green-100 bg-slate-50/50">
              <CardContent className="p-6">
                <pre className="text-sm text-slate-700 whitespace-pre-wrap leading-relaxed font-mono overflow-x-auto">
{`# [Título Principal — Palavra-chave Primária + Contexto Local]
## [Subtítulo que amplia: benefício ou detalhe relevante]

📍 Autoria: [Nome do Autor] | CADASTUR [XXXXXXX]
📅 Publicado: [Data] | Revisado: [Data] por [Revisor]
⏱ Tempo de leitura: [X] min

━━━━━━━━━━━━━━━━━━━━━━━━
✅ BLOCO DE CONFIANÇA (Trust Block)
━━━━━━━━━━━━━━━━━━━━━━━━

## Introdução (150–250 palavras)
[Gancho emocional + quem, o quê, onde, quando e por quê]

━━━━━━━━━━━━━━━━━━━━━━━━
[AD — MEIO DO ARTIGO]
━━━━━━━━━━━━━━━━━━━━━━━━

## Onde Fica e Como Chegar
[Localização, acesso, mapa, distâncias das cidades principais]

## Dados Técnicos
- Distância total: X km
- Desnível acumulado: X m
- Dificuldade: [Fácil / Moderada / Difícil / Extrema]
- Melhor época: [Meses]
- Requer guia: [Sim / Não / Recomendado]

🏕 BLOCO DE EXPERIÊNCIA PRÁTICA
[Relato de campo do autor — verificado in loco]

## Itinerário Detalhado
[Seção passo a passo, H2/H3 por trecho ou ponto de interesse]

## Dicas Essenciais
- [Dica 1]
- [Dica 2]
- ...

## Segurança & Meio Ambiente
[Riscos, equipamentos obrigatórios, LNT, contatos de emergência]

━━━━━━━━━━━━━━━━━━━━━━━━
🔗 LINKS INTERNOS RELACIONADOS
━━━━━━━━━━━━━━━━━━━━━━━━

## Perguntas Frequentes
Q: [Pergunta 1]
A: [Resposta 1]
... (mín. 4 perguntas)

[TAGS]

📖 CARTÃO DO AUTOR

📅 NOTA DE REVISÃO

📢 CTA — EXPLORE MAIS NO TREKKO

━━━━━━━━━━━━━━━━━━━━━━━━
[AD — FIM DO ARTIGO]
━━━━━━━━━━━━━━━━━━━━━━━━

📰 ARTIGOS RELACIONADOS (3 cards)`}
                </pre>
              </CardContent>
            </Card>
          </section>

          {/* Link para Política Editorial */}
          <section className="pb-4">
            <Card className="border-green-200 bg-green-50/40">
              <CardContent className="p-6 flex flex-col sm:flex-row items-start sm:items-center gap-4">
                <BookOpen className="h-8 w-8 text-green-700 shrink-0" />
                <div className="flex-1">
                  <h3 className="font-semibold text-green-800 mb-1">Política Editorial Completa</h3>
                  <p className="text-sm text-muted-foreground">
                    Consulte os princípios editoriais, processo de verificação e critérios de qualidade que
                    norteiam todo o conteúdo da Trekko.
                  </p>
                </div>
                <Link href="/politica-editorial">
                  <div className="flex items-center gap-2 text-sm font-medium text-green-700 hover:text-green-800 transition-colors whitespace-nowrap">
                    Ver política
                    <ChevronRight className="h-4 w-4" />
                  </div>
                </Link>
              </CardContent>
            </Card>
          </section>
        </div>
      </main>

      <Footer />
    </div>
  );
}
