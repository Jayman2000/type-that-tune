# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
import shutil
import subprocess
from typing import Final, Optional

import yt_dlp

from .. import common
from ..common import build_config, download


MEDIA_DIR: Final = pathlib.Path(common.GENERATED_DIR, "media")
__doc__ = f"""
Ensures that the files in the {MEDIA_DIR} directory exist.

The {MEDIA_DIR} directory contains all of the video files that Type That
Tune uses. This task makes sure that each of the video files exists. If
any of them does not exist, then this task will create it.

This task starts by ensure that required videos are preset in the
downloads cache directory. The downloads cache directory is located at:
    {common.DOWNLOADS_DIR}
If a required video is not in the downloads cache directory, then this
task will download it. The downloads cache directory is stored outside
of this repository in order to (hopefully) make sure that videos are
only downloaded once. The concern is that Niconico or YouTube might try
to block or rate limit users that download many videos.

Once this task has made sure that a video is in the downloads cache
directory, this task will then check if the video is present in the
{MEDIA_DIR} directory. If it is not, then the video will be transcoded
into a format that the Godot Engine supports and placed in the
{MEDIA_DIR} directory. Transcoding can take a very long time, so it’s
best to leave this task running in the background while you do other
stuff.
"""


class YTDLPLogger():
    """
    A pretty useless class.

    At the moment, this just hides yt-dlp’s output. Maybe in the future,
    I’ll make it do something that’s actually useful.

    The only reason why I created this was to appease the type checker.
    Once yt-dlp-types gets fixed, I won’t this class anymore.
    """
    @staticmethod
    def debug(_msg: str) -> None:
        pass

    @staticmethod
    def info(_msg: str) -> None:
        pass

    @staticmethod
    def warning(_msg: str) -> None:
        pass

    @staticmethod
    def error(_msg: str) -> None:
        pass


def locate_ffmpeg() -> pathlib.Path:
    FFMPEG_PATH: Final[Optional[str]] = shutil.which("ffmpeg")
    if FFMPEG_PATH is None:
        raise RuntimeError(
            "Couldn’t locate ffmpeg. Are you sure that ffmpeg is on "
            "your PATH?"
        )
    return pathlib.Path(FFMPEG_PATH)


def prepare_one_piece_of_media(
    url: str,
    name: str,
    additional_ffmpeg_args: tuple[str, ...] = tuple()
) -> None:
    CACHED_DOWNLOAD_PATH_NO_SUFFIX: Final = pathlib.Path(
        download.dir_to_put_download_in(url),
        "media"
    )
    CACHED_DOWNLOAD_PATH: Final = \
        CACHED_DOWNLOAD_PATH_NO_SUFFIX.with_suffix(".mkv")
    GENERATED_FILE_PATH: Final = pathlib.Path(
        MEDIA_DIR,
        name + ".ogv"
    )

    if not CACHED_DOWNLOAD_PATH.exists():
        YT_DLP_OPTIONS: Final[yt_dlp.YDLOpts] = {
            "logger": YTDLPLogger,
            "keepvideo": "True",
            "outtmpl": {
                "default": str(CACHED_DOWNLOAD_PATH_NO_SUFFIX)
            },
            "postprocessors": [
                {"key": "FFmpegVideoRemuxer", "preferedformat": "mkv" },
            ]
        }
        with yt_dlp.YoutubeDL(YT_DLP_OPTIONS) as downloader:
            downloader.download(url)

    if not GENERATED_FILE_PATH.exists():
        FFMPEG_COMMAND: Final[tuple[str, ...]] = (
            (
                str(FFMPEG_PATH),
                "-i", str(CACHED_DOWNLOAD_PATH),
                "-codec:v", "libtheora",
                "-qscale:v", "10",
                "-codec:a", "libvorbis",
                "-qscale:a", "10",
                "-y"
            )
            + additional_ffmpeg_args
            + (
                str(GENERATED_FILE_PATH.absolute()),
            )
        )
        subprocess.run(FFMPEG_COMMAND)


def perform_task(settings: build_config.BuildConfig) -> None:
    for directory in (common.CACHE_DIRECTORY, MEDIA_DIR):
        directory.mkdir(exist_ok=True, parents=True)

    FFMPEG_RESIZE_FILTER: Final = (
        "scale=width=1920"
        ":height=0"
        ":force_original_aspect_ratio=decrease"
    )

    prepare_one_piece_of_media(
        "https://youtu.be/XXU68uo9qUc",
        "clowns_tenth_anniversary"
    )
    prepare_one_piece_of_media(
        "https://youtu.be/ddWJatRxfz8",
        "glorious_octagon_of_destiny",
        ("-filter:v", FFMPEG_RESIZE_FILTER)
    )
    prepare_one_piece_of_media(
        "https://www.nicovideo.jp/watch/sm2057168",
        "ronald_mcdonald_insanity"
    )
    prepare_one_piece_of_media(
        "https://www.nicovideo.jp/watch/sm5718044",
        "mcdonalds_countdown"
    )
    prepare_one_piece_of_media(
        "https://www.nicovideo.jp/watch/sm11449123",
        "touhou_ran_ran_ru__dokeshi_boso_kuse"
    )
    prepare_one_piece_of_media(
        "https://www.nicovideo.jp/watch/sm13204470",
        "touhou_ran_ran_ru__dokeshi_kyo_hashi_yume_1st_stage"
    )


FFMPEG_PATH: Final[pathlib.Path] = locate_ffmpeg()
