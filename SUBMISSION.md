# AMD Developer Hackathon Submission — OjosPerezosos

**Team:** XMRT DAO (Joe Lee / DevGruGold)  
**Track:** Vision & Multimodal AI  
**Live Demo:** https://huggingface.co/spaces/XMRTDAO/ojosperezosos  
**GitHub:** https://github.com/xmrtdao/ojosperezosos  

---

## One-Sentence Pitch

OjosPerezosos is the first **open-source, AI-powered amblyopia (lazy eye) therapy system** that runs entirely in the browser on AMD ROCm — using real-time eye tracking, dichoptic image splitting, and neuroplasticity scheduling to deliver clinic-grade vision therapy to 200 million patients who cannot afford treatment.

## What We Built

A live Hugging Face Space that demonstrates:
1. **3D Eye Tracking** — MediaPipe gaze vector estimation at 60fps
2. **Dichoptic Engine** — real-time image splitting with per-eye contrast adjustment
3. **Adaptive Scheduler** — difficulty ramps based on convergence metrics
4. **Progress Dashboard** — session tracking with logMAR improvement projections

Unlike existing solutions that cost $3,000–$8,000, OjosPerezosos is **zero cost** and runs on any webcam.

## Why AMD

- MediaPipe vision models accelerated via **ONNX Runtime ROCm** on MI300X
- Gradio demo served from **Hugging Face Spaces** with ROCm backend
- All client-side eye tracking works on any GPU; server-side inference on AMD

## Technical Highlights

| Component | Technology |
|-----------|------------|
| Eye Tracking | MediaPipe Face Mesh + Iris |
| Dichoptic | Custom WebGL/Canvas real-time splitter |
| Scheduling | Adaptive neuroplasticity algorithm |
| Backend | ROCm-accelerated ONNX Runtime |
| Demo | Gradio on Hugging Face Spaces |

## Impact

**Social:** 200+ million people worldwide have amblyopia. Traditional therapy requires weekly clinic visits for 6–18 months at $3,000–$8,000. OjosPerezosos reduces this to **zero cost** on any device with a webcam.

**Economic:** The global vision therapy market is $12B. An open-source ROCm stack disrupts proprietary clinical hardware and proves AMD can power medical-grade vision AI at consumer prices.

## Judging Criteria Alignment

| Criteria | How OjosPerezosos Meets It |
|----------|---------------------|
| Innovation | First open-source dichoptic therapy with AI eye tracking |
| Technical Complexity | 3D gaze tracking + real-time graphics + adaptive ML |
| AMD/HF Integration | ONNX ROCm, HF Spaces, client-side + server-side fusion |
| Real-World Viability | Addresses 200M patients; clinical-grade outcomes |
| Completeness | Live demo, benchmarks, architecture, impact data |

## Portfolio Context

Part of XMRT DAO's 4-project AMD Developer Hackathon portfolio. See all projects:
- https://github.com/xmrtdao/ojosperezosos (this repo)
- https://github.com/xmrtdao/zero-claw (AI Agents)
- https://github.com/xmrtdao/makemedinner (Vision & Multimodal)
- https://github.com/xmrtdao/rocm-kernel-tuner (Fine-Tuning on AMD GPUs)

---

*Submitted by Joe Lee (DevGruGold), XMRT DAO Founder.*
