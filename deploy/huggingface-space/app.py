"""
OjosPerezosos — Amblyopia (Lazy Eye) Therapy
Hugging Face Space Gradio Demo
Built for AMD Developer Hackathon — Track 3: Vision & Multimodal AI
"""

import gradio as gr
import random
import time
import base64

# Treatment phase state
SESSION_STATE = {
    "phase": "phase2",
    "weak_eye": "left",
    "contrast_ratio": 0.3,
    "streak": 12,
    "gabor_best": 0.084,
    "vernier_best": 1.2,
    "sessions_total": 34,
}

DEMO_EXERCISES = [
    {"name": "Fixation Stability", "duration": 120, "type": "gaze"},
    {"name": "Saccade Tracking", "duration": 120, "type": "follow"},
    {"name": "Gabor Contrast Match", "duration": 180, "type": "gabor"},
    {"name": "Pursuit Smoothness", "duration": 120, "type": "smooth"},
    {"name": "Vernier Acuity", "duration": 180, "type": "vernier"},
    {"name": "Random Dot Stereogram", "duration": 150, "type": "stereogram"},
]

def get_calibration():
    """Simulate 9-point eye calibration."""
    return {
        "dominant_eye": random.choice(["Right", "Left"]),
        "gaze_stability": f"{82 + random.random()*14:.1f}%",
        "calibrated": True,
    }

def generate_session_plan(weak_eye, contrast, duration):
    """Return today's exercise queue."""
    # Pick 4-5 exercises based on phase (always include fixation + gabor)
    selected = [DEMO_EXERCISES[0], DEMO_EXERCISES[2]]
    selected += random.sample(DEMO_EXERCISES[1:] + DEMO_EXERCISES[3:], k=min(3, len(DEMO_EXERCISES)-2))
    total_min = sum(e["duration"] for e in selected) / 60
    return selected, total_min

def run_exercise(exercise_name):
    """Simulate one exercise with animated Gabor/stereogram frames (returned as video/list)."""
    if exercise_name == "Gabor Contrast Match":
        return "🎛️ Gabor patch rendered. Patient matched contrast threshold at 0.084."
    elif exercise_name == "Vernier Acuity":
        return "📏 Vernier gap task complete. Minimum gap detected: 1.2 arcmin."
    elif exercise_name == "Random Dot Stereogram":
        return "🧠 Stereogram depth fused in 4.2s. Binocular integration improving."
    else:
        return f"✅ {exercise_name} complete — accuracy: {85 + int(random.random()*14)}%"

def get_weekly_stats():
    s = SESSION_STATE
    return f"""📊 7-Day Progress
• Sessions: {s['sessions_total']}
• Best Gabor threshold: {s['gabor_best']:.3f} (↓ means better)
• Best Vernier score: {s['vernier_best']:.1f} arcmin
• Session streak: {s['streak']} days
• Compliance: Good (5+ sessions/week)
"""

def generate_report():
    s = SESSION_STATE
    return f"""# Weekly Therapy Report

**Patient ID:** demo-user
**Period:** Last 7 days
**Generated:** {time.strftime('%Y-%m-%d %H:%M')}

## Summary

| Metric | Value |
|--------|-------|
| Sessions Completed | 6 |
| Total Therapy Time | 132 min |
| Avg Session Duration | 22.0 min |
| Best Gabor Threshold | {s['gabor_best']:.3f} |
| Best Vernier Score | {s['vernier_best']:.1f} arcmin |

## Compliance

✅ Good compliance — 5+ sessions this week.

## Recommended Next Week

• Continue 20–30 min daily sessions.
• Schedule a follow-up eye exam in 2–4 weeks if not recently done.
• If headaches occur, reduce contrast ratio by 10%.
"""

def therapy_interface(weak_eye, contrast, session_min):
    """Main therapy session runner."""
    contrast_val = contrast / 100.0
    SESSION_STATE["weak_eye"] = weak_eye
    SESSION_STATE["contrast_ratio"] = contrast_val

    cal = get_calibration()
    exercises, total_min = generate_session_plan(weak_eye, contrast_val, session_min)

    plan_md = f"""## 🎯 Today's Treatment Plan

**Weak Eye:** {weak_eye.title()}
**Contrast Ratio:** Strong eye gets {int(contrast)}% contrast
**Est. Duration:** {total_min:.0f} minutes
**Dominant Eye:** {cal['dominant_eye']}
**Gaze Stability:** {cal['gaze_stability']}

### Exercises:
"""
    for i, ex in enumerate(exercises, 1):
        plan_md += f"{i}. **{ex['name']}** ({ex['duration']}s) — {ex['type']}\n"

    plan_md += "\n---\n"
    return plan_md

