import pyaudio
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Parameters
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# Initialize PyAudio
p = pyaudio.PyAudio()

# Start stream (make sure to select your loopback device)
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Recording...")

try:
    while True:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Process the audio data (extract features)
        mel_spectrogram = librosa.feature.melspectrogram(
            y=audio_data.astype(np.float32), sr=RATE, n_mels=120)
        mel_spectrogram_db = librosa.power_to_db(
            mel_spectrogram, ref=np.max)

        # Visualize the mel_spectrogram
        plt.figure(figsize=(10, 4))
        librosa.display.specshow(
            mel_spectrogram_db, sr=RATE, x_axis='time', y_axis='mel', fmax=8000)
        plt.colorbar(format='%+2.0f db')
        plt.title('Mel Spectrogram')
        plt.tight_layout()
        plt.show()

except KeyboardInterrupt:
    print("Stopping...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
