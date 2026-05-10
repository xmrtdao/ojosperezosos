// Supabase Edge Function: find-object
// Object detection with natural language query + spatial positioning

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

const DETECT_API_URL = Deno.env.get("DETECT_API_URL") || "http://localhost:8000/detect";

serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });

  try {
    const { image_base64, query = null } = await req.json();
    if (!image_base64) return new Response(JSON.stringify({ error: "image_base64 required" }), { status: 400 });

    const resp = await fetch(DETECT_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_base64, query })
    });

    if (!resp.ok) throw new Error(`Detect API ${resp.status}`);
    const result = await resp.json();

    // Format human-readable response
    const objects = result.objects || [];
    const formatted = objects.map((o: any) => {
      const pos = o.position || "center";
      return `${o.name} — ${Math.round(o.confidence * 100)}% confidence, located at ${pos}`;
    }).join("\n");

    return new Response(JSON.stringify({
      total: result.total,
      query: result.query,
      objects: result.objects,
      formatted_summary: formatted || "No objects detected matching your query."
    }), {
      status: 200,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message, total: 0, objects: [] }), { status: 500 });
  }
});
