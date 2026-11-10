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

/** Where the confirmation link should send the user back to. */
function authRedirectUrl(): string | undefined {
  try {
    return typeof window !== "undefined" ? `${window.location.origin}/` : undefined;
  } catch {
    return undefined;
  }
}

/** Translate common Supabase Auth errors to Portuguese. */
function translateAuthError(error: { message?: string; code?: string } | null): string {
  const m = `${error?.message ?? ""} ${error?.code ?? ""}`;
  if (/rate.?limit|over_email_send_rate_limit|over_request_rate_limit|429/i.test(m)) {
    return "Muitas tentativas em pouco tempo. Aguarde alguns minutos e tente novamente.";
  }
  if (/sending confirmation|sending.*email|unexpected_failure|smtp/i.test(m)) {
    return "Não conseguimos enviar o link de confirmação agora. Tente novamente em alguns minutos.";
  }
  if (/weak_password|password should/i.test(m)) {
    const n = m.match(/at least (\d+)/i);
    return n
      ? `A senha deve ter pelo menos ${n[1]} caracteres.`
      : "A senha não atende aos requisitos mínimos de segurança.";
  }
  if (/validate email|email_address_invalid|invalid format/i.test(m)) {
    return "E-mail inválido. Confira o endereço digitado.";
  }
  if (/signup_disabled|signups not allowed/i.test(m)) {
    return "Novos cadastros estão temporariamente indisponíveis.";
  }
  if (/failed to fetch|network|load failed/i.test(m)) {
    return "Falha de conexão. Verifique sua internet e tente novamente.";
  }
  return error?.message || "Erro inesperado. Tente novamente.";
}

const EMAIL_ALREADY_REGISTERED = "Este e-mail já está cadastrado. Faça login com ele.";

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
    const m = `${error.message ?? ""} ${(error as any).code ?? ""}`;
    if (m.includes("Invalid login credentials") || m.includes("invalid_credentials")) {
      return { error: "E-mail ou senha incorretos" };
    }
    if (m.includes("Email not confirmed") || m.includes("email_not_confirmed")) {
      // Resend the confirmation link so the user isn't stuck.
      let resendError: unknown = null;
      try {
        ({ error: resendError } = await supabase.auth.resend({
          type: "signup",
          email,
          options: { emailRedirectTo: authRedirectUrl() },
        }));
      } catch (e) {
        resendError = e;
      }
      return {
        error: resendError
          ? "Seu e-mail ainda não foi confirmado. Clique no link que enviamos no cadastro (confira também a pasta de spam)."
          : "Seu e-mail ainda não foi confirmado. Acabamos de reenviar o link de confirmação — confira sua caixa de entrada e a pasta de spam.",
      };
    }
    return { error: translateAuthError(error) };
  }
  if (!data.user || !data.session) return { error: "Não foi possível entrar. Tente novamente." };
  return { user: toUser(data.user) };
}

export async function supabaseRegister(data: {
  name: string;
  email: string;
  password: string;
  userType: "trekker" | "guide";
  cadasturNumber?: string;
  pixKeyType?: string;
  pixKeyValue?: string;
}): Promise<
  { user: SupabaseUser; confirmationRequired?: boolean } | { error: string }
> {
  if (!supabase) return { error: "Supabase não configurado" };
  const { data: auth, error } = await supabase.auth.signUp({
    email: data.email,
    password: data.password,
    options: {
      emailRedirectTo: authRedirectUrl(),
      data: {
        numericId: Date.now(),
        name: data.name,
        userType: data.userType,
        cadasturNumber: data.cadasturNumber ?? null,
        cadasturValidated: 0,
        bio: null,
        photoUrl: null,
        // Store Pix in metadata as recovery backup for guides
        ...(data.userType === "guide" && data.pixKeyType
          ? { pixKeyType: data.pixKeyType, pixKeyValue: data.pixKeyValue ?? null }
          : {}),
      },
    },
  });
  if (error) {
    const m = `${error.message ?? ""} ${(error as any).code ?? ""}`;
    if (/already registered|already been registered|user_already_exists|email_exists/i.test(m)) {
      return { error: EMAIL_ALREADY_REGISTERED };
    }
    return { error: translateAuthError(error) };
  }
  if (!auth.user) return { error: "Cadastro falhou. Tente novamente." };
  // With "Confirm email" enabled, Supabase answers a sign-up for an e-mail that
  // already belongs to a confirmed account with an obfuscated user whose
  // identities array is EMPTY (anti-enumeration) — no account is created and
  // no e-mail is sent.
  if (Array.isArray(auth.user.identities) && auth.user.identities.length === 0) {
    return { error: EMAIL_ALREADY_REGISTERED };
  }
  // A genuine new sign-up with confirmation enabled returns the user with a
  // null session: the account exists but the user must click the e-mail link.
  if (!auth.session) {
    return { confirmationRequired: true, user: toUser(auth.user) };
  }
  return { user: toUser(auth.user) };
}

/** Send a password-recovery link that returns to /redefinir-senha/. */
export async function supabaseRequestPasswordReset(
  email: string,
): Promise<{ success: true } | { error: string }> {
  if (!supabase) return { error: "Supabase não configurado" };
  try {
    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/redefinir-senha/`,
    });
    if (error) {
      const m = `${error.message ?? ""} ${(error as any).code ?? ""}`;
      return {
        error: /rate.?limit|429/i.test(m)
          ? "Muitas tentativas em pouco tempo. Aguarde alguns minutos e tente novamente."
          : "Não foi possível enviar o link de recuperação. Tente novamente em alguns minutos.",
      };
    }
    return { success: true };
  } catch {
    return { error: "Falha de conexão. Verifique sua internet e tente novamente." };
  }
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
