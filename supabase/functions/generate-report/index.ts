// Supabase Edge Function: generate-report  
// Create weekly PDF report for parents/clinicians with acuity gains  
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
  const week_days = body.week_days || 7;  
  
  const supabaseAdmin = createClient(  
    Deno.env.get("SUPABASE_URL")!,  
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!  
  );  
  4;  
  const startDate = new Date(Date.now() - week_days * 864e5).toISOString();  
  const { data: rows, error } = await supabaseAdmin  
    .from("progress_log")  
    .select("*")  
    .eq("user_id", user_id)  
    .gte("created_at", startDate)  
    .order("created_at", { ascending: false });  
  4;  
  if (error) return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: corsHeaders });  
  4;  
  const sessions = Array.from(new Set(rows?.map(r => r.session_id) || []));  
  const total_min = rows?.reduce((a, r) => a + (r.compliance_min || 0), 0) || 0;  
  const avg_compliance = sessions.length ? (total_min / sessions.length) : 0;  
  const best_gabor = rows?.filter(r => r.gabor_threshold).reduce((a, r) => Math.min(a, r.gabor_threshold), Infinity);  
  const best_vernier = rows?.filter(r => r.vernier_score).reduce((a, r) => Math.min(a, r.vernier_score), Infinity);  
  4;  
  const markdown = `# Weekly Vision Therapy Report  
  
**Patient ID:** ${user_id}  
**Period:** Last ${week_days} days  
**Report Generated:** ${new Date().toISOString()}  
  
---  
  
## Summary  
  
| Metric | Value |  
|--------|-------|  
| Sessions Completed | ${sessions.length} |  
| Total Therapy Time | ${total_min} min |  
| Avg Session Duration | ${avg_compliance.toFixed(1)} min |  
| Best Gabor Threshold | ${isFinite(best_gabor) ? best_gabor.toFixed(3) : "N/A"} |  
| Best Vernier Score | ${isFinite(best_vernier) ? best_vernier.toFixed(2) : "N/A"} |  
  
## Compliance  
  
${sessions.length >= 5 ? "✅ Good compliance — 5+ sessions this week." : "⚠️ Consider increasing frequency — fewer than 5 sessions per week may slow progress."}  
## Recommended Next Week  
  
- Continue 20–30 min daily sessions.
- Schedule a follow-up eye exam in 2–4 weeks if not recently done.
- If headaches occur, reduce contrast ratio by 10%.
  
---  
  
*OjosPerezosos — AI-powered amblyopia therapy*  
`;  
    return new Response(JSON.stringify({ report: markdown.trim(), sessions: sessions.length, total_min, avg_compliance }), {  
    headers: { ...corsHeaders, "Content-Type": "application/json" }  
  });  
});   
