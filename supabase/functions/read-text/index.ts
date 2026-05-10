// Supabase Edge Function: read-text
// Image → OCR text extraction + TTS audio

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

const OCR_API_URL = Deno.env.get("OCR_API_URL") || "http://localhost:8000/ocr";
const TTS_API_URL = Deno.env.get("TTS_API_URL") || "http://localhost:8000/speak";

serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });

  try {
    const { image_base64, language = "en" } = await req.json();
    if (!image_base64) return new Response(JSON.stringify({ error: "image_base64 required" }), { status: 400 });

    // 1. OCR extraction
    const ocrResp = await fetch(OCR_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ image_base64, language })
    });
    if (!ocrResp.ok) throw new Error(`OCR API ${ocrResp.status}`);
    const { full_text, lines } = await ocrResp.json();

    // 2. Generate TTS
    const ttsResp = await fetch(TTS_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: full_text })
    });
    let audio_url = null;
    if (ttsResp.ok) {
      const ttsData = await ttsResp.json();
      audio_url = ttsData.audio_url;
    }

    return new Response(JSON.stringify({ text: full_text, lines, audio_url }), {
      status: 200,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message, text: "", lines: [] }), { status: 500 });
  }
});
