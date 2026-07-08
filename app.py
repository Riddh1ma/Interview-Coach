import streamlit as st
import random
import json
import os
from datetime import datetime
from questions import INTERVIEW_QUESTIONS
from transcriber import transcribe
from analyzer import analyze_speech
from feedback import get_ai_feedback

st.set_page_config(
    page_title='AI Interview Coach',
    page_icon='🎙️',
    layout='wide'
)

# ── Custom CSS for polished look ──────────────────────
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .score-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .score-good { border-top: 4px solid #28a745; }
    .score-mid  { border-top: 4px solid #ffc107; }
    .score-bad  { border-top: 4px solid #dc3545; }
    .history-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
</style>
""", unsafe_allow_html=True)

# ── Score history helpers ─────────────────────────────
HISTORY_FILE = 'history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    return []

def save_history(entry):
    history = load_history()
    history.append(entry)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history[-10:], f)  # keep last 10

def score_color(score):
    if score >= 8: return "score-good"
    if score >= 5: return "score-mid"
    return "score-bad"

# ── Header ────────────────────────────────────────────
st.markdown("# 🎙️ AI Interview Coach")
st.markdown("*Practice your interview skills with real-time AI feedback*")
st.divider()

# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    duration = st.slider("Recording duration (seconds)", 10, 60, 30)
    st.caption("💡 Ideal answers: 45–90 seconds")
    st.divider()

    # Score history in sidebar
    st.header("📈 Your Progress")
    history = load_history()
    if history:
        for h in reversed(history[-5:]):
            st.markdown(f"""
            <div class='history-card'>
                <small>{h['date']}</small><br>
                <b>{h['category']}</b> — {h['question'][:35]}...<br>
                Confidence: {h['confidence']}/10 | Clarity: {h['clarity']}/10
            </div>
            """, unsafe_allow_html=True)
        if st.button("🗑️ Clear History"):
            os.remove(HISTORY_FILE)
            st.rerun()
    else:
        st.info("No attempts yet. Start practicing!")

# ── Question selector ─────────────────────────────────
st.subheader("📌 Choose Your Category")
col_cat, col_q, col_btn = st.columns([1, 3, 1])

with col_cat:
    category = st.selectbox("Category", list(INTERVIEW_QUESTIONS.keys()))

if 'question' not in st.session_state or st.session_state.get('category') != category:
    st.session_state.question = random.choice(INTERVIEW_QUESTIONS[category])
    st.session_state.category = category

with col_q:
    st.info(f"**{st.session_state.question}**")

with col_btn:
    st.write("")
    st.write("")
    if st.button("🎲 New", use_container_width=True):
        st.session_state.question = random.choice(INTERVIEW_QUESTIONS[category])
        st.rerun()

st.divider()

# ── Record button ─────────────────────────────────────
# ── Browser-based audio recording ─────────────────────
st.subheader("🎙️ Record Your Answer")

audio_value = st.audio_input("Click the microphone and record your answer")

if audio_value is not None:
    st.audio(audio_value)

    if st.button(
        "🤖 Analyze My Answer",
        type="primary",
        use_container_width=True
    ):
        try:
            bar = st.progress(0, text="💾 Processing your recording...")

            # Save browser-recorded audio
            audio_file = "answer.wav"

            with open(audio_file, "wb") as f:
                f.write(audio_value.getbuffer())

            bar.progress(20, text="📝 Transcribing your speech...")

            transcript = transcribe(audio_file)

            bar.progress(45, text="🗣️ Analyzing your speech...")

            # Since cloud recording does not currently capture
            # continuous webcam frames, use neutral/default values.
            emotion = "neutral"
            confidence = 5

            speech_data = analyze_speech(transcript, duration)

            bar.progress(70, text="🤖 Generating AI feedback...")

            feedback = get_ai_feedback(
                st.session_state.question,
                transcript,
                emotion,
                confidence,
                speech_data
            )

            bar.progress(100, text="✅ Analysis complete!")

            # Save attempt to history
            save_history({
                'date': datetime.now().strftime("%b %d, %H:%M"),
                'category': category,
                'question': st.session_state.question,
                'confidence': confidence,
                'clarity': speech_data['clarity_score'],
                'wpm': speech_data['wpm'],
                'emotion': emotion,
            })

            # Store results
            st.session_state.results = {
                'transcript': transcript,
                'emotion': emotion,
                'confidence': confidence,
                'speech': speech_data,
                'feedback': feedback,
            }

            st.rerun()

        except Exception as e:
            st.error(f"An error occurred while analyzing your answer: {e}")
    

# ── Results ───────────────────────────────────────────
if 'results' in st.session_state:
    r = st.session_state.results
    s = r['speech']
    st.divider()
    st.subheader("📊 Your Results")

    # Score cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='score-card {score_color(r['confidence'])}'><h4>😊 Emotion</h4><h2>{r['emotion'].title()}</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='score-card {score_color(r['confidence'])}'><h4>💪 Confidence</h4><h2>{r['confidence']}/10</h2></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='score-card {score_color(s['clarity_score'])}'><h4>🗣️ Clarity</h4><h2>{s['clarity_score']}/10</h2></div>", unsafe_allow_html=True)
    with c4:
        wpm_score = 8 if 120 <= s['wpm'] <= 150 else 5
        st.markdown(f"<div class='score-card {score_color(wpm_score)}'><h4>⚡ WPM</h4><h2>{s['wpm']}</h2></div>", unsafe_allow_html=True)

    st.write("")

    # Transcript + Feedback
    col_t, col_f = st.columns(2)
    with col_t:
        st.subheader("📝 Your Answer")
        st.write(r['transcript'])
        if s['fillers_found']:
            st.error("⚠️ Filler words: " + ", ".join(s['fillers_found']))
        else:
            st.success("✅ No filler words detected!")

    with col_f:
        st.subheader("🤖 AI Feedback")
        st.write(r['feedback'])

    st.divider()
    if st.button("🔄 Try Again", use_container_width=True):
        del st.session_state.results
        st.session_state.question = random.choice(INTERVIEW_QUESTIONS[category])
        st.rerun()