import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# IMPORTANT: Set your ffmpeg bin path here
FFMPEG_PATH = r"C:\Users\faiz9\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"


def ask_input_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select YouTube links file",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if not file_path:
        messagebox.showerror("Error", "No file selected!")
        return None

    return file_path


def read_links(file_path):
    links = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if url and not url.startswith("#"):
                links.append(url)
    return links


def run_command(cmd):
    process = subprocess.run(cmd)
    return process.returncode


def download_audio(urls, audio_folder, archive_file):
    print("\n=== Downloading Audio (MP3 Best Quality) ===\n")

    cmd = [
        "python", "-m", "yt_dlp",
        "--newline",
        "--progress",
        "--download-archive", str(archive_file),

        "--ffmpeg-location", FFMPEG_PATH,

        "-x",
        "--audio-format", "mp3",
        "--audio-quality", "0",

        "-o", str(audio_folder / "%(title)s.%(ext)s"),
    ] + urls

    code = run_command(cmd)

    if code != 0:
        print("\n❌ Audio download failed!")
    else:
        print("\n✅ Audio download completed successfully.")


def download_video(urls, video_folder, archive_file):
    print("\n=== Downloading Video (720p MP4 with Audio) ===\n")

    cmd = [
        "python", "-m", "yt_dlp",
        "--newline",
        "--progress",
        "--download-archive", str(archive_file),

        "--ffmpeg-location", FFMPEG_PATH,

        "-f", "bv*[height<=720]+ba/b[height<=720]",
        "--merge-output-format", "mp4",
        "--recode-video", "mp4",

        "-o", str(video_folder / "%(title)s.%(ext)s"),
    ] + urls

    code = run_command(cmd)

    if code != 0:
        print("\n❌ Video download failed!")
    else:
        print("\n✅ Video download completed successfully.")

def main():
    input_file = ask_input_file()
    if not input_file:
        return

    input_path = Path(input_file)
    links = read_links(input_file)

    if not links:
        messagebox.showerror("Error", "No valid links found in file!")
        return

    base_name = input_path.stem

    # OUTPUT FOLDER will be created where input file is located
    output_root = input_path.parent / f"output_{base_name}"

    audio_folder = output_root / "audio"
    video_folder = output_root / "video"

    audio_folder.mkdir(parents=True, exist_ok=True)
    video_folder.mkdir(parents=True, exist_ok=True)

    archive_audio = output_root / "archive_audio.txt"
    archive_video = output_root / "archive_video.txt"

    print(f"\nInput file: {input_file}")
    print(f"Total links: {len(links)}")
    print(f"Saving to: {output_root}\n")

    download_audio(links, audio_folder, archive_audio)
    download_video(links, video_folder, archive_video)

    messagebox.showinfo("Done", f"Downloads finished!\nSaved in:\n{output_root}")

if __name__ == "__main__":
    main()