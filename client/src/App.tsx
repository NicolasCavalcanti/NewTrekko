import { Toaster } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { lazy, Suspense } from "react";
import { Route, Switch } from "wouter";
import ErrorBoundary from "./components/ErrorBoundary";
import { PageSkeleton } from "./components/PageSkeleton";
import { ThemeProvider } from "./contexts/ThemeContext";
import { HelmetProvider } from "react-helmet-async";

const Home = lazy(() => import("./pages/Home"));
const Trails = lazy(() => import("./pages/Trails"));
const TrailDetail = lazy(() => import("./pages/TrailDetail"));
const Guides = lazy(() => import("./pages/Guides"));
const GuideDetail = lazy(() => import("./pages/GuideDetail"));
const Profile = lazy(() => import("./pages/Profile"));
const Admin = lazy(() => import("./pages/Admin"));
const About = lazy(() => import("./pages/About"));
const ExpeditionDetail = lazy(() => import("./pages/ExpeditionDetail"));
const Blog = lazy(() => import("./pages/Blog"));
const BlogPost = lazy(() => import("./pages/BlogPost"));
const Reservations = lazy(() => import("./pages/Reservations"));
const Terms = lazy(() => import("./pages/Terms"));
const Privacy = lazy(() => import("./pages/Privacy"));
const EditorialPolicy = lazy(() => import("./pages/EditorialPolicy"));
const Contact = lazy(() => import("./pages/Contact"));
const NotFound = lazy(() => import("./pages/NotFound"));

function Router() {
  return (
    <Suspense fallback={<PageSkeleton />}>
      <Switch>
        <Route path="/" component={Home} />
        <Route path="/trilhas" component={Trails} />
        <Route path="/trilha/:id" component={TrailDetail} />
        <Route path="/expedicao/:id" component={ExpeditionDetail} />
        <Route path="/guias" component={Guides} />
        <Route path="/guia/:id" component={GuideDetail} />
        <Route path="/perfil" component={Profile} />
        <Route path="/admin" component={Admin} />
        <Route path="/sobre" component={About} />
        <Route path="/blog" component={Blog} />
        <Route path="/blog/:slug" component={BlogPost} />
        <Route path="/reservas" component={Reservations} />
        <Route path="/termos" component={Terms} />
        <Route path="/privacidade" component={Privacy} />
        <Route path="/politica-editorial" component={EditorialPolicy} />
        <Route path="/contato" component={Contact} />
        <Route path="/404" component={NotFound} />
        <Route component={NotFound} />
      </Switch>
    </Suspense>
  );
}

function App() {
  return (
    <ErrorBoundary>
      <HelmetProvider>
        <ThemeProvider defaultTheme="light">
          <TooltipProvider>
            <Toaster />
            <Router />
          </TooltipProvider>
        </ThemeProvider>
      </HelmetProvider>
    </ErrorBoundary>
  );
}

export default App;
