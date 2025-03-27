import os
import sys
import subprocess
import whisper


def extract_audio(video_path, audio_path):
    """Extracts audio from an MP4 file using FFmpeg."""
    command = ["ffmpeg", "-i", video_path, "-q:a", "0", "-map", "a", audio_path, "-y"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def transcribe_audio(audio_path):
    """Transcribes audio to text using OpenAI Whisper."""
    model = whisper.load_model(
        "base"
    )  # Change to "small", "medium", or "large" if needed
    result = model.transcribe(audio_path)
    return result["text"]


def main(video_path, output_path):
    """Main function to process the video and convert speech to text."""
    if not os.path.exists(video_path):
        print("Error: File not found.")
        return

    audio_path = "temp_audio.wav"
    extract_audio(video_path, audio_path)
    text = transcribe_audio(audio_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Transcription saved to {output_path}")
    os.remove(audio_path)  # Clean up temporary audio file


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <video.mp4> <output.txt>")
    else:
        main(sys.argv[1], sys.argv[2])
