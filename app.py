# Import necessary libraries
import streamlit as st

from googleapiclient.discovery import build
from pytube import YouTube
from pydub import AudioSegment
import os
import certifi
from combine import combine_audio_during_interval, detect_tempo, get_first_segment
os.environ['SSL_CERT_FILE'] = certifi.where()
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()

from dotenv import load_dotenv

load_dotenv() 
# Set up the API
api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


def get_video_id(search_term):
    # Make the request
    request = youtube.search().list(
        part='snippet',
        maxResults=1,
        q=search_term
    )
    response = request.execute()

    # Get the video ID
    video_id = response['items'][0]['id']['videoId']
    return video_id

def download_music(id):
    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)

    audio = yt.streams.get_audio_only()
    audio.download()

    # Specify the name of the downloaded .webm file and the output .mp3 file
    webm_file = audio.default_filename
    mp3_file = webm_file.replace(".mp4", ".mp3").replace(" ", "_")

    # Convert .webm to .mp3
    AudioSegment.from_file(webm_file).export(mp3_file, format="mp3")

    return mp3_file


## APP

# Set the title of the app
st.title('cowbell.ai')

# Create a text input for the song name
# musician_name = st.text_input('Enter musician name')
song_name = st.text_input('Enter song name')

# Create a dropdown for the instrument selection
instrument = st.selectbox('Select instrument', ['cowbell'])

# Create a dropdown for the position selection
position = st.selectbox('Select position', ['chorus'])
text_music_cowbell = st.empty()
music_player_cowbell = st.empty()
text_music = st.empty()
music_player_original = st.empty()
# Function to add cowbell to the music
def add_cowbell(song_name, instrument, position):
    # Your logic here to add cowbell to the music based on the song name, instrument, and position
    # ...
    video_id = get_video_id(song_name)
    audio_file = download_music(video_id)
    
    tempo = detect_tempo(audio_file)
    best_seg_start, best_seg_end, i = get_first_segment(audio_file)
    audio_with_tempo = combine_audio_during_interval(audio_file, './cowbell.mp3',tempo, best_seg_start, best_seg_end)
    return audio_with_tempo  # Return the path to the new audio file

# If the button is clicked, call the function to add cowbell to the music
if st.button('Add cowbell to music!'):
    music_player_cowbell.text('Synthesizing the music...')
    audio_file_path = add_cowbell(song_name, instrument, position)
    
    # Load the audio file
        # Remove '_combined' from old file name to create new file name
    original_file_name = audio_file_path.replace('_combined', '')
    original_file = open(original_file_name, "rb")

    audio_file = open(audio_file_path, "rb")
    st.text('Here is your music with cowbell!')
    # Play the audio file
    st.audio(audio_file)
    st.text('Here is your original music!')
    st.audio(original_file)

# Create a button that says "More Cowbell"
# if st.button('More Cowbell'):
#     st.write('You pressed the button for more cowbell!')

# Note: This is a placeholder app and doesn't actually perform any cowbell operations.
