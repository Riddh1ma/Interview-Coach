# 🎙️ AI Interview Coach

An AI-powered interview preparation platform that helps candidates practice interview questions, analyze their speaking patterns, and receive personalized AI-generated feedback.

The platform combines speech recognition, communication analysis, and generative AI to provide actionable insights that help users improve their interview performance.

## 🚀 Live Demo

Try the deployed application:

**[Launch AI Interview Coach](https://interview-coach-r.streamlit.app/)**

## ✨ Features

- 🎤 **Browser-Based Voice Recording** — Record interview responses directly from the application.
- 📝 **AI Speech Transcription** — Converts spoken responses into text using OpenAI Whisper.
- 📊 **Speech Analysis** — Evaluates speaking pace, words per minute, filler words, and clarity.
- 🤖 **AI-Generated Feedback** — Provides structured and personalized interview feedback using a cloud-hosted LLM.
- 💡 **Actionable Recommendations** — Identifies strengths and suggests areas for improvement.
- 📈 **Progress Tracking** — Stores recent interview attempts and performance scores.
- 🎯 **Multiple Interview Categories** — Practice HR, behavioral, and technical interview questions.
- 🎲 **Dynamic Question Selection** — Generate different questions for repeated practice sessions.
- 📱 **Interactive Interface** — Clean and responsive UI built using Streamlit.

## 🧠 How It Works

The application follows the following processing pipeline:

User selects an interview question  
↓  
Records an answer using the browser microphone  
↓  
Audio is processed using FFmpeg  
↓  
Whisper converts speech to text  
↓  
Speech patterns and filler words are analyzed  
↓  
The AI model evaluates the response  
↓  
Personalized feedback and performance scores are generated  
↓  
Results are displayed on the interactive dashboard  

## 🏗️ System Architecture

The application consists of multiple components responsible for different stages of the interview analysis process.

### Frontend

**Streamlit**

Provides the interactive user interface for:

- Selecting interview categories
- Recording interview responses
- Displaying transcripts
- Viewing performance scores
- Receiving AI-generated feedback
- Tracking previous interview attempts

### Speech Recognition

**OpenAI Whisper**

Converts the recorded interview response into text for further analysis.

### Speech Analysis

The application analyzes:

- Total word count
- Words per minute (WPM)
- Speaking pace
- Filler word frequency
- Communication clarity

### AI Feedback Generation

The transcript and communication metrics are sent to a cloud-hosted Large Language Model through the Groq API.

The model generates structured feedback containing:

- Overall interview score
- Key strengths
- Areas for improvement
- Recommended answer structure
- Personalized encouragement

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core programming language |
| Streamlit | Web application framework |
| OpenAI Whisper | Speech-to-text transcription |
| FFmpeg | Audio processing |
| Groq API | Cloud-based AI inference |
| Llama 3.1 | AI feedback generation |
| NumPy | Numerical processing |
| SciPy | Audio and scientific processing |
| Git & GitHub | Version control and source code hosting |
| Streamlit Community Cloud | Application deployment |

## 📂 Project Structure

```text
Interview-Coach/
│
├── app.py
├── analyzer.py
├── feedback.py
├── questions.py
├── transcriber.py
│
├── requirements.txt
├── packages.txt
├── runtime.txt
├── README.md
└── .gitignore
