import whisper

model = whisper.load_model('base')

def transcribe(audio_file='answer.wav'):
    result = model.transcribe(audio_file)
    return result['text']
