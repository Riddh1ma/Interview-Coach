# 🎙️ AI Interview Coach

An AI-powered interview coach that analyzes your speech, detects emotions, and gives personalized feedback.

## Built for AMD Slingshot Hackathon

## Features
- 🎤 Speech transcription using OpenAI Whisper
- 😊 Facial emotion detection using DeepFace
- 📊 Filler word detection and WPM analysis
- 🤖 AI feedback using Mistral (runs locally, free)
- 📈 Practice history tracking
- 3 question categories: HR, Behavioral, Technical

## Tech Stack
- Python 3.11, Streamlit, OpenCV, Whisper, DeepFace, Ollama + Mistral

## Setup
1. Clone the repo
2. py -3.11 -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt
5. Install Ollama from ollama.com then run: ollama pull mistral
6. streamlit run app.py