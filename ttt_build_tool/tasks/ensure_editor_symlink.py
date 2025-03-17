# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import os
import pathlib
from typing import Final

from .. import common


__doc__ = f"""
Make sure that {common.EDITOR_EXECUTABLE_SYMLINK_PATH} exists.

Some other tasks need to be able to run the Godot Engine editor. Those
tasks expect that {common.EDITOR_EXECUTABLE_SYMLINK_PATH} exists and is
a symlink to a Godot Engine editor executable. This task makes sure that
that symlink exists.

If you run ttt-build-tool with the --godot-editor-path /EXAMPLE_PATH
option, then this task create a symlink to /EXAMPLE_PATH. Otherwise,
this task will build the Godot editor from source and then create a
symlink to the freshly built editor executable.
"""


def locate_editor_executable() -> pathlib.Path:
    for path in common.GODOT_BUILD_BIN_DIR.glob("*"):
        if "editor" in path.name.lower():
            return path
    raise FileNotFoundError(
        "Could not find Godot Engine editor executable."
    )


def perform_task(settings: common.Settings) -> None:
    EDITOR_EXECUTABLE_SYMLINK_PATH: Final = pathlib.Path(
        common.GODOT_ENGINE_DIR,
        "editor.exe" if os.name == "nt" else "editor"
    )
    if settings.godot_editor_path is None:
        common.run_command(
            ("scons",),
            common.GODOT_SRC_DIR
        )
        common.remove_then_symlink(
            locate_editor_executable().absolute(),
            EDITOR_EXECUTABLE_SYMLINK_PATH
        )
    else:
        common.remove_then_symlink(
            settings.godot_editor_path.absolute(),
            EDITOR_EXECUTABLE_SYMLINK_PATH
        )
