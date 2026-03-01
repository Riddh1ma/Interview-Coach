import ollama

def get_ai_feedback(question, transcript, emotion, confidence, speech_data):
    prompt = f'''
You are an expert interview coach. A candidate answered this interview question:
Question: {question}
Answer: {transcript}
Emotion detected: {emotion}
Confidence score: {confidence}/10
Filler words used: {speech_data['filler_count']}
Words per minute: {speech_data['wpm']} (ideal: 120-150)
Clarity score: {speech_data['clarity_score']}/10

Give structured feedback with these sections:
1. OVERALL SCORE (out of 10)
2. STRENGTHS (2-3 points)
3. AREAS TO IMPROVE (2-3 actionable tips)
4. IDEAL ANSWER STRUCTURE
5. ONE SENTENCE ENCOURAGEMENT

Keep it under 250 words.
'''
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response['message']['content']