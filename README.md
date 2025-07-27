# 🎥 Translate-Video

**Translate-Video** là một công cụ giúp bạn tự động:
1. Phân đoạn video bằng Whisper.
2. Dịch phụ đề sang ngôn ngữ mong muốn.
3. Tạo giọng nói bằng Google Text-to-Speech (gTTS).
4. Ghép giọng nói đã dịch vào video gốc.
5. Kết xuất video đầu ra với ngôn ngữ mới.

## 🧠 Công nghệ sử dụng

- [Whisper](https://github.com/openai/whisper) – Nhận diện giọng nói tự động từ video.
- [deep-translator](https://github.com/nidhaloff/deep-translator) – Dịch văn bản qua Google Translate.
- [gTTS](https://pypi.org/project/gTTS/) – Chuyển văn bản sang giọng nói.
- [moviepy](https://zulko.github.io/moviepy/) – Cắt video.
- [FFmpeg](https://ffmpeg.org/) – Ghép âm thanh và video.

## 🧰 Cài đặt

# Audio / Video processing
ffmpeg-python
moviepy~=1.0.3
pydub~=0.25.1
spleeter~=2.4.0
librosa
soundfile
noisereduce

# Text-to-Speech (TTS)
gtts~=2.5.4
edge-tts
playsound~=1.3.0


# Translation
deep-translator~=1.11.4
googletrans==4.0.0-rc1
translate

# YouTube downloader / transcript
yt-dlp~=2025.7.21
youtube-transcript-api
