/**
 * Supabase Edge Function — creates a Mercado Pago Checkout Pro preference
 * and returns the init_point URL to redirect the user to payment.
 *
 * Required Supabase secret: MERCADOPAGO_ACCESS_TOKEN
 * Set via: supabase secrets set MERCADOPAGO_ACCESS_TOKEN=<token> --project-ref <ref>
 */

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers":
    "authorization, x-client-info, apikey, content-type",
};

Deno.serve(async (req: Request) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: CORS });
  }

  try {
    const accessToken = Deno.env.get("MERCADOPAGO_ACCESS_TOKEN");
    if (!accessToken) {
      return json({ error: "Pagamento não configurado (MERCADOPAGO_ACCESS_TOKEN ausente)" }, 500);
    }

    const body = await req.json();
    const {
      expeditionId,
      expeditionTitle,
      trailName,
      startDate,
      price,
      quantity,
      userEmail,
      userName,
      baseUrl,
    } = body as {
      expeditionId: number;
      expeditionTitle: string | null;
      trailName: string | null;
      startDate: string | null;
      price: string;
      quantity: number;
      userEmail: string | null;
      userName: string | null;
      baseUrl: string;
    };

    if (!price || isNaN(parseFloat(price))) {
      return json({ error: "Preço inválido" }, 400);
    }

    const unitPrice = parseFloat(price);
    const externalRef = `expedition_${expeditionId}_${Date.now()}`;
    const expiresAt = new Date(Date.now() + 30 * 60 * 1000).toISOString();

    const dateLabel = startDate
      ? new Date(startDate).toLocaleDateString("pt-BR")
      : "";
    const itemTitle =
      expeditionTitle || trailName || `Expedição #${expeditionId}`;

    const preference = {
      items: [
        {
          id: `expedition_${expeditionId}`,
          title: itemTitle,
          description: `${quantity} vaga(s)${dateLabel ? ` — ${dateLabel}` : ""}`,
          quantity: quantity,
          unit_price: unitPrice,
          currency_id: "BRL",
        },
      ],
      payer: {
        ...(userEmail ? { email: userEmail } : {}),
        ...(userName ? { name: userName } : {}),
      },
      back_urls: {
        success: `${baseUrl}/reservas?success=true`,
        failure: `${baseUrl}/expedicao/${expeditionId}?cancelled=true`,
        pending: `${baseUrl}/reservas?pending=true`,
      },
      auto_return: "approved",
      external_reference: externalRef,
      expires: true,
      expiration_date_from: new Date().toISOString(),
      expiration_date_to: expiresAt,
      payment_methods: {
        installments: 12,
        default_installments: 1,
      },
      metadata: {
        expedition_id: String(expeditionId),
        source: "trekko_static",
      },
    };

    const mpRes = await fetch(
      "https://api.mercadopago.com/checkout/preferences",
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
          "X-Idempotency-Key": externalRef,
        },
        body: JSON.stringify(preference),
      },
    );

    const mpData = await mpRes.json();

    if (!mpRes.ok) {
      console.error("[create-mp-checkout] MP API error:", JSON.stringify(mpData));
      return json(
        { error: mpData?.message || "Erro ao criar preferência de pagamento" },
        400,
      );
    }

    return json({ checkoutUrl: mpData.init_point });
  } catch (err) {
    console.error("[create-mp-checkout] Unexpected error:", err);
    return json({ error: String(err) }, 500);
  }
});

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS, "Content-Type": "application/json" },
  });
}
