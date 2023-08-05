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
