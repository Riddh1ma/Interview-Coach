from deepface import DeepFace
import os

# ── EMOTION DETECTION ──────────────────────────────────
CONFIDENCE_MAP = {
    'happy': 9,
    'neutral': 7,
    'surprise': 6,
    'sad': 4,
    'fear': 3,
    'angry': 3,
    'disgust': 2,
}

def analyze_emotions(frames_dir='frames'):
    frame_files = [f for f in os.listdir(frames_dir) if f.endswith('.jpg')]
    if not frame_files:
        return 'neutral', 5

    emotions = []
    for fname in frame_files[:5]:
        try:
            result = DeepFace.analyze(
                img_path=os.path.join(frames_dir, fname),
                actions=['emotion'],
                enforce_detection=False
            )
            emotions.append(result[0]['dominant_emotion'])
        except:
            pass

    if not emotions:
        return 'neutral', 5

    dominant = max(set(emotions), key=emotions.count)
    score = CONFIDENCE_MAP.get(dominant, 5)
    return dominant, score

# ── SPEECH ANALYSIS ────────────────────────────────────
FILLER_WORDS = [
    'um', 'uh', 'like', 'you know', 'sort of', 'kind of',
    'basically', 'literally', 'right', 'so yeah', 'i mean'
]

def analyze_speech(transcript: str, duration_seconds: int = 30):
    text_lower = transcript.lower()
    words = text_lower.split()
    total_words = len(words)

    filler_count = 0
    found_fillers = []
    for filler in FILLER_WORDS:
        count = text_lower.count(filler)
        if count > 0:
            filler_count += count
            found_fillers.append(f'{filler} ({count}x)')

    duration_minutes = duration_seconds / 60
    wpm = int(total_words / duration_minutes) if duration_minutes > 0 else 0

    if wpm < 100 or wpm > 180:
        pace = 'too slow' if wpm < 100 else 'too fast'
    else:
        pace = 'good'

    clarity_score = 10
    clarity_score -= min(filler_count, 4)
    if pace != 'good':
        clarity_score -= 2
    clarity_score = max(clarity_score, 1)

    return {
        'total_words': total_words,
        'filler_count': filler_count,
        'fillers_found': found_fillers,
        'wpm': wpm,
        'pace': pace,
        'clarity_score': clarity_score,
    }