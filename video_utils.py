import subprocess
import os
from moviepy.editor import VideoFileClip


def split_video_by_segments(video_path, segments, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    clip_infos = []

    # Lấy thời lượng video
    video = VideoFileClip(video_path)
    video_duration = video.duration
    video.close()
    for i in range(len(segments)):
        start = segments[i]["start"]
        end = segments[i + 1]["start"] if i + 1 < len(segments) else video_duration
        segments[i]["end"] = end  # đảm bảo mỗi segment có 'end'

        output_file = os.path.join(output_dir, f"clip_{i:03d}.mp4")

        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start),
            "-to", str(end),
            "-i", video_path,
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            "-c:a", "aac",
            "-strict", "experimental",
            output_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        clip_infos.append((output_file, segments[i]))

    return clip_infos


def merge_video_clips(video_clip_infos, output_path):
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as list_file:
        for clip_info in video_clip_infos:
            path = clip_info[0]  # Lấy đường dẫn video từ tuple (path, segment)
            list_file.write(f"file '{os.path.abspath(path)}'\n")
        list_file_path = list_file.name

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_file_path,
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "23",
        "-c:a", "aac",
        "-strict", "experimental",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(list_file_path)
