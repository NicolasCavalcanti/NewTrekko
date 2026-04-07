import { createClient } from "@supabase/supabase-js";

const SUPABASE_URL = "https://nyvfwvydcwmbafzxfozk.supabase.co";
const SUPABASE_ANON_KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im55dmZ3dnlkY3dtYmFmenhmb3prIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU1MDQ4MDQsImV4cCI6MjA5MTA4MDgwNH0.K5F9BhwMpcSU_NsrAdm7ITOBKt_kTO0wKuEp8qvigO0";

export const USE_SUPABASE = true;

export const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
