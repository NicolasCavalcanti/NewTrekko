/**
 * Auth layer backed by Supabase when VITE_SUPABASE_URL is configured.
 * Returns objects that match the DemoUser shape so the rest of the app
 * (useAuth, Profile, etc.) can consume them without any changes.
 */
import { supabase } from "./supabase";

export type SupabaseUser = {
  id: number;
  name: string;
  email: string;
  userType: "trekker" | "guide";
  role: "user" | "admin";
  photoUrl: string | null;
  bio: string | null;
  cadasturNumber: string | null;
  cadasturValidated: number;
  openId: string | null;
  loginMethod: string | null;
  passwordHash: string | null;
  createdAt: Date | null;
  updatedAt: Date | null;
  lastSignedIn: Date | null;
};

function toUser(raw: any): SupabaseUser {
  const m = raw.user_metadata ?? {};
  return {
    id: m.numericId ?? 0,
    name: m.name ?? raw.email?.split("@")[0] ?? "Usuário",
    email: raw.email ?? "",
    userType: m.userType ?? "trekker",
    role: "user",
    photoUrl: m.photoUrl ?? null,
    bio: m.bio ?? null,
    cadasturNumber: m.cadasturNumber ?? null,
    cadasturValidated: m.cadasturValidated ?? 0,
    openId: raw.id ?? null,
    loginMethod: "password",
    passwordHash: null,
    createdAt: raw.created_at ? new Date(raw.created_at) : null,
    updatedAt: null,
    lastSignedIn: raw.last_sign_in_at ? new Date(raw.last_sign_in_at) : null,
  };
}

export async function supabaseLogin(
  email: string,
  password: string,
): Promise<{ user: SupabaseUser } | { error: string }> {
  if (!supabase) return { error: "Supabase não configurado" };
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });
  if (error) {
    // Translate common Supabase errors to Portuguese
    if (error.message.includes("Invalid login credentials")) {
      return { error: "E-mail ou senha incorretos" };
    }
    if (error.message.includes("Email not confirmed")) {
      return { error: "Confirme seu e-mail antes de entrar" };
    }
    return { error: error.message };
  }
  if (!data.user) return { error: "Login falhou" };
  return { user: toUser(data.user) };
}

export async function supabaseRegister(data: {
  name: string;
  email: string;
  password: string;
  userType: "trekker" | "guide";
  cadasturNumber?: string;
}): Promise<{ user: SupabaseUser } | { error: string }> {
  if (!supabase) return { error: "Supabase não configurado" };
  const { data: auth, error } = await supabase.auth.signUp({
    email: data.email,
    password: data.password,
    options: {
      data: {
        numericId: Date.now(),
        name: data.name,
        userType: data.userType,
        cadasturNumber: data.cadasturNumber ?? null,
        cadasturValidated: 0,
        bio: null,
        photoUrl: null,
      },
    },
  });
  if (error) {
    if (error.message.includes("already registered")) {
      return { error: "Este e-mail já está cadastrado" };
    }
    return { error: error.message };
  }
  if (!auth.user) return { error: "Cadastro falhou" };
  return { user: toUser(auth.user) };
}

export async function supabaseGetCurrentUser(): Promise<SupabaseUser | null> {
  if (!supabase) return null;
  const {
    data: { user },
  } = await supabase.auth.getUser();
  return user ? toUser(user) : null;
}

export async function supabaseSignOut(): Promise<void> {
  await supabase?.auth.signOut();
}

/** Subscribe to Supabase auth changes; returns an unsubscribe function. */
export function supabaseOnAuthChange(
  cb: (user: SupabaseUser | null) => void,
): () => void {
  if (!supabase) return () => {};
  const {
    data: { subscription },
  } = supabase.auth.onAuthStateChange((_event, session) => {
    cb(session?.user ? toUser(session.user) : null);
  });
  return () => subscription.unsubscribe();
}

export async function supabaseUpdateProfile(data: {
  name: string;
  bio: string;
  photoUrl?: string | null;
}): Promise<{ user: SupabaseUser } | { error: string }> {
  if (!supabase) return { error: "Supabase não configurado" };
  const { data: auth, error } = await supabase.auth.updateUser({
    data: {
      name: data.name,
      bio: data.bio,
      ...(data.photoUrl !== undefined ? { photoUrl: data.photoUrl } : {}),
    },
  });
  if (error) return { error: error.message };
  if (!auth.user) return { error: "Atualização falhou" };
  return { user: toUser(auth.user) };
}
