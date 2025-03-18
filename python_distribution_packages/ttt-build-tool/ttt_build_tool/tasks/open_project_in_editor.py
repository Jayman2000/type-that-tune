# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Prepares the Godot Engine editor and the Godot project directory, then
opens the Godot project in the editor.
"""
import pathlib
from typing import Final

from .. import common
from . import ensure_editor_symlink, prepare_godot_project


def perform_task(settings: common.Settings) -> None:
    ensure_editor_symlink.perform_task(settings)
    prepare_godot_project.perform_task(settings)
    COMMAND: Final = (
        common.EDITOR_EXECUTABLE_SYMLINK_PATH,
        "--editor",
        pathlib.Path(common.GODOT_PROJECT_DIR, "project.godot")
    )
    common.run_command(COMMAND, pathlib.Path.cwd())
