import { useState, useRef, useEffect, useCallback } from "react";
import { useLocation, useSearch } from "wouter";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { trpc } from "@/lib/trpc";
import { useAuth } from "@/_core/hooks/useAuth";
import { staticUpdateProfile, staticSetPhoto, staticRemovePhoto } from "@/lib/staticAuth";

const STATIC_NO_API =
  import.meta.env.VITE_STATIC_MODE === "true" && !import.meta.env.VITE_API_URL;
import { getLoginUrl } from "@/const";
import { useTrailsList, useTrailById } from "@/hooks/useTrails";
import { User, Heart, Star, Calendar, Plus, Edit, Trash2, Shield, Mountain, MapPin, Loader2, Upload, X, Wallet, Receipt } from "lucide-react";
import GuideFinancialPanel from "@/components/GuideFinancialPanel";
import UserReservationsPanel from "@/components/UserReservationsPanel";
import { toast } from "sonner";
import { format } from "date-fns";
import { USE_SUPABASE } from "@/lib/supabase";
import {
  sbListGuideExpeditions,
  sbCreateExpedition,
  sbUpdateExpedition,
  sbDeleteExpedition,
} from "@/lib/supabaseExpeditions";

export default function Profile() {
  const [, navigate] = useLocation();
  const searchParams = useSearch();
  const params = new URLSearchParams(searchParams);
  const { user, isAuthenticated, loading } = useAuth();
  
  const [activeTab, setActiveTab] = useState(params.get("tab") || "atividades");
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [expeditionDialogOpen, setExpeditionDialogOpen] = useState(false);

  if (loading) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 flex items-center justify-center">
          <Loader2 className="w-8 h-8 animate-spin text-primary" />
        </main>
        <Footer />
      </div>
    );
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex flex-col">
        <Header />
        <main className="flex-1 flex items-center justify-center bg-muted/30">
          <Card className="max-w-md w-full mx-4">
            <CardContent className="p-8 text-center">
              <User className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
              <h2 className="font-heading text-2xl font-bold mb-2">Acesso restrito</h2>
              <p className="text-muted-foreground mb-6">
                Faça login para acessar seu perfil
              </p>
              <Button asChild className="w-full">
                <a href={getLoginUrl()}>Entrar</a>
              </Button>
            </CardContent>
          </Card>
        </main>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />

      <main className="flex-1 bg-muted/30">
        <div className="container py-8">
          {/* Profile Header */}
          <Card className="mb-8">
            <CardContent className="p-6">
              <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                <div className="w-24 h-24 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
                  {user?.photoUrl ? (
                    <img src={user.photoUrl} alt="" className="w-24 h-24 rounded-full object-cover" />
                  ) : (
                    <span className="text-3xl font-semibold text-primary">
                      {user?.name?.charAt(0).toUpperCase() || "U"}
                    </span>
                  )}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h1 className="font-heading text-2xl font-bold">{user?.name || "Usuário"}</h1>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      user?.userType === 'guide' ? 'bg-primary/10 text-primary' : 'bg-muted text-muted-foreground'
                    }`}>
                      {user?.userType === 'guide' ? 'Guia' : 'Trekker'}
                    </span>
                    {user?.cadasturValidated === 1 && (
                      <span className="flex items-center gap-1 px-2 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium">
                        <Shield className="w-3 h-3" />
                        CADASTUR
                      </span>
                    )}
                  </div>
                  <p className="text-muted-foreground">{user?.email}</p>
                  {user?.bio && <p className="text-sm mt-2">{user.bio}</p>}
                </div>
                <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
                  <DialogTrigger asChild>
                    <Button variant="outline">
                      <Edit className="w-4 h-4 mr-2" />
                      Editar perfil
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-md">
                    <DialogHeader>
                      <DialogTitle>Editar perfil</DialogTitle>
                    </DialogHeader>
                    <EditProfileForm onClose={() => setEditDialogOpen(false)} />
                  </DialogContent>
                </Dialog>
              </div>
            </CardContent>
          </Card>

          {/* Tabs */}
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="mb-6">
              <TabsTrigger value="atividades">
                <Star className="w-4 h-4 mr-2" />
                Atividades
              </TabsTrigger>
              <TabsTrigger value="favoritos">
                <Heart className="w-4 h-4 mr-2" />
                Favoritos
              </TabsTrigger>
              <TabsTrigger value="reservas">
                <Receipt className="w-4 h-4 mr-2" />
                Minhas Reservas
              </TabsTrigger>
              {user?.userType === 'guide' && (
                <TabsTrigger value="expedicoes">
                  <Calendar className="w-4 h-4 mr-2" />
                  Expedições
                </TabsTrigger>
              )}
              {user?.userType === 'guide' && (
                <TabsTrigger value="financeiro">
                  <Wallet className="w-4 h-4 mr-2" />
                  Financeiro
                </TabsTrigger>
              )}
            </TabsList>

            <TabsContent value="atividades">
              <Card>
                <CardContent className="p-8 text-center">
                  <Star className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="font-heading text-lg font-semibold mb-2">Suas atividades</h3>
                  <p className="text-muted-foreground">
                    Suas atividades e avaliações aparecerão aqui
                  </p>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="favoritos">
              <FavoritesList />
            </TabsContent>

            <TabsContent value="reservas">
              <UserReservationsPanel />
            </TabsContent>

            {user?.userType === 'guide' && (
              <TabsContent value="expedicoes">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="font-heading text-xl font-semibold">Minhas Expedições</h2>
                  <Dialog open={expeditionDialogOpen} onOpenChange={setExpeditionDialogOpen}>
                    <DialogTrigger asChild>
                      <Button>
                        <Plus className="w-4 h-4 mr-2" />
                        Criar Expedição
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="max-w-lg" onPointerDownOutside={(e) => e.preventDefault()} onInteractOutside={(e) => e.preventDefault()}>
                      <DialogHeader>
                        <DialogTitle>Criar nova expedição</DialogTitle>
                      </DialogHeader>
                      <CreateExpeditionForm onClose={() => setExpeditionDialogOpen(false)} />
                    </DialogContent>
                  </Dialog>
                </div>
                <GuideExpeditions />
              </TabsContent>
            )}
            {user?.userType === 'guide' && (
              <TabsContent value="financeiro">
                <GuideFinancialPanel />
              </TabsContent>
            )}
          </Tabs>
        </div>
      </main>

      <Footer />
    </div>
  );
}

function EditProfileForm({ onClose }: { onClose: () => void }) {
  const { user } = useAuth();
  const [name, setName] = useState(user?.name || "");
  const [email, setEmail] = useState(user?.email || "");
  const [bio, setBio] = useState(user?.bio || "");
  const [cadasturNumber, setCadasturNumber] = useState(user?.cadasturNumber || "");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const utils = trpc.useUtils();
  const [uploading, setUploading] = useState(false);

  const updateMutation = trpc.user.updateProfile.useMutation({
    onSuccess: () => {
      utils.auth.me.invalidate();
      toast.success("Perfil atualizado!");
      onClose();
    },
    onError: () => {
      toast.error("Erro ao atualizar perfil");
    },
  });

  const uploadMutation = trpc.user.uploadPhoto.useMutation({
    onSuccess: () => {
      utils.auth.me.invalidate();
      toast.success("Foto atualizada!");
    },
    onError: (error) => {
      toast.error(error.message || "Erro ao enviar foto");
    },
  });

  const removeMutation = trpc.user.removePhoto.useMutation({
    onSuccess: () => {
      utils.auth.me.invalidate();
      toast.success("Foto removida!");
    },
  });

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      toast.error("Arquivo muito grande. Máximo 5MB.");
      return;
    }

    if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
      toast.error("Formato inválido. Use JPG, PNG ou GIF.");
      return;
    }

    if (STATIC_NO_API) {
      setUploading(true);
      const reader = new FileReader();
      reader.onload = () => {
        staticSetPhoto(reader.result as string);
        toast.success("Foto atualizada!");
        setUploading(false);
      };
      reader.readAsDataURL(file);
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      const base64 = (reader.result as string).split(',')[1];
      uploadMutation.mutate({
        base64,
        mimeType: file.type as 'image/jpeg' | 'image/png' | 'image/gif',
      });
    };
    reader.readAsDataURL(file);
  };

  const handleRemovePhoto = () => {
    if (STATIC_NO_API) {
      staticRemovePhoto();
      toast.success("Foto removida!");
      return;
    }
    removeMutation.mutate();
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (STATIC_NO_API) {
      staticUpdateProfile({ name, email, bio, cadasturNumber: cadasturNumber || undefined });
      toast.success("Perfil atualizado!");
      onClose();
      return;
    }
    updateMutation.mutate({ name, email, bio, cadasturNumber: cadasturNumber || undefined });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Photo Upload */}
      <div className="flex items-center gap-4">
        <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
          {user?.photoUrl ? (
            <img src={user.photoUrl} alt="" className="w-20 h-20 rounded-full object-cover" />
          ) : (
            <span className="text-2xl font-semibold text-primary">
              {user?.name?.charAt(0).toUpperCase() || "U"}
            </span>
          )}
        </div>
        <div className="flex-1">
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/jpeg,image/png,image/gif"
            className="hidden"
          />
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => fileInputRef.current?.click()}
            disabled={uploadMutation.isPending || uploading}
          >
            {(uploadMutation.isPending || uploading) ? (
              <Loader2 className="w-4 h-4 animate-spin mr-2" />
            ) : (
              <Upload className="w-4 h-4 mr-2" />
            )}
            Enviar foto
          </Button>
          {user?.photoUrl && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="ml-2 text-destructive"
              onClick={handleRemovePhoto}
              disabled={removeMutation.isPending}
            >
              <X className="w-4 h-4 mr-1" />
              Remover
            </Button>
          )}
          <p className="text-xs text-muted-foreground mt-1">JPG, PNG ou GIF. Máx 5MB.</p>
        </div>
      </div>

      <div>
        <Label htmlFor="name">Nome</Label>
        <Input id="name" value={name} onChange={(e) => setName(e.target.value)} />
      </div>
      <div>
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <Label htmlFor="bio">Bio</Label>
        <Textarea id="bio" value={bio} onChange={(e) => setBio(e.target.value)} rows={3} />
      </div>
      {user?.userType === 'guide' && (
        <div>
          <Label htmlFor="cadastur">Número CADASTUR</Label>
          <Input id="cadastur" value={cadasturNumber} onChange={(e) => setCadasturNumber(e.target.value)} />
        </div>
      )}
      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onClose}>Cancelar</Button>
        <Button type="submit" disabled={updateMutation.isPending}>
          {updateMutation.isPending ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
          Salvar
        </Button>
      </div>
    </form>
  );
}

function FavoritesList() {
  const [, navigate] = useLocation();
  const { user } = useAuth();
  const FAVORITES_KEY = `trekko_favorites_${user?.id ?? "guest"}`;

  // Backend mode
  const { data: favorites, isLoading } = trpc.favorites.list.useQuery(
    undefined,
    { enabled: !STATIC_NO_API }
  );

  // Static mode: load IDs from localStorage then resolve full trail objects
  const [staticFavorites, setStaticFavorites] = useState<any[]>([]);
  const [staticLoading, setStaticLoading] = useState(STATIC_NO_API);

  const loadStaticFavorites = useCallback(async () => {
    if (!STATIC_NO_API) return;
    setStaticLoading(true);
    try {
      const ids: number[] = JSON.parse(localStorage.getItem(FAVORITES_KEY) ?? "[]");
      if (ids.length === 0) { setStaticFavorites([]); setStaticLoading(false); return; }
      const base = import.meta.env.BASE_URL ?? "/";
      const res = await fetch(`${base}data/trails.json`.replace("//", "/"));
      const all: any[] = res.ok ? await res.json() : [];
      setStaticFavorites(all.filter((t) => ids.includes(Number(t.id))));
    } catch {
      setStaticFavorites([]);
    } finally {
      setStaticLoading(false);
    }
  }, [FAVORITES_KEY]);

  useEffect(() => {
    loadStaticFavorites();
    window.addEventListener("staticFavoritesUpdated", loadStaticFavorites);
    return () => window.removeEventListener("staticFavoritesUpdated", loadStaticFavorites);
  }, [loadStaticFavorites]);

  const displayFavorites = STATIC_NO_API ? staticFavorites : favorites;
  const loading = STATIC_NO_API ? staticLoading : isLoading;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!displayFavorites || displayFavorites.length === 0) {
    return (
      <Card>
        <CardContent className="p-8 text-center">
          <Heart className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="font-heading text-lg font-semibold mb-2">Nenhuma trilha favoritada</h3>
          <p className="text-muted-foreground mb-4">
            Explore trilhas e adicione aos favoritos
          </p>
          <Button onClick={() => navigate("/trilhas")}>Explorar trilhas</Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {displayFavorites.map((trail: any) => (
        <Card
          key={trail?.id}
          className="overflow-hidden cursor-pointer hover:shadow-lg transition-shadow"
          onClick={() => navigate(`/trilha/${trail?.id}`)}
        >
          <div className="h-32 bg-gradient-to-br from-forest/20 to-forest-light/20 flex items-center justify-center overflow-hidden">
            {trail?.imageUrl ? (
              <img src={trail.imageUrl} alt={trail.name} className="w-full h-full object-cover" />
            ) : (
              <Mountain className="w-10 h-10 text-forest/40" />
            )}
          </div>
          <CardContent className="p-4">
            <h3 className="font-heading font-semibold mb-1">{trail?.name}</h3>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <MapPin className="w-4 h-4" />
              {trail?.city}, {trail?.uf}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

function GuideExpeditions() {
  const { user } = useAuth();
  const expeditionsKey = `trekko_expeditions_${user?.id ?? "guest"}`;

  // ── Supabase mode ──────────────────────────────────────────────────────────
  const [sbExpeditions, setSbExpeditions] = useState<any[]>([]);
  const [sbLoading, setSbLoading] = useState(USE_SUPABASE);

  useEffect(() => {
    if (!USE_SUPABASE || !user?.openId) return;
    setSbLoading(true);
    sbListGuideExpeditions(user.openId as string)
      .then(setSbExpeditions)
      .finally(() => setSbLoading(false));
    const handler = () => {
      sbListGuideExpeditions(user.openId as string).then(setSbExpeditions);
    };
    window.addEventListener("supabaseExpeditionsUpdated", handler);
    return () => window.removeEventListener("supabaseExpeditionsUpdated", handler);
  }, [user?.openId]);

  // ── Static localStorage mode ───────────────────────────────────────────────
  const [staticExpeditions, setStaticExpeditions] = useState<any[]>(() => {
    if (!STATIC_NO_API) return [];
    try { return JSON.parse(localStorage.getItem(`trekko_expeditions_${(user as any)?.id ?? "guest"}`) ?? "[]"); }
    catch { return []; }
  });

  useEffect(() => {
    if (!STATIC_NO_API) return;
    const load = () => {
      try { setStaticExpeditions(JSON.parse(localStorage.getItem(expeditionsKey) ?? "[]")); }
      catch { setStaticExpeditions([]); }
    };
    load();
    window.addEventListener("staticExpeditionsUpdated", load);
    return () => window.removeEventListener("staticExpeditionsUpdated", load);
  }, [expeditionsKey]);

  // ── tRPC backend mode ──────────────────────────────────────────────────────
  const { data, isLoading } = trpc.guide.myExpeditions.useQuery(undefined, { enabled: !STATIC_NO_API && !USE_SUPABASE });

  const expeditions = USE_SUPABASE ? sbExpeditions : STATIC_NO_API ? staticExpeditions : (data?.expeditions ?? []);
  const loading = USE_SUPABASE ? sbLoading : STATIC_NO_API ? false : isLoading;

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (expeditions.length === 0) {
    return (
      <Card>
        <CardContent className="p-8 text-center">
          <Calendar className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
          <h3 className="font-heading text-lg font-semibold mb-2">Nenhuma expedição criada</h3>
          <p className="text-muted-foreground">
            Crie sua primeira expedição para começar
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {expeditions.map((expedition: any) => (
        <ExpeditionManageCard key={expedition.id} expedition={expedition} expeditionsKey={expeditionsKey} />
      ))}
    </div>
  );
}

function ExpeditionManageCard({ expedition, expeditionsKey }: { expedition: any; expeditionsKey: string }) {
  const { data: trailData } = useTrailById(expedition.trailId);
  const utils = trpc.useUtils();
  const [editOpen, setEditOpen] = useState(false);

  const deleteMutation = trpc.guide.deleteExpedition.useMutation({
    onSuccess: () => {
      utils.guide.myExpeditions.invalidate();
      toast.success("Expedição removida!");
    },
  });


  const handleDelete = async () => {
    if (USE_SUPABASE) {
      const ok = await sbDeleteExpedition(expedition.id);
      if (ok) {
        window.dispatchEvent(new Event("supabaseExpeditionsUpdated"));
        toast.success("Expedição removida!");
      } else {
        toast.error("Erro ao remover expedição");
      }
      return;
    }
    if (STATIC_NO_API) {
      try {
        const all: any[] = JSON.parse(localStorage.getItem(expeditionsKey) ?? "[]");
        localStorage.setItem(expeditionsKey, JSON.stringify(all.filter((e) => e.id !== expedition.id)));
        window.dispatchEvent(new Event("staticExpeditionsUpdated"));
        toast.success("Expedição removida!");
      } catch {
        toast.error("Erro ao remover expedição");
      }
      return;
    }
    deleteMutation.mutate({ id: expedition.id });
  };

  const trailName = expedition.trailName || trailData?.trail?.name || "Expedição";

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <h3 className="font-heading font-semibold text-lg">
                {expedition.title || trailName || "Expedição"}
              </h3>
              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                expedition.status === 'active' || expedition.status === 'published' ? 'bg-green-100 text-green-700' :
                expedition.status === 'draft' ? 'bg-yellow-100 text-yellow-700' :
                expedition.status === 'full' ? 'bg-blue-100 text-blue-700' :
                expedition.status === 'closed' ? 'bg-gray-100 text-gray-700' :
                'bg-red-100 text-red-700'
              }`}>
                {expedition.status === 'active' ? 'Ativa' :
                 expedition.status === 'published' ? 'Publicada' :
                 expedition.status === 'draft' ? 'Rascunho' :
                 expedition.status === 'full' ? 'Lotada' :
                 expedition.status === 'closed' ? 'Encerrada' : 'Cancelada'}
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-4 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <Calendar className="w-4 h-4" />
                {format(new Date(expedition.startDate), "dd/MM/yyyy")}
              </span>
              <span>{expedition.availableSpots}/{expedition.capacity} vagas</span>
              {expedition.price && <span>R$ {parseFloat(expedition.price).toFixed(2)}</span>}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Dialog open={editOpen} onOpenChange={setEditOpen}>
              <DialogTrigger asChild>
                <Button variant="outline" size="sm">
                  <Edit className="w-4 h-4 mr-1" />
                  Editar
                </Button>
              </DialogTrigger>
              <DialogContent className="max-w-lg">
                <DialogHeader>
                  <DialogTitle>Editar expedição</DialogTitle>
                </DialogHeader>
                <EditExpeditionForm
                  expedition={expedition}
                  expeditionsKey={expeditionsKey}
                  onClose={() => setEditOpen(false)}
                />
              </DialogContent>
            </Dialog>
            <Button
              variant="outline"
              size="sm"
              className="text-destructive"
              onClick={handleDelete}
              disabled={!STATIC_NO_API && !USE_SUPABASE && deleteMutation.isPending}
            >
              <Trash2 className="w-4 h-4 mr-1" />
              Remover
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

