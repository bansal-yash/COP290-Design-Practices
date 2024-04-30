import assemblyai as aai
import speech_recognition as sr
import whisper


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


def audio_to_text_whisper(audio_file, output_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    text = insert_line_breaks(result["text"])
    with open(output_file, "w") as f:
        f.write(text)


def audio_to_text_google(audio_file, output_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
        text = insert_line_breaks(text)
        with open(output_file, "w") as f:
            f.write(text)


def audio_to_text_assembly(audio_file, output_file):
    aai.settings.api_key = "e951a42220064b5f9074f35cc01d9667"
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(audio_file)
    text = insert_line_breaks(transcript.text)
    with open(output_file, "w") as f:
        f.write(text)

audio_to_text_whisper("audios/What's_Up_With_the_Militarization_of_Space?.mp3", "out.txt")