// Supabase Edge Function: ai-adjust  
// LLM adjusts difficulty + exercise mix based on 7-day rolling progress window  
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";  
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.4";  
  
const corsHeaders = {  
  "Access-Control-Allow-Origin": "*",  
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",  
};  
  
// DeepSeek API key from env; fallback to heuristic  
const getLLM = async (messages: any[]) => {  
  const apiKey = Deno.env.get("DEEPSEEK_API_KEY");  
  if (!apiKey) return null;  
  const resp = await fetch("https://api.deepseek.com/v1/chat/completions", {  
    method: "POST",  
    headers: { "Authorization": `Bearer ${apiKey}`, "Content-Type": "application/json" },  
    body: JSON.stringify({ model: "deepseek-chat", messages, temperature: 0.3 })  
  });  
  if (!resp.ok) return null;  
  const data = await resp.json();  
  const raw = data.choices?.[0]?.message?.content || "{\"contrast_ratio\":0.3,\"phase\":\"phase2\"}";  
  try { return JSON.parse(raw); } catch { return { contrast_ratio: 0.3, phase: "phase2", reason: "heuristic" }; }  
};  
  
serve(async (req) => {  
  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });  
  
  const body = await req.json().catch(() => ({}));  
  const user_id = body.user_id || "anonymous";  
  
  const supabaseAdmin = createClient(  
    Deno.env.get("SUPABASE_URL")!,  
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!  
  );  
  
  // Fetch last 7 days of progress  
  const sevenDaysAgo = new Date(Date.now() - 7 * 864e5).toISOString();  
  const { data: rows, error } = await supabaseAdmin  
    .from("progress_log")  
    .select("*, created_at")  
    .eq("user_id", user_id)  
    .gte("created_at", sevenDaysAgo)  
    .order("created_at", { ascending: false });  
  
  if (error || !rows?.length) {  
    return new Response(JSON.stringify({ contrast_ratio: 0.3, phase: "phase2", reason: "no history" }), {  
      headers: { ...corsHeaders, "Content-Type": "application/json" }  
    });  
  }  
  
  // Heuristic fallback if no LLM  
  const avg_gabor = rows.filter(r => r.gabor_threshold).reduce((a, r) => a + r.gabor_threshold, 0) / rows.length;  
  const avg_compliance = rows.reduce((a, r) => a + (r.compliance_min || 0), 0) / rows.length;  
  let phase = "phase2";  
  if (avg_gabor < 0.15 && avg_compliance > 18) phase = "phase3";  
  if (avg_gabor < 0.08 && avg_compliance > 20) phase = "phase4";  
  const contrast_ratio = Math.max(0.1, Math.min(0.9, 0.3 - (avg_gabor || 0.3) * 0.5));  
  
  // Try LLM refinement  
  const llmResult = await getLLM([  
    { role: "system", content: "You are a vision therapy AI. Given patient progress data, return ONLY JSON with adjusted contrast_ratio (float 0.1-0.9), phase (phase1|phase2|phase3|phase4), and reason (string)." },  
    { role: "user", content: `Patient progress (7d, ${rows.length} sessions): avg gabor=${avg_gabor.toFixed(3)}, avg compliance=${avg_compliance.toFixed(1)}min. Recommend next phase and contrast setting.` }  
  ]);  
  
  const result = llmResult || { contrast_ratio: parseFloat(contrast_ratio.toFixed(2)), phase, reason: "heuristic" };  
  
  return new Response(JSON.stringify(result), {  
    headers: { ...corsHeaders, "Content-Type": "application/json" }  
  });  
});  