// Supabase Edge Function: run-exercise  
// Return personalized exercise sequence based on user's treatment plan  
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";  
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.4";  
  
const corsHeaders = {  
  "Access-Control-Allow-Origin": "*",  
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",  
};  
  
const EXERCISE_POOL = [  
  { id: "fixation", name: "Fixation Stability", type: "gaze", duration: 120, description: "Hold gaze on a stationary cross" },  
  { id: "saccade", name: "Saccade Tracking", type: "follow", duration: 120, description: "Follow a jumping target" },  
  { id: "pursuit", name: "Smooth Pursuit", type: "smooth", duration: 120, description: "Track a moving dot smoothly" },  
  { id: "gabor", name: "Gabor Contrast Task", type: "gabor", duration: 180, description: "Match contrast between eyes" },  
  { id: "vernier", name: "Vernier Acuity", type: "vernier", duration: 180, description: "Align split lines with gaze" },  
  { id: "stereogram", name: "Random Dot Stereogram", type: "stereogram", duration: 150, description: "Fuse depth perception" }  
];  
  
serve(async (req) => {  
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });  
  
  const body = await req.json().catch(() => ({}));  
  const user_id = body.user_id || "anonymous";  
  const phase = body.phase || "phase2"; // phase1 | phase2 | phase3 | phase4  
  const weak_eye = body.weak_eye || "left";  
  const contrast_ratio = body.contrast_ratio ?? 0.3;  
  const session_min = body.session_min ?? 20;  
  
  // Build sequence based on treatment phase  
  let sequence = [];  
  if (phase === "phase1") {  
    sequence = EXERCISE_POOL.slice(0, 2); // Calibration focus  
  } else if (phase === "phase2") {  
    sequence = [EXERCISE_POOL[1], EXERCISE_POOL[0], EXERCISE_POOL[3], EXERCISE_POOL[4]];  
  } else if (phase === "phase3") {  
    sequence = [EXERCISE_POOL[2], EXERCISE_POOL[3], EXERCISE_POOL[4], EXERCISE_POOL[5]];  
  } else {  
    sequence = [EXERCISE_POOL[3], EXERCISE_POOL[5]];  
  }  
  
  // Adjust contrast per eye  
  const strong_contrast = contrast_ratio;  
  const weak_contrast = 1.0;  
  const strong_eye = weak_eye === "left" ? "right" : "left";  
  
  return new Response(JSON.stringify({  
    user_id,  
    phase,  
    exercises: sequence.map((ex, i) => ({ ...ex, order: i+1 })),  
    contrast: {  
      [weak_eye]: weak_contrast,  
      [strong_eye]: strong_contrast  
    },  
    target_duration_min: session_min,  
    message: `Today: ${sequence.length} exercises, ~${sequence.reduce((a,b) => a + b.duration, 0)/60} min + breaks.`  
  }), {  
    headers: { ...corsHeaders, "Content-Type": "application/json" }  
  });  
});  