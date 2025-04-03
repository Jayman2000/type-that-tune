# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Code that downloads things and caches them so that they don’t have to be
redownloaded.
"""
import hashlib
import pathlib
from typing import Final

import requests_cache

from . import DOWNLOADS_DIR, CACHE_DIRECTORY


REQUESTS_CACHE_CACHE_DIR: Final = (
    pathlib.Path(CACHE_DIRECTORY, "requests_cache")
)
REQUESTS_CACHE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
REQUESTS_SESSION: Final = requests_cache.CachedSession(
    REQUESTS_CACHE_CACHE_DIR,
    backend="filesystem",
    cache_control=True,
    # This is a workaround for this bug:
    # <https://github.com/requests-cache/requests-cache/issues/1078>
    serializer="yaml"
)


def dir_to_put_download_in(url: str) -> pathlib.Path:
    """
    Determines where inside DOWNLOADS_DIR a file should be saved.

    Even if the ttt-build-tool is run multiple times, it should only
    ever download files once. The ttt-build-tool stores its downloads in
    subdirectories of the DOWNLOADS_DIR directory so that they can be
    reused when the ttt-build-tool is run again.
    """
    URL_HASH: Final = hashlib.sha3_256(url.encode("utf-8")).hexdigest()
    return pathlib.Path(DOWNLOADS_DIR, URL_HASH)


def download_if_needed(
    url: str,
    relative_path: pathlib.Path,
    expected_hash: str
) -> pathlib.Path:
    """
    Download a regular file from url if necessary.

    This function will download a regular file. It can’t be used to
    download a video from sites like Niconico.

    This function caches its output. It won’t try to redownload
    something if it was already downloaded during a previous run of the
    ttt-build-tool.

    Parameters:
    url — The Web address of the file that you want to download.

    expected_hash — The SHA3-256 hash of the file that we’re going to
    download. After the file is downloaded, its hash will be calculated
    and compared to expected_hash. If they don’t match, then an
    exception will be raised. This helps ensure that the code in this
    repo is reproducible. expected_hash should be set to a string of
    hexadecimal digits.

    relative_path — Where to save the file, relative to
    dir_to_put_download_in(url).

    Return value: The path to the downloaded file.

    Raises a requests.RequestException if the file fails to download.
    """
    DESTINATION: Final = pathlib.Path(
        dir_to_put_download_in(url),
        relative_path
    )
    if DESTINATION.exists():
        with DESTINATION.open(mode="rb") as file:
            ACTUAL_HASH_1: Final = (
                hashlib.sha3_256(file.read()).hexdigest()
            )
        if ACTUAL_HASH_1 != expected_hash:
            raise ValueError(
                f"A file was downloaded from {repr(url)} and saved to "
                + f"{DESTINATION}. ttt-build-tool expected that its "
                + f"SHA3-256 hash would be {repr(expected_hash)}, but "
                + "its hash was actually {repr(ACTUAL_HASH_1)}."
            )
    else:
        RESPONSE: Final = REQUESTS_SESSION.get(url)
        RESPONSE.raise_for_status()
        ACTUAL_HASH_2: Final = (
            hashlib.sha3_256(RESPONSE.content).hexdigest()
        )
        if ACTUAL_HASH_2 != expected_hash:
            raise ValueError(
                f"A file was downloaded from {repr(url)}. "
                + "ttt-build-tool expected that its SHA3-256 hash would"
                + f" be {repr(expected_hash)}, but its hash was "
                + f"actually {repr(ACTUAL_HASH_2)}."
            )
        DESTINATION.parent.mkdir(parents=True, exist_ok=True)
        with DESTINATION.open(mode="wb") as file:
            file.write(RESPONSE.content)
    return DESTINATION
