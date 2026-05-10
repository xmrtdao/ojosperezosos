# OjosPerezosos

**Multimodal AI Vision Assistant for Accessibility**

> "Your eyes when you need a rest — an AI that sees, reads, and describes the world aloud."

OjosPerezosos ("Lazy Eyes") is a multimodal accessibility assistant built for the AMD Developer Hackathon (Vision & Multimodal AI track). It helps users with visual fatigue, low vision, or temporary eye strain by describing scenes, reading text from images, and providing audio-guided navigation — all powered by AMD ROCm-accelerated vision and language models.

---

## Hackathon Track

**Vision & Multimodal AI** — OjosPerezosos combines scene understanding (image captioning), OCR (text extraction), object detection, and text-to-speech into a unified accessibility pipeline running on AMD MI300X GPUs.

---

## Features

1. **Scene Describe** — Point your camera at any scene. Get a rich audio description: "A busy kitchen counter with a red kettle, three apples, and a window showing a sunset."
2. **Text-to-Speech OCR** — Snap a photo of a document, sign, menu, or screen. The AI reads it aloud word-for-word.
3. **Object Finder** — "Where are my keys?" The AI scans the frame and answers: "Keys detected on the wooden table, near the left edge."
4. **Color Reader** — For colorblind users: "That shirt is navy blue with small white dots."
5. **Face Recognition Lite** — "Who is in front of me?" Names faces from a private contact gallery (opt-in, on-device).
6. **Reading Mode** — Point at a book page. The AI reads continuously, turning pages via swipe gestures.
7. **Safety Alerts** — "Caution: steps ahead" or "Obstacle detected at 2 o'clock."

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (Browser / PWA)                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Camera     │  │  Mic        │  │  Speaker / Earbuds  │  │
│  │  (WebRTC)   │  │  (Commands) │  │  (TTS Output)       │  │
│  └──────┬──────┘  └──────┬──────┘  └─────────────────────┘  │
└─────────┼──────────────┼───────────────────────────────────┘
          │                │
          ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│              AMD DEVELOPER CLOUD (ROCm/MI300X)              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  LLaVA-NeXT  │  │  PaddleOCR   │  │  YOLOv8      │        │
│  │  (Caption)   │  │  (Text Read) │  │  (Objects)   │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         └─────────────────┼─────────────────┘                │
│                           ▼                                  │
│              ┌────────────────────┐                          │
│              │  Piper / Coqui TTS │                          │
│              │  (Audio Output)    │                          │
│              └────────────────────┘                          │
│                                                              │
│              Supabase (Auth, DB, Edge Functions)              │
└─────────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component | Technology | AMD Optimized |
|-----------|-----------|---------------|
| Scene Captioning | LLaVA-NeXT 7B / 13B | vLLM on MI300X |
| OCR | PaddleOCR | ROCm PyTorch |
| Object Detection | YOLOv8 | ONNX Runtime ROCm |
| TTS | Coqui TTS / Piper | ROCm-accelerated |
| Backend | Supabase Edge Functions | Deno Deploy |
| DB | Supabase PostgreSQL | — |
| Demo | Vanilla JS PWA | Web Speech API fallback |

---

## Quick Start

```bash
# Clone
git clone https://github.com/xmrtdao/ojosperezosos.git
cd ojosperezosos

# Run demo locally
cd demo && python3 -m http.server 8080
```

Open `http://localhost:8080` → Allow camera & microphone → Tap screen to describe.

---

## Project Structure

```
ojosperezosos/
├── README.md
├── demo/
│   └── index.html          # Accessible PWA demo (screen reader friendly)
├── vision/
│   ├── caption.py            # LLaVA scene captioning
│   ├── ocr.py                # PaddleOCR text extraction
│   ├── detect.py             # YOLOv8 object detection
│   └── requirements.txt
├── tts/
│   ├── generate.py           # TTS pipeline
│   └── voices/
├── supabase/
│   ├── schema.sql            # descriptions, user_prefs, audio_cache
│   └── functions/
│       ├── describe-scene/    # Image → caption endpoint
│       ├── read-text/         # Image → OCR → TTS endpoint
│       ├── find-object/       # Object detection + spatial audio
│       └── speak/             # Text → audio URL
└── deploy/
    └── huggingface-space/    # Gradio demo for HF
```

---

## API Endpoints (Edge Functions)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/describe-scene` | POST | Accepts base64 image, returns rich caption |
| `/read-text` | POST | Image → extracted text + audio URL |
| `/find-object` | POST | Query + image → object location + distance |
| `/speak` | POST | Text → TTS audio URL (cached) |
| `/safety-scan` | POST | Image → obstacle/warning list |

---

## Vision Models

### Scene Captioning (LLaVA-NeXT)
```bash
# Serve on AMD MI300X via vLLM
python -m vllm.entrypoints.openai.api_server \
  --model liuhaotian/llava-v1.6-vicuna-7b \
  --tensor-parallel-size 1 \
  --device cuda
```

### OCR (PaddleOCR)
```bash
python vision/ocr.py --image test_menu.jpg --lang en
```

### Object Detection (YOLOv8)
```bash
python vision/detect.py --image test_room.jpg --classes keys,phone,glasses
```

---

## Accessibility Design

- **High contrast UI** — black background, large white/orange text
- **Full keyboard navigation** — Tab through all controls
- **ARIA labels** — Every button has descriptive `aria-label`
- **Screen reader optimized** — Results read automatically via Web Speech API
- **Haptic feedback** — Vibration on mobile for capture confirmation
- **Voice commands** — "Describe", "Read", "Find keys", "What color"

---

## Demo

Try the live demo: [https://huggingface.co/spaces/xmrtdao/ojosperezosos](https://huggingface.co/spaces/xmrtdao/ojosperezosos)

Or run locally:
```bash
cd demo
python3 -m http.server 8080
```

The demo supports:
- Tap to capture + auto describe
- Swipe left for OCR / text reading
- Swipe right for object search
- Voice commands via Web Speech API

---

## Team

- **Joe Lee** (DevGruGold / XMRT DAO) — Accessibility UX, edge functions, PWA
- **David Elze** (Cuddlefish Labs) — Vision models, ROCm optimization, TTS pipeline

---

## Hackathon Submission

- **Event:** AMD Developer Hackathon on lablab.ai
- **Track:** Vision & Multimodal AI
- **Repo:** https://github.com/xmrtdao/ojosperezosos
- **Build in Public:** Tweet thread @AIatAMD @lablabai
- **Tags:** `#AMDHackathon`, `#ROCm`, `#AccessibilityAI`, `#VisionAI`, `#A11y`

---

## License

MIT — open source, built for everyone.
