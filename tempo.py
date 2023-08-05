import librosa

def detect_tempo(file_name):
    # Load the mp3 file
    y, sr = librosa.load(file_name)

    # Use librosa's beat tracker to get the tempo and beat frames
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    print(f"The detected tempo of the file '{file_name}' is: {tempo} BPM")

    print(f"Saving the beat frames to '{file_name}_beat_frames.txt'")
    # Save the beat frames to a text file
    with open(f'{file_name}_beat_frames.txt', 'w') as f:
        for i, beat_frame in enumerate(beat_frames):
            f.write(f'{beat_frame}_{i}\n')
            

# You can use this function to detect the tempo of an mp3 file
# Just replace 'your_file.mp3' with the path to the mp3 file you want to analyze
detect_tempo('Headlines_Internet_Version.mp3')
