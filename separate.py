import subprocess
import os

def separate_audio(file_name, stems):
    """
    Separates an audio file into a specified number of stems (2, 4, or 5).

    :param file_name: Name of the audio file located in the "audio" directory.
    :param stems: Number of stems for separation, must be 2, 4, or 5.
    :return: None. The separated audio files are saved in the "output" directory.
    """
    
    # Check if the number of stems is valid
    if stems not in [2, 4, 5]:
        print("Invalid number of stems. Stems should be 2, 4, or 5.")
        return

    # Define the input audio file path
    audio_file = os.path.join("audio", file_name)
    
    # Define the output directory
    output_dir = "output"

    # Check if the audio file exists
    if not os.path.exists(audio_file):
        print(f"File {audio_file} does not exist.")
        return

    # Construct the spleeter command
    command = f"spleeter separate -p spleeter:{stems}stems -o {output_dir} {audio_file}"

    # Run the command using subprocess
    process = subprocess.run(command, shell=True, check=True)

    # Print the result
    if process.returncode == 0:
        print(f"Audio separation successful for {file_name} with {stems} stems!")
    else:
        print(f"Audio separation failed for {file_name} with {stems} stems!")

# Example usage
file_name = "AUDIO_6821.mp3"
stems = 4
separate_audio(file_name, stems)
