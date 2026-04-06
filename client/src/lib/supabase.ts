import { createClient } from "@supabase/supabase-js";

const url = import.meta.env.VITE_SUPABASE_URL ?? "";
const key = import.meta.env.VITE_SUPABASE_ANON_KEY ?? "";

function isValidHttpUrl(str: string): boolean {
  try {
    const u = new URL(str);
    return u.protocol === "http:" || u.protocol === "https:";
  } catch {
    return false;
  }
}

/** True only when both env vars are present AND the URL is a valid https URL. */
export const USE_SUPABASE = Boolean(url && key && isValidHttpUrl(url));

let _client: ReturnType<typeof createClient> | null = null;
if (USE_SUPABASE) {
  try {
    _client = createClient(url, key);
  } catch (e) {
    console.warn("[Trekko] Supabase init failed — falling back to local auth:", e);
  }
}
export const supabase = _client;
