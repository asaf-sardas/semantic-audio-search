import whisper

model = whisper.load_model("tiny.en")
result = model.transcribe("media/sample.mp3")
print(result["text"])