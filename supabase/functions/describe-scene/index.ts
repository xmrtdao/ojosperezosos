// Supabase Edge Function: describe-scene
// Image → LLaVA caption → TTS audio

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

const VISION_API = Deno.env.get("VISION_API_URL") || "http://localhost:8000/describe";
const TTS_API = Deno.env.get("TTS_API_URL") || "http://localhost:8000/speak";

serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });

  try {
    const { image_base64, detail = "standard" } = await req.json();
    if (!image_base64) return new Response(JSON.stringify({ error: "image_base64 required" }), { status: 400 });

    // 1. Get caption from vision model
    const capResp = await fetch(VISION_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_base64, detail })
    });
    if (!capResp.ok) throw new Error(`Vision API ${capResp.status}`);
    const { caption } = await capResp.json();

    // 2. Generate TTS for caption
    const ttsResp = await fetch(TTS_API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: caption })
    });
    let audio_url = null;
    if (ttsResp.ok) {
      const ttsData = await ttsResp.json();
      audio_url = ttsData.audio_url;
    }

    return new Response(JSON.stringify({ caption, audio_url }), {
      status: 200,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
});
