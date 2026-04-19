import { useParams, Link } from "wouter";
import { Helmet } from "react-helmet-async";
import { useAuthorBySlug } from "@/hooks/useAuthors";
import { useAllStaticPostsPublic } from "@/hooks/useBlog";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import {
  ArrowLeft,
  Award,
  MapPin,
  Clock,
  Mountain,
  BookOpen,
  ChevronRight,
} from "lucide-react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

const CATEGORY_LABELS: Record<string, string> = {
  "trilhas-destinos": "Trilhas & Destinos",
  "guias-praticos": "Guias Práticos",
  "planejamento-seguranca": "Planejamento & Segurança",
  "equipamentos": "Equipamentos",
  "conservacao-ambiental": "Conservação Ambiental",
  "historias-inspiracao": "Histórias & Inspiração",
};

export default function AuthorDetail() {
  const { slug } = useParams<{ slug: string }>();
  const { data: author, isLoading } = useAuthorBySlug(slug ?? "");
  const { data: allPosts } = useAllStaticPostsPublic();

  const authorPosts =
    author && allPosts
      ? allPosts.filter((p) => author.postIds.includes(p.id))
      : [];

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <Header />
        <main className="flex-1 py-12">
          <div className="container max-w-3xl">
            <Skeleton className="h-6 w-24 mb-8" />
            <div className="flex gap-6 mb-8">
              <Skeleton className="w-24 h-24 rounded-full shrink-0" />
              <div className="flex-1 space-y-3">
                <Skeleton className="h-8 w-48" />
                <Skeleton className="h-4 w-64" />
                <Skeleton className="h-4 w-32" />
              </div>
            </div>
            <Skeleton className="h-32 w-full" />
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  if (!author) {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <h1 className="text-2xl font-bold mb-4">Autor não encontrado</h1>
            <Link href="/blog">
              <Button>
                <ArrowLeft className="h-4 w-4 mr-2" />
                Voltar ao Blog
              </Button>
            </Link>
          </div>
        </main>
        <Footer />
      </div>
    );
  }

  const canonicalUrl = `https://trekko.com.br/autor/${author.slug}`;
  const metaTitle = `${author.name} — Autor no Trekko`;
  const metaDescription = author.shortBio;

  const personSchema = {
    "@context": "https://schema.org",
    "@type": "Person",
    name: author.name,
    url: canonicalUrl,
    description: author.bio,
    jobTitle: author.title,
    worksFor: { "@type": "Organization", name: "Trekko", url: "https://trekko.com.br" },
    address: { "@type": "PostalAddress", addressLocality: author.location, addressCountry: "BR" },
    ...(author.photoUrl ? { image: author.photoUrl } : {}),
    knowsAbout: author.specialty,
  };

  const initials = author.name
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("");

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <Helmet>
        <title>{metaTitle}</title>
        <meta name="description" content={metaDescription} />
        <link rel="canonical" href={canonicalUrl} />
        <meta property="og:type" content="profile" />
        <meta property="og:title" content={metaTitle} />
        <meta property="og:description" content={metaDescription} />
        <meta property="og:url" content={canonicalUrl} />
        <meta property="og:site_name" content="Trekko" />
        <script type="application/ld+json">{JSON.stringify(personSchema)}</script>
      </Helmet>

      <Header />

      <main className="flex-1 py-12">
        <div className="container max-w-3xl">
          {/* Back */}
          <Link href="/blog">
            <Button variant="ghost" size="sm" className="mb-8">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Blog
            </Button>
          </Link>

          {/* Author Hero */}
          <div className="flex flex-col sm:flex-row gap-6 mb-10 pb-10 border-b">
            {author.photoUrl ? (
              <img
                src={author.photoUrl}
                alt={author.name}
                className="w-24 h-24 rounded-full object-cover ring-4 ring-green-100 shrink-0"
              />
            ) : (
              <span className="w-24 h-24 rounded-full bg-green-700 text-white text-3xl font-bold flex items-center justify-center shrink-0">
                {initials}
              </span>
            )}
            <div className="flex-1">
              <h1 className="font-heading text-3xl font-bold mb-1">{author.name}</h1>
              <p className="text-green-700 font-medium mb-3">{author.title}</p>
              <div className="flex flex-wrap gap-2 mb-4">
                {author.cadasturNumber && (
                  <Badge className="bg-green-700 text-white gap-1 text-xs">
                    <Award className="h-3 w-3" />
                    CADASTUR {author.cadasturNumber}
                  </Badge>
                )}
                <Badge variant="outline" className="text-xs gap-1">
                  <MapPin className="h-3 w-3" />
                  {author.location}
                </Badge>
                <Badge variant="outline" className="text-xs">
                  {author.yearsExperience} anos de experiência
                </Badge>
                <Badge variant="outline" className="text-xs">
                  {author.trailsCount}+ trilhas percorridas
                </Badge>
              </div>

              {/* Specialty tags */}
              <div className="flex flex-wrap gap-1.5">
                {author.specialty.map((s) => (
                  <span
                    key={s}
                    className="text-xs bg-green-50 text-green-800 border border-green-200 px-2 py-0.5 rounded-full"
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Full Bio */}
          <section className="mb-10">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-green-700" />
              Sobre {author.name.split(" ")[0]}
            </h2>
            {author.bio.split("\n\n").map((paragraph, i) => (
              <p key={i} className="text-muted-foreground leading-relaxed mb-4">
                {paragraph}
              </p>
            ))}
          </section>

          {/* Articles by this author */}
          {authorPosts.length > 0 && (
            <section>
              <h2 className="text-lg font-semibold mb-6 flex items-center gap-2">
                <Mountain className="h-5 w-5 text-green-700" />
                Artigos de {author.name.split(" ")[0]}
              </h2>
              <div className="space-y-4">
                {authorPosts.map((post) => (
                  <Link key={post.id} href={`/blog/${post.slug}`}>
                    <Card className="overflow-hidden hover:shadow-md transition-shadow cursor-pointer group">
                      <CardContent className="p-0 flex">
                        {post.imageUrl && (
                          <div className="w-28 sm:w-40 shrink-0">
                            <img
                              src={post.imageUrl}
                              alt={post.title}
                              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                            />
                          </div>
                        )}
                        <div className="p-4 flex-1">
                          {post.category && (
                            <span className="text-xs text-green-700 font-medium uppercase tracking-wide">
                              {CATEGORY_LABELS[post.category] ?? post.category}
                            </span>
                          )}
                          <h3 className="font-bold mt-1 mb-2 group-hover:text-green-700 transition-colors line-clamp-2">
                            {post.title}
                          </h3>
                          {post.excerpt && (
                            <p className="text-sm text-muted-foreground line-clamp-2 mb-2">
                              {post.excerpt}
                            </p>
                          )}
                          <div className="flex items-center gap-3 text-xs text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Clock className="h-3 w-3" />
                              {post.readingTime || 5} min
                            </span>
                            {post.publishedAt && (
                              <span>
                                {new Date(post.publishedAt).toLocaleDateString("pt-BR", {
                                  day: "numeric",
                                  month: "short",
                                  year: "numeric",
                                })}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center pr-4">
                          <ChevronRight className="h-5 w-5 text-muted-foreground group-hover:text-green-700 transition-colors" />
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                ))}
              </div>
            </section>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}