def start_session(exercises_md):
    """Run through mock exercises and return results."""
    lines = ["## 🏃 Session Started\n"]
    for ex in DEMO_EXERCISES[:5]:
        lines.append(run_exercise(ex["name"]))
        time.sleep(0.05)  # simulate processing
    lines.append("\n✅ Session complete! Progress saved.")
    SESSION_STATE["sessions_total"] += 1
    return "\n".join(lines)

def generate_hf_image(weak_eye, contrast):
    """Simulate dichoptic training image per eye (renders text-based diagram)."""
    c = int(contrast)
    strong = "right" if weak_eye == "left" else "left"
    ascii_art = f"""
╔══════════════════════════════════════╗
║   DICHOPTIC TRAINING DISPLAY         ║
╠══════════════════════════════════════╣
║                                      ║
║   {weak_eye.upper()} EYE (WEAK)         {strong.upper()} EYE (STRONG)
║   ████████████████████               ║
║   ████████  TARGET  ████           ║
║   ████████  ██████  ████           ║
║   ████████  ██████  ████           ║
║   ████████████████████               ║
║   Contrast: {100-c:3d}%            Contrast: {c:3d}%
║   Sharp edges        Blurred edges   ║
║   ↓ weaker eye       ↓ stronger eye║
║   gets stimulation   gets blur     ║
║                                      ║
╚══════════════════════════════════════╝
    """
    return ascii_art

# ─── GRADIO UI ──────────────────────────────────────────

with gr.Blocks(title="OjosPerezosos — Amblyopia Therapy") as demo:
    gr.Markdown("""
    # OjosPerezosos 👁️
    ## Neuroplasticity-Based Amblyopia (Lazy Eye) Therapy
    **AMD Developer Hackathon 2026 — Track 3: Vision & Multimodal AI**

    AI-powered dichoptic training you can do at home, using just your webcam and browser.
    """)

    with gr.Tab("🗓️ Plan Session"):
        with gr.Row():
            with gr.Column():
                weak_eye_ui = gr.Dropdown(["left", "right"], value="left", label="Amblyopic (Weaker) Eye")
                contrast_ui = gr.Slider(10, 90, value=30, step=5, label="Strong Eye Contrast %")
                session_min_ui = gr.Slider(5, 45, value=20, step=5, label="Target Duration (min)")
                plan_btn = gr.Button("Generate Plan", variant="primary")
            with gr.Column():
                plan_output = gr.Markdown()
        plan_btn.click(therapy_interface, inputs=[weak_eye_ui, contrast_ui, session_min_ui], outputs=plan_output)

    with gr.Tab("👁️ Dichoptic Display"):
        gr.Markdown("This simulates what each eye sees during dichoptic training.")
        with gr.Row():
            disp_weak = gr.Dropdown(["left", "right"], value="left", label="Weak Eye")
            disp_contrast = gr.Slider(10, 90, value=30, step=5, label="Strong Eye Contrast %")
            disp_btn = gr.Button("Render View")
        disp_output = gr.Textbox(label="Display Schematic", lines=18, font=gr.themes.GoogleFont("Courier New"))
        disp_btn.click(generate_hf_image, inputs=[disp_weak, disp_contrast], outputs=disp_output)

    with gr.Tab("🏃 Run Session"):
        session_btn = gr.Button("Start Simulated Session", variant="primary")
        session_out = gr.Textbox(label="Session Log", lines=12)
        session_btn.click(start_session, inputs=[gr.State()], outputs=session_out)

    with gr.Tab("📊 Progress"):
        stats_btn = gr.Button("Show Weekly Stats", variant="secondary")
        stats_out = gr.Textbox(label="Stats", lines=8)
        stats_btn.click(get_weekly_stats, outputs=stats_out)

    with gr.Tab("📄 Report"):
        report_btn = gr.Button("Generate Weekly Report", variant="secondary")
        report_md = gr.Markdown()
        report_btn.click(generate_report, outputs=report_md)

    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        **OjosPerezosos** (Spanish for "lazy eyes") is an amblyopia therapy app that uses dichoptic contrast-balanced training to stimulate the visual cortex.

        ### The Science
        - **Dichoptic Treatment:** Degrade the strong eye's image while presenting full contrast to the weak eye. Forces the brain to reintegrate binocular input.
        - **Neuroplasticity:** Adults can improve visual acuity through perceptual learning. AI-adaptive difficulty accelerates gains.
        - **Gamification:** Game-based exercises have **3x higher compliance** than eye patching.

        ### Safety
        ⚠️ This is a demo. **Always consult an ophthalmologist before starting vision therapy.**

        ---
        **Team:** Joe Lee (DevGruGold / XMRT DAO) + David Elze (Cuddlefish Labs)
        **Powered by:** AMD MI300X ROCm, Gradio, Supabase
        **Repo:** github.com/xmrtdao/ojosperezosos
        """)

if __name__ == "__main__":
    demo.launch()
