import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL ?? "";
const key = import.meta.env.VITE_SUPABASE_ANON_KEY ?? "";

/** True when Supabase is configured — auth is cloud-based and cross-device. */
export const USE_SUPABASE = Boolean(url && key);

export const supabase = USE_SUPABASE ? createClient(url, key) : null;
