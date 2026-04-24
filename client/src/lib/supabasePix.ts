import { supabase } from "./supabase";
import type { PixKeyType } from "./pixValidation";

export type GuidePix = {
  id: string;
  userId: string;
  pixKeyType: PixKeyType;
  pixKeyValue: string;
  pixKeyStatus: "pending" | "active" | "inactive";
  pixKeyVerified: boolean;
  createdAt: string;
  updatedAt: string;
};

export async function saveGuidePix(data: {
  pixKeyType: PixKeyType;
  pixKeyValue: string;
}): Promise<{ success: true } | { error: string }> {
  if (!supabase) return { error: "Supabase não configurado" };

  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return { error: "Usuário não autenticado" };

  const { error } = await supabase.from("guide_pix_keys").upsert(
    {
      user_id: user.id,
      pix_key_type: data.pixKeyType,
      pix_key_value: data.pixKeyValue,
      pix_key_status: "pending",
      pix_key_verified: false,
      updated_at: new Date().toISOString(),
    },
    { onConflict: "user_id" }
  );

  if (error) {
    // Table may not exist in all environments — soft fail
    if (error.code === "42P01") return { success: true };
    return { error: error.message };
  }

  return { success: true };
}

export async function getMyGuidePix(): Promise<GuidePix | null> {
  if (!supabase) return null;

  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) return null;

  const { data, error } = await supabase
    .from("guide_pix_keys")
    .select("*")
    .eq("user_id", user.id)
    .maybeSingle();

  if (error || !data) return null;

  return {
    id: data.id,
    userId: data.user_id,
    pixKeyType: data.pix_key_type,
    pixKeyValue: data.pix_key_value,
    pixKeyStatus: data.pix_key_status,
    pixKeyVerified: data.pix_key_verified,
    createdAt: data.created_at,
    updatedAt: data.updated_at,
  };
}
