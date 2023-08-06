from pydub import AudioSegment
import simpleaudio as sa
import numpy as np

from pytube import YouTube
from pydub import AudioSegment

url = "https://www.youtube.com/watch?v=cimoNqiulUE"
yt = YouTube(url)

audio = yt.streams.get_audio_only()
audio.download()

# Specify the name of the downloaded .webm file and the output .mp3 file
webm_file = audio.default_filename
mp3_file = webm_file.replace(".mp4", ".mp3").replace(" ", "_")

# Convert .webm to .mp3
AudioSegment.from_file(webm_file).export(mp3_file, format="mp3")

print("Download and conversion completed!!")

def combine_audio_with_tempo(main_audio_path, short_audio_path, tempo):
    main_audio = AudioSegment.from_mp3(main_audio_path)
    short_audio = AudioSegment.from_mp3(short_audio_path)

    # Compute the total play time
    main_audio_length = len(main_audio)

    # Calculate the interval between each beat (in milliseconds)
    interval = 60 / tempo * 1000  # Convert to milliseconds

    # Add the shorter audio at each beat
    combined_audio = main_audio
    beat_counter = 0
    for i in np.arange(0, main_audio_length, interval):
        if beat_counter % 2 == 0 or True:  # Play the short audio only on even beats
            combined_audio = combined_audio.overlay(short_audio, position=int(i))
        beat_counter += 1

    return combined_audio

def play_audio(audio):
    # Convert stereo to mono
    audio = audio.set_channels(1)

    # Play audio
    audio_wave = np.array(audio.get_array_of_samples())
    play_obj = sa.play_buffer(audio_wave, 1, 2, audio.frame_rate)
    play_obj.wait_done()

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
    return int(tempo)

# Load the audio files
main_audio_path = mp3_file
short_audio_path = 'cowbell.mp3'
tempo = detect_tempo(mp3_file)  # Play the short audio at 120 BPM

# Combine the audio files
combined_audio = combine_audio_with_tempo(main_audio_path, short_audio_path, tempo)

# Play the combined audio
# play_audio(combined_audio)
# Save the combined audio to an MP3 file
combined_audio.export(mp3_file[:-4] + '_combined.mp3', format="mp3")
# play_audio(combined_audio)