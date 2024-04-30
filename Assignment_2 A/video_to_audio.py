from moviepy.editor import VideoFileClip

def video_to_audio(video_file, audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(audio_file)

video_to_audio("videos/background.mp4", "audios/background.mp3")