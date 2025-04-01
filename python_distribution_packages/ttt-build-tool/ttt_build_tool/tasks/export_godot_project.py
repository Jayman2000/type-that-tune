# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import shutil
from typing import Final

from .. import common
from . import run_task


def perform_task(settings: common.BuildConfig) -> None:
    # This makes sure that the exported copy is up to date.
    shutil.rmtree(common.EXPORTED_DIR, ignore_errors=True)

    run_task("prepare_godot_project", settings)
    COMMAND: Final = (
        settings.godot_editor_path(),
        "--export-release",
        settings.export_preset,
        settings.exported_project_executable_path(),
        common.EXPORTED_DIR
    )
    common.run_command(COMMAND, cwd=common.GODOT_PROJECT_DIR)
