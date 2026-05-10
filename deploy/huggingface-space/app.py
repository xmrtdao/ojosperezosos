"""
OjosPerezosos — Neuroplasticity-Based Amblyopia Therapy
HuggingFace Spaces Streamlit Demo
"""
import streamlit as st
import base64
import io
from PIL import Image
import json

st.set_page_config(page_title="OjosPerezosos Therapy", page_icon="👁️", layout="wide")

# CSS
st.markdown("""
<style>
.main-header { text-align:center; padding:1.5rem 1rem; }
.main-header h1 { font-size:2rem; background: linear-gradient(135deg,#ff3e3e,#ff6b35); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.phase-card { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:14px; padding:1rem; margin-bottom:1rem; }
.phase-card h4 { color:#ff6b35; margin-bottom:0.5rem; }
.cal-dot { display:inline-block; width:10px; height:10px; background:#ff3e3e; border-radius:50%; animation:pulse 2s infinite; }
@keyframes pulse { 0%,100%{box-shadow:0 0 0 0 rgba(255,62,62,0.5);} 50%{box-shadow:0 0 0 8px rgba(255,62,62,0);} }
.stat-box { background:rgba(255,255,255,0.03); border-radius:10px; padding:0.75rem; text-align:center; }
.stat-value { font-size:1.5rem; font-weight:700; color:#00c853; }
.stat-label { font-size:0.75rem; color:#888; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👁️ OjosPerezosos</h1><p style="color:#888;">Neuroplasticity-based amblyopia therapy · AI-adaptive · Home-based</p></div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Start Session", "Progress", "Settings"])

with tab1:
    col1, col2 = st.columns([1,1.5])
    with col1:
        st.subheader("Patient Profile")
        eye = st.selectbox("Amblyopic Eye", ["Auto-detect", "Left Eye", "Right Eye"])
        age = st.slider("Age", 4, 55, 25)
        severity = st.select_slider("Severity", options=["Mild", "Moderate", "Severe"])
        duration = st.slider("Session Duration", 5, 45, 20, step=5)

        st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
        if st.button("▶️ Start Therapy Session", type="primary"):
            st.session_state["session_active"] = True
            st.session_state["session_time"] = 0
            st.success("Session started! Follow the on-screen exercises.")

    with col2:
        st.subheader("Today's Exercise Plan")
        exercises = [
            {"name": "Fixation Stability", "type": "gaze", "mins": 3, "desc": "Hold gaze on central dot for 3 min"},
            {"name": "Saccade Tracking", "type": "follow", "mins": 3, "desc": "Follow the moving target smoothly"},
            {"name": "Gabor Contrast Match", "type": "gabor", "mins": 5, "desc": "Detect faint Gabor patches with weak eye"},
            {"name": "Vernier Gap Task", "type": "vernier", "mins": 4, "desc": "Align the offset lines using both eyes"},
            {"name": "Dichoptic Flanker", "type": "flanker", "mins": 5, "desc": "Suppress strong eye; recognize target with weak eye"},
        ]
        for i, ex in enumerate(exercises, 1):
            with st.container():
                st.markdown(f"""
                <div class="phase-card">
                    <h4>{i}. {ex['name']} <span style="color:#888; font-size:0.8rem;">({ex['mins']} min)</span></h4>
                    <p style="color:#aaa; font-size:0.85rem;">{ex['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

        st.info("Total daily goal: **20 min** · Current streak: **0 days**")

with tab2:
    st.subheader("Treatment Progress")
    st.caption("Note: This is a demo with synthetic data. Real progress would be stored in Supabase.")

    metric_cols = st.columns(4)
    metric_cols[0].markdown('<div class="stat-box"><div class="stat-value">0</div><div class="stat-label">Sessions Complete</div></div>', unsafe_allow_html=True)
    metric_cols[1].markdown('<div class="stat-box"><div class="stat-value">0m</div><div class="stat-label">Total Time</div></div>', unsafe_allow_html=True)
    metric_cols[2].markdown('<div class="stat-box"><div class="stat-value">—</div><div class="stat-label">Best Eye (logMAR)</div></div>', unsafe_allow_html=True)
    metric_cols[3].markdown('<div class="stat-box"><div class="stat-value">0%</div><div class="stat-label">Compliance</div></div>', unsafe_allow_html=True)

    st.markdown("""
    ### 4-Phase Treatment Protocol

    <div class="phase-card">
        <h4>Phase 1: Calibration (Sessions 1-3)</h4>
        <p style="color:#aaa; font-size:0.85rem;">Assess suppression zone, measure contrast threshold per eye, determine anisometropia type.</p>
    </div>
    <div class="phase-card">
        <h4>Phase 2: Force Integration (Sessions 4-30)</h4>
        <p style="color:#aaa; font-size:0.85rem;">20 min/day dichoptic games. Strong eye degraded, weak eye at full contrast.</p>
    </div>
    <div class="phase-card">
        <h4>Phase 3: Binocular Fusion (Sessions 31-60)</h4>
        <p style="color:#aaa; font-size:0.85rem;">Both eyes at 80%+ contrast. Depth perception tasks, stereograms.</p>
    </div>
    <div class="phase-card">
        <h4>Phase 4: Maintenance (Ongoing)</h4>
        <p style="color:#aaa; font-size:0.85rem;">10 min/week maintenance games. Alert if acuity regresses. Recalibrate quarterly.</p>
    </div>
    """)

    if st.button("📊 Export Progress CSV"):
        st.download_button("Download", "session,date,exercise,score\n1,2025-05-10,Fixation,85\n", file_name="ojosperezosos_progress.csv")

with tab3:
    st.subheader("Therapy Settings")
    st.slider("Strong Eye Contrast", 0.1, 1.0, 0.3, step=0.05)
    st.slider("Weak Eye Contrast", 0.1, 1.0, 1.0, step=0.05)
    st.selectbox("Diffusion Type", ["Gaussian blur", "Band-pass noise", "Texture deletion"])
    st.checkbox("Enable audio cues")
    st.checkbox("Enable parental dashboard notifications")
    st.checkbox("HIPAA-compliant data mode")

    st.markdown("---")
    st.markdown("**Medical Disclaimer:** This app is an adjunct to professional care. Consult an ophthalmologist before starting therapy.")

st.markdown("---")
st.caption("OjosPerezosos — AMD Developer Hackathon · Vision & Multimodal AI Track · OSS")
