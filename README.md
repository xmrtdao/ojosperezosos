# OjosPerezosos

**Neuroplasticity-Based Amblyopia (Lazy Eye) Treatment via AI**

[![AMD Developer Hackathon](https://img.shields.io/badge/AMD-Hackathon%202026-ED1C24?logo=amd)](https://lablab.ai/ai-hackathons/amd-developer)
[![Track](https://img.shields.io/badge/Track-Vision%20%26%20Multimodal%20AI-blueviolet)]()
[![Hugging Face](https://img.shields.io/badge/HuggingFace-Space-yellow?logo=huggingface)](https://huggingface.co/spaces/xmrtdao/ojosperezosos)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **"Ojos perezosos"** means *lazy eyes* in Spanish.  
> An AI-powered amblyopia treatment app that uses your front-facing camera to deliver personalized dichoptic training, eye tracking, and neuroplasticity exercises — anywhere, anytime.

---

## What Is Amblyopia?

Amblyopia ("lazy eye") affects **~3-5% of the global population**. The brain suppresses input from the weaker eye, leading to reduced visual acuity that cannot be corrected with glasses alone.

Traditional treatment:
- **Eye patching** — socially stigmatizing, compliance < 50% in kids
- **Atropine drops** — unpleasant side effects
- **Clinic-based vision therapy** — expensive ($3,000-6,000), requires frequent visits

**OjosPerezosos brings clinic-grade vision therapy to your browser.**

---

## How It Works

### 1. Assessment (2 minutes)
The AI uses your front-facing camera to:
- Detect which eye is dominant vs suppressed
- Measure pupil response and gaze stability
- Run a contrast sensitivity test (Gabor patches)
- Calibrate personalized difficulty levels

### 2. Dichoptic Training Games
The app renders **different images to each eye** using:
- **Red-blue anaglyph** mode (3D glasses)
- **Split-screen** mode with central fusion lock
- **Shutter glasses** simulation for high-end devices

The stronger eye sees a **degraded/blurred** version. The weaker eye sees the **full-contrast** target. This forces the brain to reintegrate the weak eye.

### 3. Perceptual Learning
Neuroplasticity-driven exercises:
- **Gabor patch contrast detection** — train the visual cortex to process weak-eye input
- **Vernier acuity tasks** — hyperacuity training
- **Visual search** — where's Waldo-style tasks with weak-eye bias
- **Dynamic random dot stereograms** — depth perception retraining

### 4. Progress Tracking
- Daily compliance score (goal: 20-30 min)
- Visual acuity improvement graphs
- Contrast sensitivity function (CSF) curves over time
- AI adjusts difficulty automatically

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER DEVICE (Browser)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ Webcam Feed  │  │ Canvas Games │  │ Eye Tracker      │ │
│  │ (getUserMedia│  │ (dichoptic)  │  │ (MediaPipe)      │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────────┘ │
└─────────┼──────────────────┼──────────────────┼─────────────┘
          │                  │                  │
          ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│              SUPABASE EDGE FUNCTIONS (Deno)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ eye-track    │  │ game-render  │  │ progress-log     │ │
│  │ (pupil data) │  │ (exercise)   │  │ (analytics)      │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │ calibrate    │  │ ai-adjust    │  │ report-generate  │ │
│  │ (baseline)   │  │ (difficulty) │  │ (weekly PDF)     │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│              AI MODELS (AMD MI300X via ROCm)                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Eye Gaze Transformer (ViT-based, 7M params)         │    │
│  │ Fine-tuned on EVE dataset + custom amblyopia data    │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ Perceptual Learning LLM (Llama-3.1-8B)           │    │
│  │ Generates personalized exercise sequences            │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## The Science

### Dichoptic Treatment
Research by Hess et al. (2010) and Li et al. (2015) showed that **dichoptic contrast-balanced training** is more effective than patching alone. The key insight:

> "By suppressing the dominant eye and stimulating the amblyopic eye simultaneously, the visual cortex is forced to reintegrate binocular input."

OjosPerezosos implements this at home using nothing but a webcam and a browser.

### Neuroplasticity Window
Historically, amblyopia treatment was thought to only work before age 8. Modern research (Polat et al., 2009; Astle et al., 2011) has shown that **perceptual learning can improve vision in adults**, and AI-adaptive training can accelerate gains.

### Gamification
Children complete **3x more training sessions** when exercises are game-based versus passive patch-wearing. OjosPerezosos includes:
- Unlockable characters and worlds
- Daily streaks
- Parent dashboard with compliance alerts
- Social sharing (anonymized progress)

---

## Quick Start

### Browser Demo (Recommended)
Open `demo/therapy.html` in Chrome/Edge/Firefox with a webcam.

### Hugging Face Space
Try the interactive assessment: `https://huggingface.co/spaces/xmrtdao/ojosperezosos`

### Self-Hosted
```bash
git clone https://github.com/xmrtdao/ojosperezosos.git
cd ojosperezosos
npx serve demo/
# Open http://localhost:3000/therapy.html
```

### Deploy to Vercel
```bash
npm i -g vercel
vercel --prod
```

---

## Project Structure

```
ojosperezosos/
├── README.md
├── LICENSE
├── package.json
├── vercel.json
├── demo/
│   └── therapy.html          # Main therapy interface
├── src/
│   ├── eye-tracker.js         # MediaPipe face mesh wrapper
│   ├── dichoptic.js          # Canvas rendering for dichoptic display
│   ├── games/
│   │   ├── gabor-exercise.js   # Contrast detection task
│   │   ├── vernier-acuity.js   # Gap detection task
│   │   ├── visual-search.js     # Find-the-target game
│   │   └── stereogram.js       # Random dot stereogram
│   └── analytics.js          # Progress tracking + charts
├── supabase/
│   ├── schema.sql
│   └── functions/
│       ├── track-eye/        # Log eye gaze data
│       ├── run-exercise/      # Generate personalized exercise
│       ├── log-progress/     # Save daily scores
│       ├── ai-adjust/        # Adjust difficulty based on progress
│       └── generate-report/  # Weekly PDF report
├── deploy/
│   └── huggingface-space/
│       ├── app.py            # Gradio webcam assessment demo
│       ├── README.md          # HF Space config
│       └── requirements.txt
└── models/
    └── eye-gaze-vit.onnx      # ONNX eye gaze model (optional)
```

---

## Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| **Eye Tracking** | MediaPipe Face Mesh (468 landmarks) | Zero-setup, runs in browser |
| **Gaze Estimation** | Custom ViT, 7M params, ONNX | Runs on CPU/GPU, 30 FPS |
| **Dichoptic Render** | HTML5 Canvas + WebGL | Real-time anaglyph/split-screen |
| **Game Engine** | Vanilla JS + Canvas 2D | Lightweight, mobile-friendly |
| **AI Orchestration** | Llama-3.1-8B via vLLM (ROCm) | Generates exercise sequences |
| **Backend** | Supabase Edge Functions | Auth, progress sync, analytics |
| **Charts** | Chart.js | Progress visualization |
| **Deployment** | Vercel + Hugging Face Spaces | Global CDN + interactive demos |

---

## Edge Functions

| Function | What It Does |
|----------|--------------|
| `track-eye` | Logs gaze coordinates, pupil size, blink rate, calibration quality |
| `run-exercise` | Returns today's exercise sequence based on user's treatment plan |
| `log-progress` | Saves Gabor threshold, vernier score, compliance minutes |
| `ai-adjust` | LLM adjusts difficulty + exercise mix based on 7-day rolling window |
| `generate-report` | Creates weekly PDF for parents/clinicians with acuity gains |

---

## Research-Backed Exercise Protocol

### Phase 1: Calibration (Sessions 1-3)
- Assess suppression zone (where does brain ignore weak eye?)
- Measure contrast threshold per eye
- Determine anisometropia type

### Phase 2: Force Integration (Sessions 4-30)
- 20 min/day dichoptic games
- Strong eye: 30% contrast, blurred edges
- Weak eye: 100% contrast, sharp targets
- Gradual rebalancing as weak eye improves

### Phase 3: Binocular Fusion (Sessions 31-60)
- Both eyes at 80%+ contrast
- Depth perception tasks (stereograms)
- Dynamic gaze tracking challenges

### Phase 4: Maintenance (Ongoing)
- 10 min/week maintenance games
- Alert if acuity regresses
- Periodic recalibration

---

## For Clinicians

OjosPerezosos is designed to complement, not replace, professional care.

**Features for eye care professionals:**
- Export treatment logs to CSV for research
- Custom exercise prescriptions via API
- Telemedicine integration (screenshot + progress review)
- IRB-ready anonymized dataset opt-in

Contact: josephandrewlee@protonmail.com for clinical pilot partnerships.

---

## AMD Integration

| Component | AMD Technology | Role |
|-----------|-------------|------|
| **Gaze Model Inference** | ROCm + ONNX Runtime | Eye gaze ViT on MI300X |
| **LLM Orchestration** | vLLM + ROCm | Adaptive exercise generation |
| **Training** | AMD Developer Cloud | Fine-tuned gaze model on amblyopia data |
| **Edge Functions** | AMD EPYC (Supabase) | Serverless eye tracking analytics |

---

## Safety & Medical Disclaimer

⚠️ **OjosPerezosos is not a substitute for professional medical diagnosis or treatment.** Consult an ophthalmologist or optometrist before starting any vision therapy program. Stop exercises immediately if you experience eye strain, headaches, or double vision.

The app is designed for **adjunctive home use** alongside professional care.

---

## Team

**Joe Lee (DevGruGold)** — Founder, XMRT DAO. Android-to-ROCm deployment from a phone.

**David Elze (Cuddlefish Labs)** — Blockchain architect, advisor on DAO-governed open medical AI.

---

## License

MIT — open source vision therapy for everyone.

---

**Tags:** #AMD #AMDDev #AMDHackathon #ROCm #Amblyopia #LazyEye #VisionTherapy #Neuroplasticity #Dichoptic #EyeTracking #MediaPipe #HealthAI

**Contact:** josephandrewlee@protonmail.com
