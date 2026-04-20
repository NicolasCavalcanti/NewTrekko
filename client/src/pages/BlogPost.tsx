import React from "react";
import { useParams, Link } from "wouter";
import { Helmet } from "react-helmet-async";
import { trpc } from "@/lib/trpc";
import { useBlogPostBySlug, useBlogRelated } from "@/hooks/useBlog";
import { useAuthorBySlug } from "@/hooks/useAuthors";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Badge } from "@/components/ui/badge";
import { AdUnit, AD_SLOTS } from "@/components/AdUnit";
import {
  ArrowLeft,
  Clock,
  Calendar,
  Share2,
  Bookmark,
  ChevronRight,
  Mountain,
  User,
  Award,
  MapPin,
  Map,
  BookOpen,
} from "lucide-react";
import { ArticleFAQBlock } from "@/components/ArticleFAQBlock";
import { ArticleTrustBlock } from "@/components/ArticleTrustBlock";
import { ArticlePracticalBox } from "@/components/ArticlePracticalBox";


const CATEGORY_LABELS: Record<string, string> = {
  "trilhas-destinos": "Trilhas & Destinos",
  "guias-praticos": "Guias Práticos",
  "planejamento-seguranca": "Planejamento & Segurança",
  "equipamentos": "Equipamentos",
  "conservacao-ambiental": "Conservação Ambiental",
  "historias-inspiracao": "Histórias & Inspiração",
};

