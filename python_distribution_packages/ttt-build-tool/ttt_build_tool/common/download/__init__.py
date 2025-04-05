# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Code that downloads things and caches them so that they don’t have to be
redownloaded.
"""
import hashlib
import pathlib
import shutil
from typing import Final, NamedTuple

import requests_cache

from .. import DOWNLOADS_DIR, CACHE_DIRECTORY


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


class Downloadable(NamedTuple):
    """
    A file or directory that can be obtained on-demand from an internal
    cache or the Internet.

    This class will download a regular file. It can’t be used to
    download a video from sites like Niconico.

    This class caches its output. It won’t try to redownload something
    if it was already downloaded during a previous run of the
    ttt-build-tool.

    Fields:
    url — The Web address of the file that you want to download.

    expected_hash — The SHA3-256 hash of the file that we’re going to
    download. After the file is downloaded, its hash will be calculated
    and compared to expected_hash. If they don’t match, then an
    exception will be raised. This helps ensure that the code in this
    repo is reproducible. expected_hash should be set to a string of
    hexadecimal digits.

    save_path — Where to save the file, relative to
    dir_to_put_download_in(self.url). This should always be a relative
    path.

    archive_item_of_interest — Path to the item in the archive that we
    want to use. This path will be put at the end of the
    self.extracted_path’s return value.
    """
    url: str
    expected_hash: str
    save_path: pathlib.Path
    archive_item_of_interest: pathlib.Path

    def path(self) -> pathlib.Path:
        """
        Returns the path to a cached copy of the file at self.url.

        Raises a requests.RequestException if the file fails to
        download.
        """
        DESTINATION: Final = pathlib.Path(
            dir_to_put_download_in(self.url),
            self.save_path
        )
        if DESTINATION.exists():
            with DESTINATION.open(mode="rb") as file:
                ACTUAL_HASH_1: Final = (
                    hashlib.sha3_256(file.read()).hexdigest()
                )
            if ACTUAL_HASH_1 != self.expected_hash:
                raise ValueError(
                    f"A file was downloaded from {repr(self.url)} and "
                    + f"saved to {DESTINATION}. ttt-build-tool expected"
                    + " that its SHA3-256 hash would be "
                    + f"{repr(self.expected_hash)}, but its hash was "
                    + f"actually {repr(ACTUAL_HASH_1)}."
                )
        else:
            RESPONSE: Final = REQUESTS_SESSION.get(self.url)
            RESPONSE.raise_for_status()
            ACTUAL_HASH_2: Final = (
                hashlib.sha3_256(RESPONSE.content).hexdigest()
            )
            if ACTUAL_HASH_2 != self.expected_hash:
                raise ValueError(
                    f"A file was downloaded from {repr(self.url)}. "
                    + "ttt-build-tool expected that its SHA3-256 hash "
                    + f"would be {repr(self.expected_hash)}, but its "
                    + f"hash was actually {repr(ACTUAL_HASH_2)}."
                )
            DESTINATION.parent.mkdir(parents=True, exist_ok=True)
            with DESTINATION.open(mode="wb") as file:
                file.write(RESPONSE.content)
        return DESTINATION


    def extracted_path(self) -> pathlib.Path:
        """
        Assumes that the file located at self.url is an archive and
        returns a path to an item in a cached copy of the contents of
        the archive.

        If the file located at self.url isn’t actually an archive, or if
        it has an unsupported file extension, then this method will
        fail.

        When we download an archive (most of the time), we don’t want to
        do something with the entire contents of the archive. Instead,
        we want to do something with one of the files or directories
        that is inside of the archive. When using this method,
        self.archive_item_of_interest should be set to the path to the
        item in the archive that we care about, relative to the root of
        the archive. This method will return the path to that item.

        Raises a requests.RequestException if the file fails to
        download.
        """
        ARCHIVE_PATH: Final = self.path()
        EXTRACTED_DIR_PATH: Final = pathlib.Path(
            ARCHIVE_PATH.parent,
            "extracted"
        )
        if not EXTRACTED_DIR_PATH.exists():
            shutil.unpack_archive(
                ARCHIVE_PATH,
                EXTRACTED_DIR_PATH
            )
        return pathlib.Path(
            EXTRACTED_DIR_PATH,
            self.archive_item_of_interest
        )
