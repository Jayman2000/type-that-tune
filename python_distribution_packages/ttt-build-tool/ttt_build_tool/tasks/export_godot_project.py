# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
import shutil
from typing import Final

from .. import common
from ..common.config_files import build_config
from ..common.run_command import run_command
from . import run_task


def perform_task(settings: build_config.BuildConfig) -> None:
    # This makes sure that the exported copy is up to date.
    shutil.rmtree(common.EXPORTED_DIR, ignore_errors=True)
    run_task("prepare_godot_project", settings)

    # editorconfig-checker-disable
    COMMAND: Final = (
        settings.godot_editor_executable_search_list.path_to_use().absolute(),
        "--export-release",
        settings.export_preset,
        settings.exported_project_executable_path().absolute(),
        pathlib.Path(common.GODOT_PROJECT_DIR, "project.godot").absolute()
    )
    # editorconfig-checker-enable
    run_command(COMMAND, cwd=common.GODOT_PROJECT_DIR)