export default function BlogPost() {
  const { slug } = useParams<{ slug: string }>();

  const { data: post, isLoading, error } = useBlogPostBySlug(slug || "");
  const { data: author } = useAuthorBySlug(post?.authorSlug ?? "");

  const { data: relatedPosts } = useBlogRelated(post?.id, post?.category ?? undefined);

  const handleShare = async () => {
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({
          title: post?.title,
          text: post?.excerpt || "",
          url,
        });
      } catch {
        // User cancelled or error
      }
    } else {
      await navigator.clipboard.writeText(url);
      alert("Link copiado para a área de transferência!");
    }
  };

  const handleSave = () => {
    alert("Artigo salvo nos favoritos!");
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-background">
        <div className="container py-8">
          <Skeleton className="h-8 w-32 mb-8" />
          <Skeleton className="h-64 w-full rounded-xl mb-8" />
          <Skeleton className="h-12 w-3/4 mb-4" />
          <Skeleton className="h-6 w-1/2 mb-8" />
          <div className="space-y-4">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-3/4" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !post) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Artigo não encontrado</h1>
          <p className="text-muted-foreground mb-6">
            O artigo que você procura não existe ou foi removido.
          </p>
          <Link href="/blog">
            <Button>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Voltar ao Blog
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  const publishedDate = post.publishedAt 
    ? new Date(post.publishedAt).toLocaleDateString("pt-BR", {
        day: "numeric",
        month: "long",
        year: "numeric",
      })
    : null;

  // Parse content to render with proper formatting.
  // Injects a mid-article ad unit after the second paragraph.
  const renderContent = (content: string) => {
    const sections = content.split(/\n\n+/);
    const elements: React.ReactNode[] = [];
    let paragraphCount = 0;

    sections.forEach((section, index) => {
      const trimmed = section.trim();
      let isParagraph = false;

      // Check if it's a heading (starts with emoji or specific patterns)
      if (trimmed.match(/^[🎯👥🧱🧭⚠️🔎🎨🧩✅⛰️🌿]/)) {
        elements.push(
          <h2 key={index} className="text-2xl font-bold mt-8 mb-4 text-green-800">
            {trimmed}
          </h2>
        );
      } else if (trimmed.match(/^(A montanha|Onde fica|Um marco|Beleza que|A importância|Não é sobre|Por que|Serra Fina não)/)) {
        // Subheading
        elements.push(
          <h2 key={index} className="text-2xl font-bold mt-8 mb-4 text-green-800">
            {trimmed}
          </h2>
        );
      } else if (trimmed.includes('\n') && trimmed.split('\n').every(line => line.trim().match(/^[-•]/))) {
        // Explicit bullet list
        const items = trimmed.split('\n').filter(line => line.trim());
        elements.push(
          <ul key={index} className="list-disc list-inside space-y-2 my-4 text-muted-foreground">
            {items.map((item, i) => (
              <li key={i}>{item.replace(/^[-•]\s*/, '')}</li>
            ))}
          </ul>
        );
      } else if (trimmed.includes('\n')) {
        // Multiple short lines — treat as list
        const lines = trimmed.split('\n').filter(line => line.trim());
        if (lines.length > 1 && lines.every(line => line.length < 100)) {
          elements.push(
            <ul key={index} className="list-disc list-inside space-y-2 my-4 text-muted-foreground">
              {lines.map((line, i) => (
                <li key={i}>{line.trim()}</li>
              ))}
            </ul>
          );
        } else {
          isParagraph = true;
          elements.push(
            <p key={index} className="text-muted-foreground leading-relaxed mb-4">
              {trimmed}
            </p>
          );
        }
      } else if (trimmed.length < 150 && !trimmed.includes('.') && trimmed.split('\n').length === 1) {
        // Quote-like content
        elements.push(
          <blockquote key={index} className="border-l-4 border-green-600 pl-4 my-6 italic text-lg text-green-800">
            {trimmed}
          </blockquote>
        );
      } else {
        // Regular paragraph
        isParagraph = true;
        elements.push(
          <p key={index} className="text-muted-foreground leading-relaxed mb-4">
            {trimmed}
          </p>
        );
      }

      // Inject mid-article ad after the second paragraph
      if (isParagraph) {
        paragraphCount++;
        if (paragraphCount === 2) {
          elements.push(
            <AdUnit
              key="blog-mid-article"
              slot={AD_SLOTS.BLOG_MID_ARTICLE}
              className="my-6"
            />
          );
        }
      }
    });

    return elements;
  };

  const canonicalUrl = `https://trekko.com.br/blog/${post.slug}`;
  const metaTitle = `${post.title} — Trekko`;
  const metaDescription = post.excerpt || post.title;
  const ogImage = post.imageUrl || "https://trekko.com.br/og-image.jpg";
  const authorUrl = author
    ? `https://trekko.com.br/autor/${author.slug}`
    : undefined;

  const articleSchema = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: post.title,
    description: metaDescription,
    image: ogImage,
    url: canonicalUrl,
    datePublished: post.publishedAt
      ? new Date(post.publishedAt).toISOString()
      : undefined,
    dateModified: (post.reviewedAt ?? post.updatedAt)
      ? new Date((post.reviewedAt ?? post.updatedAt)!).toISOString()
      : undefined,
    publisher: {
      "@type": "Organization",
      name: "Trekko",
      url: "https://trekko.com.br",
      logo: {
        "@type": "ImageObject",
        url: "https://trekko.com.br/android-chrome-512x512.png",
      },
    },
    author: author
      ? {
          "@type": "Person",
          name: author.name,
          url: authorUrl,
          description: author.shortBio,
          jobTitle: author.title,
          ...(author.photoUrl
            ? { image: author.photoUrl }
            : {}),
        }
      : { "@type": "Organization", name: "Trekko" },
  };

  return (
    <div className="min-h-screen bg-background">
      <Helmet>
        <title>{metaTitle}</title>
        <meta name="description" content={metaDescription} />
        <link rel="canonical" href={canonicalUrl} />
        <meta property="og:type" content="article" />
        <meta property="og:title" content={metaTitle} />
        <meta property="og:description" content={metaDescription} />
        <meta property="og:url" content={canonicalUrl} />
        <meta property="og:image" content={ogImage} />
        <meta property="og:site_name" content="Trekko" />
        <meta property="og:locale" content="pt_BR" />
        {post.publishedAt && <meta property="article:published_time" content={new Date(post.publishedAt).toISOString()} />}
        {post.updatedAt && <meta property="article:modified_time" content={new Date(post.updatedAt).toISOString()} />}
        {author && <meta property="article:author" content={authorUrl} />}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={metaTitle} />
        <meta name="twitter:description" content={metaDescription} />
        <meta name="twitter:image" content={ogImage} />
        <script type="application/ld+json">
          {JSON.stringify(articleSchema)}
        </script>
      </Helmet>
      {/* Back Button */}
      <div className="container py-4">
        <Link href="/blog">
          <Button variant="ghost" size="sm">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Voltar ao Blog
          </Button>
        </Link>
      </div>

      {/* Hero Image */}
      <div className="relative h-64 md:h-96 bg-gradient-to-br from-green-800 to-green-900">
        {post.imageUrl ? (
          <img
            src={post.imageUrl}
            alt={post.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="absolute inset-0 flex items-center justify-center">
            <Mountain className="h-24 w-24 text-green-600/30" />
          </div>
        )}
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        
        {/* Category Badge */}
        {post.category && (
          <span className="absolute top-4 left-4 bg-green-700 text-white text-sm px-3 py-1 rounded">
            {CATEGORY_LABELS[post.category] || post.category}
          </span>
        )}
      </div>

      {/* Article Content */}
      <article className="container py-8">
        <div className="max-w-3xl mx-auto">
          {/* Title */}
          <h1 className="text-3xl md:text-4xl font-bold mb-4 text-foreground">
            {post.title}
          </h1>

          {/* Subtitle */}
          {post.subtitle && (
            <p className="text-xl text-muted-foreground mb-6">
              {post.subtitle}
            </p>
          )}

          {/* Author Byline */}
          <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground mb-8 pb-8 border-b">
            {author ? (
              <Link href={`/autor/${author.slug}`} className="flex items-center gap-2 hover:text-foreground transition-colors group">
                {author.photoUrl ? (
                  <img
                    src={author.photoUrl}
                    alt={author.name}
                    className="w-8 h-8 rounded-full object-cover ring-2 ring-green-100"
                  />
                ) : (
                  <span className="w-8 h-8 rounded-full bg-green-700 text-white text-xs font-bold flex items-center justify-center shrink-0">
                    {author.name.split(" ").map((n) => n[0]).slice(0, 2).join("")}
                  </span>
                )}
                <div>
                  <span className="font-medium text-foreground group-hover:text-green-700 transition-colors block leading-tight">
                    {author.name}
                  </span>
                  {author.cadasturNumber && (
                    <span className="text-xs text-green-700 leading-tight block">CADASTUR {author.cadasturNumber}</span>
                  )}
                </div>
              </Link>
            ) : (
              <div className="flex items-center gap-2">
                <User className="h-4 w-4" />
                <span>{post.authorName || "TREKKO"}</span>
              </div>
            )}

            {publishedDate && (
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                <span>{publishedDate}</span>
              </div>
            )}
            <div className="flex items-center gap-2">
              <Clock className="h-4 w-4" />
              <span>{post.readingTime || 5} min de leitura</span>
            </div>

            {/* Actions */}
            <div className="flex gap-2 ml-auto">
              <Button variant="outline" size="sm" onClick={handleShare}>
                <Share2 className="h-4 w-4 mr-2" />
                Compartilhar
              </Button>
              <Button variant="outline" size="sm" onClick={handleSave}>
                <Bookmark className="h-4 w-4 mr-2" />
                Salvar
              </Button>
            </div>
          </div>

          {/* Trust block — published/reviewed signals */}
          <ArticleTrustBlock
            publishedAt={post.publishedAt}
            reviewedAt={post.reviewedAt}
            reviewerName={post.reviewerName}
            isHighValue={!!post.isHighValue}
          />

          {/* Content */}
          <div className="prose prose-lg max-w-none">
            {renderContent(post.content)}
          </div>

          {/* Practical experience callout — shown on high-value articles */}
          {post.isHighValue && author && (
            <ArticlePracticalBox>
              <p>
                Este artigo foi produzido com base em{" "}
                <strong>experiência prática de campo</strong> por{" "}
                <strong>{author.name}</strong>
                {author.yearsExperience
                  ? `, com ${author.yearsExperience} anos de experiência em ecoturismo e trekking no Brasil`
                  : ""}
                {author.location ? `, atuando em ${author.location}` : ""}.
              </p>
              {post.reviewedAt && (
                <p>
                  Conteúdo revisado e atualizado em{" "}
                  {new Date(post.reviewedAt).toLocaleDateString("pt-BR", {
                    month: "long",
                    year: "numeric",
                  })}
                  {post.reviewerName ? ` por ${post.reviewerName}` : ""}.
                </p>
              )}
            </ArticlePracticalBox>
          )}

          {/* Ad unit 2 — end of article */}
          <AdUnit slot={AD_SLOTS.BLOG_END_ARTICLE} className="my-8" />

          {/* Internal links — related trails & guides */}
          {post.isHighValue && (
            <div className="mt-10 pt-8 border-t">
              <div className="flex items-center gap-2 mb-4">
                <BookOpen className="h-5 w-5 text-green-700 shrink-0" />
                <h2 className="text-lg font-bold text-foreground">Continue Explorando</h2>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <Link href="/trilhas">
                  <div className="flex items-center gap-3 p-3 rounded-lg border border-green-100 hover:border-green-300 hover:bg-green-50/50 transition-colors group">
                    <Map className="h-5 w-5 text-green-600 shrink-0" />
                    <div>
                      <p className="text-sm font-medium group-hover:text-green-700 transition-colors">
                        Trilhas no Brasil
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Explore trilhas por dificuldade e região
                      </p>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground ml-auto" />
                  </div>
                </Link>
                <Link href="/guias">
                  <div className="flex items-center gap-3 p-3 rounded-lg border border-green-100 hover:border-green-300 hover:bg-green-50/50 transition-colors group">
                    <Award className="h-5 w-5 text-green-600 shrink-0" />
                    <div>
                      <p className="text-sm font-medium group-hover:text-green-700 transition-colors">
                        Guias Certificados CADASTUR
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Conecte-se com guias experientes
                      </p>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground ml-auto" />
                  </div>
                </Link>
                <Link href="/blog">
                  <div className="flex items-center gap-3 p-3 rounded-lg border border-green-100 hover:border-green-300 hover:bg-green-50/50 transition-colors group">
                    <BookOpen className="h-5 w-5 text-green-600 shrink-0" />
                    <div>
                      <p className="text-sm font-medium group-hover:text-green-700 transition-colors">
                        Guias Práticos
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Planejamento, equipamentos e segurança
                      </p>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground ml-auto" />
                  </div>
                </Link>
                <Link href="/blog?category=planejamento-seguranca">
                  <div className="flex items-center gap-3 p-3 rounded-lg border border-green-100 hover:border-green-300 hover:bg-green-50/50 transition-colors group">
                    <Mountain className="h-5 w-5 text-green-600 shrink-0" />
                    <div>
                      <p className="text-sm font-medium group-hover:text-green-700 transition-colors">
                        Segurança em Trilhas
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Dicas essenciais para trilhar com segurança
                      </p>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground ml-auto" />
                  </div>
                </Link>
              </div>
            </div>
          )}

          {/* FAQ section */}
          {post.faqData && post.faqData.length > 0 && (
            <ArticleFAQBlock
              faqs={post.faqData}
              articleUrl={`https://trekko.com.br/blog/${post.slug}`}
            />
          )}

          {/* Tags */}
          {post.tags && post.tags.length > 0 && (
            <div className="mt-8 pt-8 border-t">
              <h3 className="text-sm font-semibold text-muted-foreground mb-3">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {post.tags.map((tag, i) => (
                  <span
                    key={i}
                    className="bg-green-100 text-green-800 text-sm px-3 py-1 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Author Bio Card */}
          {author && (
            <Card className="mt-8 border-green-100">
              <CardContent className="p-6">
                <h3 className="text-sm font-semibold text-muted-foreground uppercase tracking-wide mb-4">
                  Sobre o autor
                </h3>
                <div className="flex gap-4">
                  {author.photoUrl ? (
                    <img
                      src={author.photoUrl}
                      alt={author.name}
                      className="w-16 h-16 rounded-full object-cover shrink-0 ring-2 ring-green-100"
                    />
                  ) : (
                    <span className="w-16 h-16 rounded-full bg-green-700 text-white text-xl font-bold flex items-center justify-center shrink-0">
                      {author.name.split(" ").map((n) => n[0]).slice(0, 2).join("")}
                    </span>
                  )}
                  <div className="flex-1 min-w-0">
                    <Link href={`/autor/${author.slug}`}>
                      <h4 className="font-bold text-lg hover:text-green-700 transition-colors">
                        {author.name}
                      </h4>
                    </Link>
                    <p className="text-sm text-green-700 font-medium mb-1">{author.title}</p>
                    <div className="flex flex-wrap gap-2 mb-3">
                      {author.cadasturNumber && (
                        <Badge variant="outline" className="text-xs border-green-300 text-green-700 gap-1">
                          <Award className="h-3 w-3" />
                          CADASTUR {author.cadasturNumber}
                        </Badge>
                      )}
                      <Badge variant="outline" className="text-xs border-slate-200 text-muted-foreground gap-1">
                        <MapPin className="h-3 w-3" />
                        {author.location}
                      </Badge>
                      <Badge variant="outline" className="text-xs border-slate-200 text-muted-foreground">
                        {author.yearsExperience} anos de experiência
                      </Badge>
                    </div>
                    <p className="text-sm text-muted-foreground leading-relaxed mb-3">
                      {author.shortBio}
                    </p>
                    <Link href={`/autor/${author.slug}`}>
                      <Button variant="outline" size="sm" className="border-green-600 text-green-700 hover:bg-green-50 text-xs">
                        Ver perfil completo
                        <ChevronRight className="h-3 w-3 ml-1" />
                      </Button>
                    </Link>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* CTA Box */}
          <Card className="mt-8 bg-gradient-to-br from-green-50 to-green-100 border-green-200">
            <CardContent className="p-6">
              <h3 className="text-xl font-bold text-green-800 mb-2">
                Explore mais trilhas no TREKKO
              </h3>
              <p className="text-green-700 mb-4">
                Descubra trilhas incríveis, conecte-se com guias certificados e planeje sua próxima aventura.
              </p>
              <div className="flex flex-wrap gap-3">
                <Link href="/trilhas">
                  <Button className="bg-green-700 hover:bg-green-800">
                    Ver Trilhas
                    <ChevronRight className="h-4 w-4 ml-2" />
                  </Button>
                </Link>
                <Link href="/guias">
                  <Button variant="outline" className="border-green-600 text-green-700 hover:bg-green-50">
                    Conhecer Guias
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>
        </div>
      </article>

      {/* Related Posts */}
      {relatedPosts && relatedPosts.length > 0 && (
        <section className="bg-muted py-12">
          <div className="container">
            <h2 className="text-2xl font-bold mb-6">Artigos Relacionados</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {relatedPosts.map((relatedPost) => (
                <Link key={relatedPost.id} href={`/blog/${relatedPost.slug}`}>
                  <Card className="overflow-hidden h-full hover:shadow-lg transition-shadow cursor-pointer group">
                    <div className="relative h-40 bg-gradient-to-br from-green-700 to-green-900">
                      {relatedPost.imageUrl ? (
                        <img
                          src={relatedPost.imageUrl}
                          alt={relatedPost.title}
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        />
                      ) : (
                        <div className="absolute inset-0 flex items-center justify-center">
                          <Mountain className="h-12 w-12 text-green-500/50" />
                        </div>
                      )}
                    </div>
                    <CardContent className="p-4">
                      <h3 className="font-bold line-clamp-2 group-hover:text-green-700 transition-colors">
                        {relatedPost.title}
                      </h3>
                      <div className="flex items-center gap-1 text-sm text-muted-foreground mt-2">
                        <Clock className="h-4 w-4" />
                        <span>{relatedPost.readingTime || 5} min</span>
                      </div>
                    </CardContent>
                  </Card>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}
