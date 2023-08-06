from pydub import AudioSegment
import simpleaudio as sa
import numpy as np

from pytube import YouTube
from pydub import AudioSegment

import msaf

url = "https://www.youtube.com/watch?v=-MsvER1dpjM"
yt = YouTube(url)

audio = yt.streams.get_audio_only()
audio.download()

# Specify the name of the downloaded .webm file and the output .mp3 file
webm_file = audio.default_filename
mp3_file = webm_file.replace(".mp4", ".mp3").replace(" ", "_")

# Convert .webm to .mp3
AudioSegment.from_file(webm_file).export(mp3_file, format="mp3")

print("Download and conversion completed!!")

def combine_audio_during_interval(main_audio_path, cowbell_audio_path, tempo, start_time, end_time):
    # Load both audio files
    main_audio = AudioSegment.from_mp3(main_audio_path)
    cowbell_audio = AudioSegment.from_mp3(cowbell_audio_path)

    # Compute the total play time
    main_audio_length = len(main_audio)

    # Convert start and end times to milliseconds
    start_time_ms = start_time * 1000
    end_time_ms = end_time * 1000

    # Calculate the interval between each beat (in milliseconds)
    interval = 60 / tempo * 1000  # Convert to milliseconds

    # Overlay the cowbell audio during the specified interval
    combined_audio = main_audio
    for i in np.arange(0, main_audio_length, interval):
        if start_time_ms <= i <= end_time_ms:  # Check if the current position is within the specified time range
            combined_audio = combined_audio.overlay(cowbell_audio, position=int(i))

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

# Extract the code into a function:
def get_segments(audio_file):
    # 2. Segment the file using the default MSAF parameters (this might take a few seconds)
    boundaries, labels = msaf.process(audio_file, feature='mfcc',
                                      boundaries_id = 'cnmf',plot=False)
    print('feature: mfcc')
    print('Estimated boundaries:', boundaries)
    print('Estimated labels:', labels)

    # 3. Save segments using the MIREX format
    out_file = 'segments.txt'
    print('Saving output to %s' % out_file)
    msaf.io.write_mirex(boundaries, labels, out_file)
    return boundaries, labels

# get the first segment that is longer than 10 seconds
def get_first_segment(audio_file):
    boundaries, labels = get_segments(audio_file)
    for i in range(2, len(boundaries)):
        if boundaries[i] - boundaries[i-1] > 10:
            return boundaries[i-1], boundaries[i], i


# Load the audio files
main_audio_path = mp3_file
short_audio_path = 'cowbell.mp3'
tempo = detect_tempo(mp3_file)  # Play the short audio at 120 BPM

best_seg_start, best_seg_end, i = get_first_segment(mp3_file)

print(best_seg_start, best_seg_end, i)

# Set the interval during which the cowbell should play (in seconds)
start_time = best_seg_start  # Start after 1 minute
end_time = best_seg_end   # End after 2 minutes

# Combine the audio files
combined_audio = combine_audio_during_interval(main_audio_path, short_audio_path, tempo, start_time, end_time)

# Play the combined audio
# play_audio(combined_audio)
# Save the combined audio to an MP3 file
combined_audio.export(mp3_file[:-4] + '_combined.mp3', format="mp3")
play_audio(combined_audio)