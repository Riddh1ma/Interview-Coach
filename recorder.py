import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import cv2
import os
import time

SAMPLE_RATE = 16000

def record_audio_and_frames(audio_file='answer.wav', duration=30, frames_dir='frames'):
    os.makedirs(frames_dir, exist_ok=True)
    
    # Try different camera indexes
    cap = None
    for index in [0, 1, 2]:
        test = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        if test.isOpened():
            ret, frame = test.read()
            if ret and frame is not None:
                cap = test
                break
        test.release()

    # Start audio recording
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16',
        device=1
    )

    # Capture frames if camera works
    saved_frames = []
    if cap:
        start = time.time()
        frame_count = 0
        while time.time() - start < duration:
            ret, frame = cap.read()
            if ret and frame_count % 30 == 0:
                path = f'{frames_dir}/frame_{len(saved_frames)}.jpg'
                cv2.imwrite(path, frame)
                saved_frames.append(path)
            frame_count += 1
        cap.release()
    else:
        # No camera — just wait for audio
        sd.wait()

    sd.wait()
    write(audio_file, SAMPLE_RATE, audio)
    return audio_file, saved_frames