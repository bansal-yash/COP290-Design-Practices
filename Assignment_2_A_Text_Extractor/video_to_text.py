import audio_to_text
from moviepy.editor import VideoFileClip
import os


def video_to_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)


def insert_line_breaks(text, max_length=120):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            current_line += " " + word
        else:
            lines.append(current_line.strip())
            current_line = word
    if current_line:
        lines.append(current_line.strip())
    return "\n".join(lines)


def video_to_text(video_file, output_file):
    name = video_file.split(".")[0]
    video_to_audio(video_file, name + ".mp3")
    text = audio_to_text.audio_to_text_whisper(name + ".mp3")
    text = insert_line_breaks(text)
    with open(output_file, "w") as f:
        f.write(text)

    os.remove(name + ".mp3")


video_to_text("videos/news.mp4", "out.txt")
