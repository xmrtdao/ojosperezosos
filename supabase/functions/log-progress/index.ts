// Supabase Edge Function: log-progress  
// Save daily exercise scores (Gabor threshold, vernier score, compliance minutes)  
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";  
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.4";  
  
const corsHeaders = {  
  "Access-Control-Allow-Origin": "*",  
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",  
};  
  
serve(async (req) => {  
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });  
  
  const body = await req.json().catch(() => ({}));  
  const user_id = body.user_id || "anonymous";  
  const session_id = body.session_id || crypto.randomUUID();  
  const exercise_id = body.exercise_id || "unknown";  
  const score = body.score ?? null;  
  const gabor_threshold = body.gabor_threshold ?? null;  
  const vernier_score = body.vernier_score ?? null;  
  const compliance_min = body.compliance_min ?? 0;  
  const dominant_eye = body.dominant_eye || "right";  
  const gaze_stability = body.gaze_stability ?? null;  
  
  const supabaseAdmin = createClient(  
    Deno.env.get("SUPABASE_URL")!,  
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!  
  );  
  
  const { error } = await supabaseAdmin.from("progress_log").insert({  
    user_id, session_id, exercise_id, score, gabor_threshold, vernier_score, compliance_min, dominant_eye, gaze_stability  
  });  
  
  if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: corsHeaders });  
  
  return new Response(JSON.stringify({ ok: true, session_id }), {  
    headers: { ...corsHeaders, "Content-Type": "application/json" }  
  });  
});  