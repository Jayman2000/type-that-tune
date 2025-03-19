# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
import subprocess
import sys
import tomllib
from typing import Final, NamedTuple, Self, Union


GODOT_PROJECT_DIR: Final = pathlib.Path("godot_project")
GENERATED_DIR: Final = pathlib.Path(GODOT_PROJECT_DIR, "generated")


class BuildConfig(NamedTuple):
    """User preferences available to all tasks."""
    @classmethod
    def from_path(cls, path_to_build_config_file: pathlib.Path) -> Self:
        with path_to_build_config_file.open(mode='rb') as file:
            try:
                PARSED_TOML: Final = tomllib.load(file)
            except tomllib.TOMLDecodeError as ORIGINAL_EXCEPTION:
                NEW_EXCEPTION: Final = ValueError(
                    f"We tried to interpret {path_to_build_config_file}"
                    + " as a TOML file, but we failed. Are you sure "
                    + "that that file contains valid TOML?"
                )
                raise NEW_EXCEPTION from ORIGINAL_EXCEPTION
        if len(PARSED_TOML) != 0:
            UNEXPECTED_KEYS: Final = tuple(PARSED_TOML.keys())
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) contained some extra "
                + "TOML keys that ttt-build-tool doesn’t understand. "
                + "Here’s the list of extra TOML keys that weren’t "
                + f"understood: {UNEXPECTED_KEYS}."
            )
        return cls()


def run_command(
    command: tuple[Union[str, pathlib.Path], ...],
    cwd: pathlib.Path
) -> None:
    RESULT: Final = subprocess.run(
        command,
        cwd=cwd,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    if RESULT.returncode != 0:
        raise RuntimeError(f"This command failed: {command}")
