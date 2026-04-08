/**
 * Client-side helper to create a Mercado Pago checkout via Supabase Edge Function.
 * The edge function holds the MERCADOPAGO_ACCESS_TOKEN securely server-side.
 */
import { supabase } from "./supabase";

export async function sbCreateMpCheckout(input: {
  expeditionId: number;
  expeditionTitle: string | null;
  trailName: string | null;
  startDate: string | null;
  price: string;
  quantity: number;
  userEmail: string | null;
  userName: string | null;
}): Promise<{ checkoutUrl: string | null; error: string | null }> {
  if (!supabase) return { checkoutUrl: null, error: "Supabase não configurado" };

  // Derive the app base URL (works on GitHub Pages and custom domains)
  const base = window.location.origin;

  const { data, error } = await supabase.functions.invoke("create-mp-checkout", {
    body: { ...input, baseUrl: base },
  });

  if (error) {
    console.error("[Trekko] sbCreateMpCheckout:", error.message);
    return { checkoutUrl: null, error: error.message };
  }

  if (!data?.checkoutUrl) {
    const msg = data?.error || "URL de pagamento não gerada";
    console.error("[Trekko] sbCreateMpCheckout: no checkoutUrl —", msg);
    return { checkoutUrl: null, error: msg };
  }

  return { checkoutUrl: data.checkoutUrl, error: null };
}
