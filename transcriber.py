import whisper


def get_segments(video_path):
    model = whisper.load_model("medium")
    result = model.transcribe(video_path)
    return result['segments']
