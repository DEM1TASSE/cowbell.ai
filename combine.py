from pydub import AudioSegment
import simpleaudio as sa
import numpy as np

def combine_audio_with_tempo(main_audio_path, short_audio_path, tempo):
    # Load both audio files
    main_audio = AudioSegment.from_mp3(main_audio_path)
    short_audio = AudioSegment.from_mp3(short_audio_path)

    # Compute the total play time
    main_audio_length = len(main_audio)

    # Calculate the interval between each beat (in milliseconds)
    interval = 60 / tempo * 1000  # Convert to milliseconds

    # Add the shorter audio at each beat
    combined_audio = main_audio
    for i in np.arange(0, main_audio_length, interval):
        combined_audio = combined_audio.overlay(short_audio, position=int(i))

    return combined_audio

def play_audio(audio):
    # Convert stereo to mono
    audio = audio.set_channels(1)

    # Play audio
    audio_wave = np.array(audio.get_array_of_samples())
    play_obj = sa.play_buffer(audio_wave, 1, 2, audio.frame_rate)
    play_obj.wait_done()

# Load the audio files
main_audio_path = 'Headlines_Internet_Version.mp3'
short_audio_path = 'cowbell.mp3'
tempo = 152  # Play the short audio at 120 BPM

# Combine the audio files
combined_audio = combine_audio_with_tempo(main_audio_path, short_audio_path, tempo)

# Play the combined audio
play_audio(combined_audio)

