import os
import streamlit as st
from groq import Groq


def get_ai_feedback(question, transcript, emotion, confidence, speech_data):

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    prompt = f"""
You are an expert interview coach.

A candidate answered this interview question:

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

Keep the feedback under 250 words.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content