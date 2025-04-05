# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Ensure that all Downloadables are functional.

Sometimes, the ttt-build-tool needs to download and extract a file from
the Internet. The ttt-build-tool does this using Downloadable objects.
Downloadable objects have a few attributes. Each of those attributes
needs to be set correctly, or else the Downloadable object will not work
properly. This task checks all of those properties in order to make sure
that they are set correctly. If any of them are set incorrectly, then
this task will fail.

If this task ever fails, then there’s probably either a bug with the
ttt-build-tool or a problem with your Internet connection.
"""
import importlib
import importlib.util
import pathlib
from typing import Any, Final

from ..common import download
from ..common.config_files import build_config


def perform_task(settings: build_config.BuildConfig) -> None:
    # We don’t really need to use importlib here (we could just use an
    # import statement), but I decided to use it so that we can have a
    # variable that contains the absolute import path of the
    # downloadables module.
    RELATIVE_MODULE_PATH: Final = "...common.download.downloadables"
    ABSOLUTE_MODULE_PATH: Final = importlib.util.resolve_name(
        RELATIVE_MODULE_PATH,
        __name__
    )
    DOWNLOADABLES: Final = importlib.import_module(
        RELATIVE_MODULE_PATH,
        package=__name__
    )

    ATTRIBUTE_NAMES: Final = dir(DOWNLOADABLES)
    attribute_name: str
    for attribute_name in ATTRIBUTE_NAMES:
        attribute: Any = getattr(DOWNLOADABLES, attribute_name)
        if isinstance(attribute, download.Downloadable):
            attribute_path: str = (
                f"{ABSOLUTE_MODULE_PATH}.{attribute_name}"
            )

            print(f"Starting to check {attribute_path}…")
            extracted_path: pathlib.Path = attribute.extracted_path()
            if not extracted_path.exists():
                raise ValueError(
                    f"{attribute_path}.extracted_path() returned this "
                    + f"value: {repr(extracted_path)}. The file or "
                    + "directory that that path refers to should exist,"
                    + " but it doesn’t exist."
                )
            print(f"Finished checking {attribute_path}.")
    print("All checks finished successfully.")
