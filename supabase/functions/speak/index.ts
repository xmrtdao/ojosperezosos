// Supabase Edge Function: speak
// General TTS endpoint with caching

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";

const TTS_API_URL = Deno.env.get("TTS_API_URL") || "http://localhost:8000/speak";

serve(async (req) => {
  if (req.method !== "POST") return new Response("POST only", { status: 405 });

  try {
    const { text, voice = "default", language = "en" } = await req.json();
    if (!text) return new Response(JSON.stringify({ error: "text required" }), { status: 400 });

    // Compute hash for cache
    const encoder = new TextEncoder();
    const hashBuf = await crypto.subtle.digest("SHA-256", encoder.encode(text + voice + language));
    const hash = Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, "0")).join("");

    const resp = await fetch(TTS_API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, voice, language, hash })
    });

    if (!resp.ok) throw new Error(`TTS API ${resp.status}: ${await resp.text()}`);
    const { audio_url } = await resp.json();

    return new Response(JSON.stringify({ audio_url, text_hash: hash, text }), {
      status: 200,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  } catch (e: any) {
    return new Response(JSON.stringify({ error: e.message }), { status: 500 });
  }
});
