# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
from typing import Final

from .. import common
from ..common import expected_versions
from ..common.config_files import build_config


INFO_DIR_PATH: Final = pathlib.Path(
    common.GENERATED_DIR,
    "info_from_build_tool"
)
__doc__ = f"""
Creates or recreates the {INFO_DIR_PATH} directory.

The {INFO_DIR_PATH} directory is used to take information that is known
by the ttt-build-tool at build time and give it to the Godot project so
that the Godot project can know that information at runtime.

Originally, I had thought to make a single JSON file that contains all
of the information, but I decided to split up the information into
multiple plain text files instead. Doing so made it easier to write the
GDScript code that parses the information. When I tried writing GDScript
code that would parse JSON, I had to write if statements that would
check to see if values were the correct type. Splitting the data up into
multiple different files makes it so that I don’t have to do that.
"""


def perform_task(settings: build_config.BuildConfig) -> None:
    INFO_DIR_PATH.mkdir(parents=True, exist_ok=True)
    EXPECTED_GODOT_VERSION_PATH: Final = pathlib.Path(
        INFO_DIR_PATH,
        "expected_godot_version.txt"
    )
    EXPECTED_GODOT_VERSION_FILE: Final = (
        EXPECTED_GODOT_VERSION_PATH.open(mode="w", encoding="utf_8")
    )
    with EXPECTED_GODOT_VERSION_FILE as file:
        file.write(
            # This version number always uses three digits, even if the
            # upstream version number only uses two. For example,
            # godotengine.org might mention Godot version 4.3. Here, we
            # wouldn’t call it version 4.3. Instead, we would call it
            # version 4.3.0.
            str(expected_versions.GODOT_VERSION_MAJOR)
            + "."
            + str(expected_versions.GODOT_VERSION_MINOR)
            + "."
            + str(expected_versions.GODOT_VERSION_PATCH)
            + "-"
            + str(expected_versions.GODOT_VERSION_STATUS)
        )
