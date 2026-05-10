// Supabase Edge Function: safety-scan
// Obstacle and hazard detection for accessibility safety alerts

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

const DETECT_API_URL = Deno.env.get("DETECT_API_URL") || "http://localhost:8000/detect";

serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });

  try {
    const { image_base64 } = await req.json();
    if (!image_base64) return new Response(JSON.stringify({ error: "image_base64 required" }), { status: 400 });

    const resp = await fetch(DETECT_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_base64, classes: ["person", "stairs", "door", "chair", "table", "bottle", "cup"] })
    });

    if (!resp.ok) throw new Error(`Detect API ${resp.status}`);
    const result = await resp.json();

    const hazards = ["stairs"];
    const warnings = [];
    for (const obj of result.objects || []) {
      if (hazards.includes(obj.name)) {
        warnings.push(`Caution: ${obj.name} detected at ${obj.position}.`);
      }
    }

    return new Response(JSON.stringify({
      warnings,
      total_objects: result.total,
      safe: warnings.length === 0
    }), {
      status: 200,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message, warnings: [], safe: true }), { status: 500 });
  }
});
