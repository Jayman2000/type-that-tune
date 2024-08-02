from pathlib import Path
from yt_dlp import YoutubeDL

def main():
    generated_folder = Path("project", "generated")
    generated_folder.mkdir(parents=True, exist_ok=True)
    song = generated_folder / "8_sides_of_nico_nico_douga"
    if not song.with_suffix(".ogv").exists():
        options = {
            "keepvideo": True,
            "final_ext": "ogv",
            "outtmpl": {
                "default": str(song)
            },
            "postprocessors": [ 
                # Unfortunately, we have to remux into mkv before we can switch to difference video and audio codecs. I don’t know why.
                {"key": "FFmpegVideoRemuxer", "preferedformat": "mkv" },
                # This next one switches the video codec to Theora and the audio codec to Vorbis. It was inspired by <https://github.com/yt-dlp/yt-dlp/issues/7607#issuecomment-2050676387>. We need Theora video and Vorbis audio because that’s what Godot requires.
                {"key": "FFmpegCopyStream"},
                # This last one remuxes the video from mkv to ogv. Godot requires ogv.
                {"key": "FFmpegVideoRemuxer", "preferedformat": "ogv" }
            ],
            "postprocessor_args": {
                "copystream": [
                    "-codec:v", "libtheora", "-qscale:v", "10", "-codec:a", "libvorbis", "-qscale:a", "10"
                ]
            }
        }
        with YoutubeDL(options) as downloader:
            downloader.download(("https://www.youtube.com/watch?v=UmC-_bTCRwQ",))
