/**
 * Expedition CRUD via Supabase — used when USE_SUPABASE is true so that
 * expeditions created by guides are visible to all users on all devices.
 */
import { supabase } from "./supabase";

/** Row as stored in Supabase (snake_case). */
type ExpeditionRow = {
  id: number;
  guide_id: string;
  guide_name: string | null;
  trail_id: number;
  trail_name: string | null;
  title: string | null;
  start_date: string;
  end_date: string | null;
  capacity: number;
  available_spots: number;
  price: string | null;
  meeting_point: string | null;
  notes: string | null;
  status: string;
  created_at: string;
};

/** Camel-case shape used by the existing display components. */
export type Expedition = {
  id: number;
  guideId: string;
  guideName: string | null;
  trailId: number;
  trailName: string | null;
  title: string | null;
  startDate: string;
  endDate: string | null;
  capacity: number;
  availableSpots: number;
  price: string | null;
  meetingPoint: string | null;
  notes: string | null;
  status: string;
  createdAt: string;
};

function toExpedition(row: ExpeditionRow): Expedition {
  return {
    id: row.id,
    guideId: row.guide_id,
    guideName: row.guide_name,
    trailId: row.trail_id,
    trailName: row.trail_name,
    title: row.title,
    startDate: row.start_date,
    endDate: row.end_date,
    capacity: row.capacity,
    availableSpots: row.available_spots,
    price: row.price,
    meetingPoint: row.meeting_point,
    notes: row.notes,
    status: row.status,
    createdAt: row.created_at,
  };
}

/** Returns true if the expeditions table is accessible. */
export async function sbExpeditionsTableExists(): Promise<boolean> {
  if (!supabase) return false;
  const { error } = await supabase.from("expeditions").select("id").limit(0);
  return !error;
}

export async function sbListPublicExpeditions(search?: string): Promise<Expedition[]> {
  if (!supabase) return [];
  let q = supabase
    .from("expeditions")
    .select("*")
    .neq("status", "cancelled")
    .order("start_date", { ascending: true });
  if (search) q = q.ilike("trail_name", `%${search}%`);
  const { data, error } = await q;
  if (error) { console.error("[Trekko] sbListPublicExpeditions:", error.message); return []; }
  return (data as ExpeditionRow[]).map(toExpedition);
}

export async function sbListGuideExpeditions(guideId: string): Promise<Expedition[]> {
  if (!supabase) return [];
  const { data, error } = await supabase
    .from("expeditions")
    .select("*")
    .eq("guide_id", guideId)
    .order("start_date", { ascending: true });
  if (error) { console.error("[Trekko] sbListGuideExpeditions:", error.message); return []; }
  return (data as ExpeditionRow[]).map(toExpedition);
}

export async function sbCreateExpedition(input: {
  guideId: string;
  guideName: string | null;
  trailId: number;
  trailName: string | null;
  title?: string;
  startDate: string;
  endDate?: string;
  capacity: number;
  price?: string;
  meetingPoint?: string;
  notes?: string;
}): Promise<{ expedition: Expedition | null; error: string | null }> {
  if (!supabase) return { expedition: null, error: "Supabase não configurado" };
  if (!input.guideId) return { expedition: null, error: "Usuário não autenticado" };
  const { data, error } = await supabase
    .from("expeditions")
    .insert({
      guide_id: input.guideId,
      guide_name: input.guideName,
      trail_id: input.trailId,
      trail_name: input.trailName,
      title: input.title ?? null,
      start_date: input.startDate,
      end_date: input.endDate ?? null,
      capacity: input.capacity,
      available_spots: input.capacity,
      price: input.price ?? null,
      meeting_point: input.meetingPoint ?? null,
      notes: input.notes ?? null,
      status: "active",
    })
    .select()
    .single();
  if (error) {
    console.error("[Trekko] sbCreateExpedition:", error.message, error.code);
    const msg = error.code === "42P01"
      ? "Tabela de expedições não existe no Supabase. Execute o SQL de configuração."
      : error.message;
    return { expedition: null, error: msg };
  }
  return { expedition: toExpedition(data as ExpeditionRow), error: null };
}

export async function sbUpdateExpedition(
  id: number,
  input: {
    title?: string | null;
    startDate: string;
    endDate?: string | null;
    capacity: number;
    price?: string | null;
    meetingPoint?: string | null;
    notes?: string | null;
    status?: string;
  }
): Promise<{ expedition: Expedition | null; error: string | null }> {
  if (!supabase) return { expedition: null, error: "Supabase não configurado" };
  const { data, error } = await supabase
    .from("expeditions")
    .update({
      title: input.title ?? null,
      start_date: input.startDate,
      end_date: input.endDate ?? null,
      capacity: input.capacity,
      available_spots: input.capacity,
      price: input.price ?? null,
      meeting_point: input.meetingPoint ?? null,
      notes: input.notes ?? null,
      status: input.status ?? "active",
    })
    .eq("id", id)
    .select()
    .single();
  if (error) {
    console.error("[Trekko] sbUpdateExpedition:", error.message);
    return { expedition: null, error: error.message };
  }
  return { expedition: toExpedition(data as ExpeditionRow), error: null };
}

export async function sbDeleteExpedition(id: number): Promise<boolean> {
  if (!supabase) return false;
  const { error } = await supabase.from("expeditions").delete().eq("id", id);
  if (error) { console.error("[Trekko] sbDeleteExpedition:", error.message); return false; }
  return true;
}
