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

export async function sbGetExpeditionById(id: number): Promise<Expedition | null> {
  if (!supabase) return null;
  const { data, error } = await supabase
    .from("expeditions")
    .select("*")
    .eq("id", id)
    .single();
  if (error) { console.error("[Trekko] sbGetExpeditionById:", error.message); return null; }
  return toExpedition(data as ExpeditionRow);
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

  // First try a direct UPDATE (works when the UPDATE RLS policy exists)
  const { data: updated, error: updateError } = await supabase
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

  if (!updateError && updated) {
    return { expedition: toExpedition(updated as ExpeditionRow), error: null };
  }

  // Fallback: delete + re-insert preserving the same ID
  // (needed until the UPDATE RLS policy is applied via migration).
  console.warn("[Trekko] UPDATE failed, falling back to delete+insert:", updateError?.message);

  const { data: existing, error: fetchError } = await supabase
    .from("expeditions")
    .select("*")
    .eq("id", id)
    .single();
  if (fetchError || !existing) return { expedition: null, error: "Expedição não encontrada" };

  const { error: deleteError } = await supabase.from("expeditions").delete().eq("id", id);
  if (deleteError) return { expedition: null, error: deleteError.message };

  const { data: inserted, error: insertError } = await supabase
    .from("expeditions")
    .insert({
      id,                                              // Preserve original ID so URLs don't break
      guide_id: (existing as ExpeditionRow).guide_id,
      guide_name: (existing as ExpeditionRow).guide_name,
      trail_id: (existing as ExpeditionRow).trail_id,
      trail_name: (existing as ExpeditionRow).trail_name,
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
    .select()
    .single();

  if (insertError) {
    console.error("[Trekko] sbUpdateExpedition fallback insert failed:", insertError.message);
    return { expedition: null, error: insertError.message };
  }
  return { expedition: toExpedition(inserted as ExpeditionRow), error: null };
}

// ─── Enrollment ───────────────────────────────────────────────────────────────
//
// Three-tier strategy per operation:
//   1. Supabase `enrollments` table via atomic RPC function (best: tracks spots)
//   2. Direct insert/delete on `enrollments` table (good: records enrollment)
//   3. Supabase auth user_metadata (fallback: works without any migration)
//

/** PostgREST returns a schema-cache error (not 42P01) when the table doesn't exist. */
function isMissingTableError(err: { code?: string; message?: string } | null | undefined): boolean {
  if (!err) return false;
  return (
    err.code === "42P01" ||
    err.message?.includes("schema cache") === true ||
    err.message?.includes("does not exist") === true ||
    err.message?.includes("Could not find") === true
  );
}

/** Read enrolled expedition IDs from the current user's auth metadata. */
async function metaGetEnrolled(): Promise<number[]> {
  if (!supabase) return [];
  const { data: { user } } = await supabase.auth.getUser();
  return (user?.user_metadata?.enrolledExpeditions as number[] | undefined) ?? [];
}

/** Persist enrolled expedition IDs to the current user's auth metadata. */
async function metaSetEnrolled(ids: number[]): Promise<void> {
  await supabase!.auth.updateUser({ data: { enrolledExpeditions: ids } });
}

export async function sbIsEnrolled(expeditionId: number, _userId: string): Promise<boolean> {
  if (!supabase) return false;

  // Try the enrollments table
  const { data, error } = await supabase
    .from("enrollments")
    .select("id")
    .eq("expedition_id", expeditionId)
    .neq("status", "cancelled")
    .maybeSingle();

  if (!error) return Boolean(data);

  // Table missing — fall back to user_metadata
  if (isMissingTableError(error)) {
    const ids = await metaGetEnrolled();
    return ids.includes(expeditionId);
  }

  console.error("[Trekko] sbIsEnrolled:", error.message);
  return false;
}

export async function sbEnrollExpedition(input: {
  expeditionId: number;
  userId: string;
  userName: string | null;
  userEmail: string | null;
  spots: number;
}): Promise<{ success: boolean; error: string | null }> {
  if (!supabase) return { success: false, error: "Supabase não configurado" };

  // 1. Try atomic RPC (creates enrollment + updates available_spots in one tx)
  const { data: rpcData, error: rpcError } = await supabase.rpc("enroll_in_expedition", {
    p_expedition_id: input.expeditionId,
    p_user_id: input.userId,
    p_user_name: input.userName,
    p_user_email: input.userEmail,
    p_spots: input.spots,
  });

  if (!rpcError && (rpcData as any)?.success) return { success: true, error: null };

  // 2. Try direct insert into enrollments table (RPC may have failed for unrelated reason)
  if (!isMissingTableError(rpcError)) {
    const { error: insertError } = await supabase.from("enrollments").insert({
      expedition_id: input.expeditionId,
      user_id: input.userId,
      user_name: input.userName,
      user_email: input.userEmail,
      spots: input.spots,
      status: "confirmed",
    });

    if (!insertError) return { success: true, error: null };

    if (insertError.code === "23505") {
      return { success: false, error: "Você já está inscrito nesta expedição" };
    }
    if (!isMissingTableError(insertError)) {
      return { success: false, error: insertError.message };
    }
    // table missing → fall through
  }

  // 3. Fallback: store in auth user_metadata (no table required)
  console.warn("[Trekko] enrollments table not found — using user_metadata fallback");
  const ids = await metaGetEnrolled();
  if (ids.includes(input.expeditionId)) {
    return { success: false, error: "Você já está inscrito nesta expedição" };
  }
  await metaSetEnrolled([...ids, input.expeditionId]);
  return { success: true, error: null };
}

export async function sbCancelEnrollment(
  expeditionId: number,
  userId: string,
): Promise<{ success: boolean; error: string | null }> {
  if (!supabase) return { success: false, error: "Supabase não configurado" };

  // 1. Try atomic RPC
  const { data: rpcData, error: rpcError } = await supabase.rpc("cancel_enrollment", {
    p_expedition_id: expeditionId,
    p_user_id: userId,
  });

  if (!rpcError && (rpcData as any)?.success) return { success: true, error: null };

  // 2. Try direct delete on enrollments table
  if (!isMissingTableError(rpcError)) {
    const { error: deleteError } = await supabase
      .from("enrollments")
      .delete()
      .eq("expedition_id", expeditionId)
      .eq("user_id", userId);

    if (!deleteError) return { success: true, error: null };
    if (!isMissingTableError(deleteError)) return { success: false, error: deleteError.message };
  }

  // 3. Fallback: remove from auth user_metadata
  console.warn("[Trekko] enrollments table not found — using user_metadata fallback for cancel");
  const ids = await metaGetEnrolled();
  await metaSetEnrolled(ids.filter((id) => id !== expeditionId));
  return { success: true, error: null };
}

export async function sbDeleteExpedition(id: number): Promise<boolean> {
  if (!supabase) return false;
  const { error } = await supabase.from("expeditions").delete().eq("id", id);
  if (error) { console.error("[Trekko] sbDeleteExpedition:", error.message); return false; }
  return true;
}