function EditExpeditionForm({ expedition, expeditionsKey, onClose }: { expedition: any; expeditionsKey: string; onClose: () => void }) {
  const { user } = useAuth();
  const [title, setTitle] = useState(expedition.title ?? "");
  const [startDate, setStartDate] = useState(expedition.startDate ? expedition.startDate.slice(0, 10) : "");
  const [endDate, setEndDate] = useState(expedition.endDate ? expedition.endDate.slice(0, 10) : "");
  const [capacity, setCapacity] = useState(String(expedition.capacity ?? 10));
  const [price, setPrice] = useState(expedition.price ?? "");
  const [meetingPoint, setMeetingPoint] = useState(expedition.meetingPoint ?? "");
  const [notes, setNotes] = useState(expedition.notes ?? "");
  const [status, setStatus] = useState(expedition.status ?? "active");
  const [submitting, setSubmitting] = useState(false);

  const utils = trpc.useUtils();
  const updateMutation = trpc.guide.updateExpedition?.useMutation?.({
    onSuccess: () => { utils.guide.myExpeditions.invalidate(); toast.success("Expedição atualizada!"); onClose(); },
    onError: () => toast.error("Erro ao atualizar expedição"),
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!startDate) { toast.error("Informe a data de início"); return; }

    if (USE_SUPABASE) {
      if (!user?.openId) { toast.error("Sessão expirada. Faça login novamente."); return; }
      setSubmitting(true);
      const { expedition: updated, error } = await sbUpdateExpedition(expedition.id, {
        title: title || null,
        startDate: new Date(startDate).toISOString(),
        endDate: endDate ? new Date(endDate).toISOString() : null,
        capacity: parseInt(capacity),
        price: price || null,
        meetingPoint: meetingPoint || null,
        notes: notes || null,
        status,
      });
      setSubmitting(false);
      if (error || !updated) { console.error(error); toast.error("Não foi possível atualizar a expedição."); return; }
      window.dispatchEvent(new Event("supabaseExpeditionsUpdated"));
      toast.success("Expedição atualizada!");
      onClose();
      return;
    }

    if (STATIC_NO_API) {
      try {
        const all: any[] = JSON.parse(localStorage.getItem(expeditionsKey) ?? "[]");
        const idx = all.findIndex((e) => e.id === expedition.id);
        if (idx !== -1) {
          all[idx] = { ...all[idx], title: title || null, startDate: new Date(startDate).toISOString(), endDate: endDate ? new Date(endDate).toISOString() : null, capacity: parseInt(capacity), availableSpots: parseInt(capacity), price: price || null, meetingPoint: meetingPoint || null, notes: notes || null, status };
          localStorage.setItem(expeditionsKey, JSON.stringify(all));
          window.dispatchEvent(new Event("staticExpeditionsUpdated"));
        }
        toast.success("Expedição atualizada!"); onClose();
      } catch { toast.error("Erro ao atualizar expedição"); }
      return;
    }

    updateMutation?.mutate?.({ id: expedition.id, title: title || undefined, startDate: new Date(startDate), endDate: endDate ? new Date(endDate) : undefined, capacity: parseInt(capacity), price: price ? parseFloat(price) : undefined, meetingPoint: meetingPoint || undefined, notes: notes || undefined });
  };

  const STATUS_OPTIONS = [
    { value: "active", label: "Ativa" },
    { value: "full", label: "Lotada" },
    { value: "closed", label: "Encerrada" },
    { value: "cancelled", label: "Cancelada" },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="edit-title">Título (opcional)</Label>
        <Input id="edit-title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Ex: Expedição de fim de semana" />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="edit-startDate">Data início *</Label>
          <Input id="edit-startDate" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </div>
        <div>
          <Label htmlFor="edit-endDate">Data fim</Label>
          <Input id="edit-endDate" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="edit-capacity">Vagas</Label>
          <Input id="edit-capacity" type="number" value={capacity} onChange={(e) => setCapacity(e.target.value)} min="1" />
        </div>
        <div>
          <Label htmlFor="edit-price">Preço (R$)</Label>
          <Input id="edit-price" type="number" value={price} onChange={(e) => setPrice(e.target.value)} min="0" step="0.01" />
        </div>
      </div>
      <div>
        <Label htmlFor="edit-meetingPoint">Ponto de encontro</Label>
        <Input id="edit-meetingPoint" value={meetingPoint} onChange={(e) => setMeetingPoint(e.target.value)} />
      </div>
      <div>
        <Label htmlFor="edit-notes">Observações</Label>
        <Textarea id="edit-notes" value={notes} onChange={(e) => setNotes(e.target.value)} rows={2} />
      </div>
      <div>
        <Label htmlFor="edit-status">Status</Label>
        <Select value={status} onValueChange={setStatus}>
          <SelectTrigger id="edit-status">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {STATUS_OPTIONS.map((s) => (
              <SelectItem key={s.value} value={s.value}>{s.label}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="outline" onClick={onClose}>Cancelar</Button>
        <Button type="submit" disabled={submitting}>
          {submitting ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
          Salvar alterações
        </Button>
      </div>
    </form>
  );
}

function CreateExpeditionForm({ onClose }: { onClose: () => void }) {
  const { user } = useAuth();
  const expeditionsKey = `trekko_expeditions_${user?.id ?? "guest"}`;
  const [trailId, setTrailId] = useState<number | null>(null);
  const [trailSearch, setTrailSearch] = useState("");
  const [title, setTitle] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [capacity, setCapacity] = useState("10");
  const [price, setPrice] = useState("");
  const [meetingPoint, setMeetingPoint] = useState("");
  const [notes, setNotes] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const { data: trailsData } = useTrailsList({ search: trailSearch, limit: 5 });
  const utils = trpc.useUtils();

  const createMutation = trpc.guide.createExpedition.useMutation({
    onSuccess: () => {
      utils.guide.myExpeditions.invalidate();
      toast.success("Expedição criada!");
      onClose();
    },
    onError: () => {
      toast.error("Erro ao criar expedição");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!trailId || !startDate) {
      toast.error("Selecione uma trilha e data");
      return;
    }

    if (USE_SUPABASE) {
      if (!user?.openId) {
        toast.error("Sessão expirada. Faça login novamente.");
        return;
      }
      setSubmitting(true);
      sbCreateExpedition({
        guideId: user.openId as string,
        guideName: user?.name ?? null,
        trailId,
        trailName: trailSearch,
        title: title || undefined,
        startDate: new Date(startDate).toISOString(),
        endDate: endDate ? new Date(endDate).toISOString() : undefined,
        capacity: parseInt(capacity),
        price: price || undefined,
        meetingPoint: meetingPoint || undefined,
        notes: notes || undefined,
      }).then(({ expedition, error }) => {
        if (error || !expedition) {
          console.error("[Trekko] expedition creation failed:", error);
          toast.error("Não foi possível criar a expedição. Tente novamente.");
          return;
        }
        window.dispatchEvent(new Event("supabaseExpeditionsUpdated"));
        toast.success("Expedição criada!");
        onClose();
      }).finally(() => setSubmitting(false));
      return;
    }

    if (STATIC_NO_API) {
      setSubmitting(true);
      try {
        const existing: any[] = JSON.parse(localStorage.getItem(expeditionsKey) ?? "[]");
        const newExpedition = {
          id: Date.now(),
          trailId,
          trailName: trailSearch,
          title: title || null,
          startDate: new Date(startDate).toISOString(),
          endDate: endDate ? new Date(endDate).toISOString() : null,
          capacity: parseInt(capacity),
          availableSpots: parseInt(capacity),
          price: price || null,
          meetingPoint: meetingPoint || null,
          notes: notes || null,
          status: "active",
        };
        localStorage.setItem(expeditionsKey, JSON.stringify([...existing, newExpedition]));
        window.dispatchEvent(new Event("staticExpeditionsUpdated"));
        toast.success("Expedição criada!");
        onClose();
      } catch {
        toast.error("Erro ao criar expedição");
      } finally {
        setSubmitting(false);
      }
      return;
    }

    createMutation.mutate({
      trailId,
      title: title || undefined,
      startDate: new Date(startDate),
      endDate: endDate ? new Date(endDate) : undefined,
      capacity: parseInt(capacity),
      price: price ? parseFloat(price) : undefined,
      meetingPoint: meetingPoint || undefined,
      notes: notes || undefined,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label>Trilha *</Label>
        <Input
          placeholder="Buscar trilha..."
          value={trailSearch}
          onChange={(e) => setTrailSearch(e.target.value)}
          className="mb-2"
        />
        {trailsData?.trails && trailsData.trails.length > 0 && trailSearch && !trailId && (
          <div className="border rounded-md max-h-40 overflow-y-auto bg-background shadow-md">
            {trailsData.trails.map((trail) => (
              <button
                key={trail.id}
                type="button"
                className="w-full text-left px-3 py-2 hover:bg-muted cursor-pointer block"
                onClick={() => {
                  setTrailId(trail.id);
                  setTrailSearch(trail.name);
                }}
              >
                <span className="font-medium">{trail.name}</span>
                <span className="text-sm text-muted-foreground ml-2">{trail.city}, {trail.uf}</span>
              </button>
            ))}
          </div>
        )}
        {trailId && (
          <div className="flex items-center gap-2 p-2 bg-primary/10 rounded-md">
            <span className="text-sm font-medium">{trailSearch}</span>
            <button
              type="button"
              className="text-muted-foreground hover:text-foreground"
              onClick={() => {
                setTrailId(null);
                setTrailSearch("");
              }}
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
      <div>
        <Label htmlFor="title">Título (opcional)</Label>
        <Input id="title" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Ex: Expedição de fim de semana" />
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="startDate">Data início *</Label>
          <Input id="startDate" type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
        </div>
        <div>
          <Label htmlFor="endDate">Data fim</Label>
          <Input id="endDate" type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
        </div>
      </div>
      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="capacity">Vagas</Label>
          <Input id="capacity" type="number" value={capacity} onChange={(e) => setCapacity(e.target.value)} min="1" />
        </div>
        <div>
          <Label htmlFor="price">Preço (R$)</Label>
          <Input id="price" type="number" value={price} onChange={(e) => setPrice(e.target.value)} min="0" step="0.01" />
        </div>
      </div>
      <div>
        <Label htmlFor="meetingPoint">Ponto de encontro</Label>
        <Input id="meetingPoint" value={meetingPoint} onChange={(e) => setMeetingPoint(e.target.value)} />
      </div>
      <div>
        <Label htmlFor="notes">Observações</Label>
        <Textarea id="notes" value={notes} onChange={(e) => setNotes(e.target.value)} rows={2} />
      </div>

      {/* Platform Fee Notice */}
      <div className="p-3 bg-amber-50 border border-amber-200 rounded-lg">
        <p className="text-sm text-amber-800">
          <strong>Taxa da plataforma:</strong> Uma taxa de <strong>4%</strong> será aplicada sobre o valor de cada reserva efetivada nesta expedição.
        </p>
      </div>

      <div className="flex justify-end gap-2 pt-4">
        <Button type="button" variant="outline" onClick={onClose}>Cancelar</Button>
        <Button type="submit" disabled={submitting || createMutation.isPending}>
          {(submitting || createMutation.isPending) ? <Loader2 className="w-4 h-4 animate-spin mr-2" /> : null}
          Criar expedição
        </Button>
      </div>
    </form>
  );
}
