# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
import re
import subprocess
from typing import Any, Final

from ..common.config_files import build_config


EXPECTED_VERSIONS_FILE: Final = pathlib.Path(
    "python_distribution_packages",
    "ttt-build-tool",
    "ttt_build_tool",
    "common",
    "expected_versions.py"
)
__doc__ = f"""
Updates the expected versions of all dependencies.

Specifically, this task will update {EXPECTED_VERSIONS_FILE}.
"""


def sub_at_least_once(
    regex_pattern: str,
    replacement: Any,
    string: str
)-> str:
    RESULT: Final = re.subn(
        regex_pattern,
        # I’m using a lambda function here because I don’t want the
        # replacement string to be interpreted as potentially having
        # escape characters. See
        # <https://stackoverflow.com/a/16291763/7593853>.
        lambda _: repr(replacement),
        string
    )
    if RESULT[1] <= 0:
        raise ValueError(
            "At least one substitution should have been made. In "
            + f"reality, {RESULT[0]} substitutions were made."
        )
    return RESULT[0]


def perform_task(settings: build_config.BuildConfig) -> None:
    # Determine the new version numbers.
    NEW_GODOT_VERSION_COMMAND: Final = (
        settings.godot_editor_executable_search_list.path_to_use(),
        "--version"
    )
    NEW_GODOT_VERSION_UNPARSED: Final = subprocess.check_output(
        NEW_GODOT_VERSION_COMMAND,
        encoding="locale"
    )
    NEW_GODOT_VERSION_SEGMENTS: Final = (
        NEW_GODOT_VERSION_UNPARSED.split(sep=".")
    )
    NEW_GODOT_VERSION_MAJOR: Final = int(NEW_GODOT_VERSION_SEGMENTS[0])
    NEW_GODOT_VERSION_MINOR: Final = int(NEW_GODOT_VERSION_SEGMENTS[1])
    new_godot_version_patch: int
    new_godot_version_status: str
    try:
        new_godot_version_patch = int(NEW_GODOT_VERSION_SEGMENTS[2])
        new_godot_version_status = NEW_GODOT_VERSION_SEGMENTS[3]
    except ValueError:
        new_godot_version_patch = 0
        new_godot_version_status = NEW_GODOT_VERSION_SEGMENTS[2]

    # Replace the old version numbers with the new ones.
    with EXPECTED_VERSIONS_FILE.open(mode="r", encoding="utf_8") as f:
        module_source_code: str = f.read()
    module_source_code = sub_at_least_once(
        "(?<=GODOT_VERSION_MAJOR: Final = ).*",
        NEW_GODOT_VERSION_MAJOR,
        module_source_code
    )
    module_source_code = sub_at_least_once(
        "(?<=GODOT_VERSION_MINOR: Final = ).*",
        NEW_GODOT_VERSION_MINOR,
        module_source_code
    )
    module_source_code = sub_at_least_once(
        "(?<=GODOT_VERSION_PATCH: Final = ).*",
        new_godot_version_patch,
        module_source_code
    )
    module_source_code = sub_at_least_once(
        "(?<=GODOT_VERSION_STATUS: Final = ).*",
        new_godot_version_status,
        module_source_code
    )
    with EXPECTED_VERSIONS_FILE.open(mode="w", encoding="utf_8") as f:
        f.write(module_source_code)
