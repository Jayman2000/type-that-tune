# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
from typing import Final

from .. import common
from . import prepare_godot_project
__doc__ = f"""
Opens the {common.GODOT_PROJECT_DIR} directory in the Godot Engine
editor.

This task also ensures that the {common.GODOT_PROJECT_DIR} directory is
ready to be imported by the Godot editor before trying to launch the
Godot editor.
"""


def perform_task(settings: common.BuildConfig) -> None:
    prepare_godot_project.perform_task(settings)
    COMMAND: Final = (
        settings.godot_editor_path(),
        "--editor"
    )
    common.run_command(COMMAND, cwd=common.GODOT_PROJECT_DIR)
