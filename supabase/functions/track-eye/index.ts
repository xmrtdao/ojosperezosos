// Supabase Edge Function: track-eye  
// Log eye gaze data from therapy session  
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
  const eye = body.eye || "left"; // "left" | "right"  
  const gaze_x = body.gaze_x ?? null;  
  const gaze_y = body.gaze_y ?? null;  
  const pupil_size = body.pupil_size ?? null;  
  const blink_rate = body.blink_rate ?? null;  
  const timestamp = body.timestamp || new Date().toISOString();  
  
  const supabaseAdmin = createClient(  
    Deno.env.get("SUPABASE_URL")!,  
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!  
  );  
  
  const { error } = await supabaseAdmin.from("eye_tracking").insert({  
    user_id, session_id, eye, gaze_x, gaze_y, pupil_size, blink_rate, timestamp  
  });  
  
  if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: corsHeaders });  
  
  return new Response(JSON.stringify({ ok: true, session_id }), {  
    headers: { ...corsHeaders, "Content-Type": "application/json" }  
  });  
});  