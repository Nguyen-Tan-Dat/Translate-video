from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import subprocess
import os
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import shutil


def translate_video(input_video_path: str, output_video_path: str, transcript_en: str, lang='vi'):
    # Bước 1: Dịch văn bản
    translated_text = GoogleTranslator(source='en', target=lang).translate(transcript_en)
    if not translated_text or translated_text.strip() == "":
        print("⚠️ Không có bản dịch. Sao chép video gốc sang output và giữ nguyên nhạc nền.")
        shutil.copy(input_video_path, output_video_path)
        return

    print("✅ Văn bản đã dịch:", translated_text)

    # Bước 2: Tạo giọng đọc từ văn bản dịch
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tts_file:
        gTTS(text=translated_text, lang=lang).save(tts_file.name)
        tts_path = tts_file.name

    # Bước 3: Tách nhạc nền từ video gốc
    background_audio_path = tts_path.replace('.mp3', '_bg.mp3')
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_video_path,
        "-q:a", "0",
        "-map", "a",
        background_audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Lấy độ dài video
    video_clip = VideoFileClip(input_video_path)
    video_duration = video_clip.duration

    # Lấy độ dài 2 âm thanh
    bg_audio = AudioSegment.from_file(background_audio_path)
    voice_audio = AudioSegment.from_file(tts_path)
    voice_duration = voice_audio.duration_seconds

    # Cân bằng thời lượng giữa âm thanh
    if voice_duration > video_duration:
        speed = video_duration / voice_duration
        adjusted_video_path = input_video_path.replace('.mp4', '_slowed.mp4')
        subprocess.run([
            'ffmpeg', '-y',
            '-i', input_video_path,
            '-filter:v', f"setpts={1 / speed}*PTS",
            '-an',
            adjusted_video_path
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        final_video_input = adjusted_video_path
    else:
        silence = AudioSegment.silent(duration=int((video_duration - voice_duration) * 1000))
        voice_audio += silence
        final_video_input = input_video_path

    # Cân bằng độ dài nhạc nền nếu cần
    if len(bg_audio) < len(voice_audio):
        bg_audio += AudioSegment.silent(duration=(len(voice_audio) - len(bg_audio)))
    else:
        bg_audio = bg_audio[:len(voice_audio)]

    # Giảm âm lượng nhạc nền và trộn
    bg_audio = bg_audio - 15  # giảm 15 dB để làm nền
    mixed_audio = bg_audio.overlay(voice_audio)

    # Xuất file âm thanh đã trộn
    mixed_audio_path = tts_path.replace('.mp3', '_mixed.m4a')
    mixed_audio.export(mixed_audio_path, format='ipod')  # ipod = m4a container

    # Bước 4: Ghép âm thanh đã trộn vào video
    subprocess.run([
        'ffmpeg', '-y',
        '-i', final_video_input,
        '-i', mixed_audio_path,
        '-c:v', 'copy',
        '-map', '0:v:0',
        '-map', '1:a:0',
        output_video_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Cleanup
    os.remove(tts_path)
    os.remove(background_audio_path)
    os.remove(mixed_audio_path)
    if 'adjusted_video_path' in locals():
        os.remove(adjusted_video_path)
    print(f"✅ Hoàn tất! Video đã dịch (giữ nhạc nền) lưu tại: {output_video_path}")
