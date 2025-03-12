# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
import hashlib
import pathlib
import shutil
import subprocess
from typing import Final, Optional

import appdirs
import reuse._main
import reuse.project
import reuse.spdx
import reuse.vcs
import yt_dlp


CACHE_DIRECTORY: Final = pathlib.Path(appdirs.user_cache_dir(
    appname="ttt-build-tool",
    appauthor="Type That Tune contributors"
))
GENERATED_DIR: Final = pathlib.Path("project", "generated")
MEDIA_DIR: Final = pathlib.Path(GENERATED_DIR, "media")


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


def generate_license_related_files() -> int:
    ORIGINAL_LICENSES_PATH: Final = pathlib.Path("LICENSES")
    GENERATED_LICENSES_PATH: Final = pathlib.Path(
        GENERATED_DIR,
        "licenses"
    )
    if GENERATED_LICENSES_PATH.exists():
        shutil.rmtree(GENERATED_LICENSES_PATH)
    shutil.copytree(ORIGINAL_LICENSES_PATH, GENERATED_LICENSES_PATH)

    BOM_PATH: Final = pathlib.Path(
        GENERATED_DIR,
        "type_that_tune_legal_notices.spdx"
    )
    # I wish that calling reuse.spdx.run() didn’t require that I create
    # an ArgumentParser, but it does.
    REUSE_ARGUMENT_PARSER: Final = reuse._main.parser()
    reuse.spdx.add_arguments(REUSE_ARGUMENT_PARSER)
    REUSE_PROJECT: Final = reuse.project.Project(
        pathlib.Path.cwd(),
        vcs_strategy=reuse.vcs.VCSStrategyGit
    )
    with BOM_PATH.open(mode="w", encoding="utf-8") as bom_file:
        return reuse.spdx.run(
            REUSE_ARGUMENT_PARSER.parse_args(args=tuple()),
            REUSE_PROJECT,
            out=bom_file
        )


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
    URL_HASH: Final = hashlib.sha3_256(url.encode("utf-8")).hexdigest()
    CACHED_DOWNLOAD_PATH_NO_SUFFIX: Final = pathlib.Path(
        CACHE_DIRECTORY,
        "downloads",
        URL_HASH,
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


def prepare_all_media() -> None:
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


def main() -> int:
    for directory in (CACHE_DIRECTORY, MEDIA_DIR):
        directory.mkdir(exist_ok=True, parents=True)

    EXIT_STATUS: Final = generate_license_related_files()
    if EXIT_STATUS != 0:
        return EXIT_STATUS

    prepare_all_media()

    return 0

FFMPEG_PATH: Final[pathlib.Path] = locate_ffmpeg()
