import os
import subprocess
from moviepy.editor import VideoFileClip

from downloader import download_youtube_video
from speak import translate_video
from transcriber import get_segments
from video_utils import split_video_by_segments, merge_video_clips

if __name__ == "__main__":
    yt_url = "https://www.youtube.com/watch?v=AW5ySkC2LdQ&ab_channel=MiniMoments-Adventure%26Play"
    output_folder = "temp"
    os.makedirs(output_folder, exist_ok=True)

    print("📥 Bước 1: Tải video YouTube...")
    video_path = download_youtube_video(yt_url, output_folder)

    print("📝 Bước 2: Phân tích lời thoại để lấy các đoạn (segments)...")
    segments = get_segments(video_path)
    print(f"🔍 Tổng số đoạn có thoại: {len(segments)}")

    print("📐 Bước 3: Chuyển sang các đoạn liên tiếp không mất đoạn...")
    full_segments = []
    video_duration = VideoFileClip(video_path).duration

    for i, seg in enumerate(segments):
        start = seg['start']
        end = segments[i + 1]['start'] if i + 1 < len(segments) else video_duration
        full_segments.append({"start": start, "end": end, "text": segments[i]["text"]})

    print(f"✂️ Bước 4: Cắt video thành {len(full_segments)} đoạn...")
    clip_paths = split_video_by_segments(video_path, full_segments, output_folder)

    print("🎬 Bước 5: Ghép các đoạn video lại để kiểm tra khớp...")
    final_output = "video.mp4"
    merge_video_clips(clip_paths, final_output)

    print("🌍 Bước 6: Dịch và lồng tiếng từng đoạn video...")
    translated_clips = []
    for i, (clip_path, segment) in enumerate(clip_paths):
        translated_path = os.path.join(output_folder, f"translated_{i:03d}.mp4")
        translate_video(clip_path, translated_path, segment["text"])
        translated_clips.append((translated_path, segment))

    print("🎞️ Bước 7: Ghép các đoạn đã dịch lại...")
    final_translated_output = "translated.mp4"
    merge_video_clips(translated_clips, final_translated_output)

    print("🎧 Bước 8: Tách nhạc nền từ video gốc...")
    background_audio = os.path.join(output_folder, "bg_music.aac")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", final_output,
        "-vn",
        "-acodec", "copy",
        background_audio
    ], check=True)

    print("🎚️ Bước 9: Trộn nhạc nền vào video dịch...")
    final_mixed_output = "translated_with_music.mp4"
    subprocess.run([
        "ffmpeg", "-y",
        "-i", final_translated_output,
        "-i", background_audio,
        "-filter_complex",
        "[1:a]volume=0.3[a1];[0:a][a1]amix=inputs=2:duration=first:dropout_transition=2[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        final_mixed_output
    ], check=True)

    print(f"\n✅ Video gốc đã lưu tại: {os.path.abspath(final_output)}")
    print(f"✅ Video dịch đã lưu tại: {os.path.abspath(final_translated_output)}")
    print(f"✅ Video dịch kèm nhạc nền đã lưu tại: {os.path.abspath(final_mixed_output)}")
