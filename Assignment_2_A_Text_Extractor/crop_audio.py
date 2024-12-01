from moviepy.editor import AudioFileClip
import math
import os


def crop_audio(input_file):
    audio_clip = AudioFileClip(input_file)
    duration = audio_clip.duration
    n = math.ceil(duration / 30)
    name = input_file.split(".")[0]
    ext = input_file.split(".")[1]
    for i in range(1, n):
        cropped_clip = audio_clip.subclip(30 * (i - 1), 30 * i + 0.5)
        cropped_clip.write_audiofile(name + str(i) + "." + ext)

    cropped_clip = audio_clip.subclip(30 * (n - 1) - 0.5, duration)
    cropped_clip.write_audiofile(name + str(n) + "." + ext)

    return n


def delete_audios(input_file, n):
    name = input_file.split(".")[0]
    ext = input_file.split(".")[1]

    for i in range(1, n + 1):
        os.remove(name + str(i) + "." + ext)
