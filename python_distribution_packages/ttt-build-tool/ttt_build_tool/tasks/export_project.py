# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Turns the Godot project into a standalone runnable application.

You must use the --godot-export-preset command-line option when running
this task.
"""
import os
import pathlib
import shutil
from typing import Final

from .. import common
from . import ensure_editor_symlink, prepare_godot_project


def perform_task(settings: common.Settings) -> None:
    if settings.godot_export_preset is None:
        raise ValueError(
            "--godot-export-preset was not specified. It must be "
            + "specified whenever the export_project task is used."
        )
    else:
        ensure_editor_symlink.perform_task(settings)
        prepare_godot_project.perform_task(settings)
        for path in common.EXPORTED_PROJECT_DIR.glob("*"):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        EXPORTED_EXECUTABLE: Final = pathlib.Path(
            common.EXPORTED_PROJECT_DIR,
            f"type-that-tune{".exe" if os.name == "nt" else ""}"
        )
        COMMAND: Final = (
            common.EDITOR_EXECUTABLE_SYMLINK_PATH.absolute(),
            "--export-release",
            settings.godot_export_preset,
            EXPORTED_EXECUTABLE.absolute(),
            pathlib.Path(common.GODOT_PROJECT_DIR, "project.godot")
        )
        common.run_command(COMMAND, common.GODOT_PROJECT_DIR)
