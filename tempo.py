import librosa
import numpy as np


def detect_tempo(file_name):
    # Load the mp3 file
    y, sr = librosa.load(file_name)

    # Compute the spectral contrast
    S = np.abs(librosa.stft(y))
    contrast = librosa.feature.spectral_contrast(S=S, sr=sr)

    # Detect the onset strength envelope using spectral contrast
    onset_env = librosa.onset.onset_strength(S=contrast, sr=sr)

    # Use librosa's beat tracker to get the tempo and beat frames from the onset envelope
    tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    print(f"The detected tempo of the file '{file_name}' is: {tempo} BPM")


# You can use this function to detect the tempo of an mp3 file
# Just replace 'your_file.mp3' with the path to the mp3 file you want to analyze
detect_tempo('Headlines_Internet_Version.mp3')
