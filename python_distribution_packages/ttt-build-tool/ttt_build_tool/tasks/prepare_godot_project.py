# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
from .. import common
from ..common.config_files import build_config
from . import run_task
__doc__ = f"""
Ensures that the Godot project is ready to be imported by the editor.

The {common.GODOT_PROJECT_DIR} directory will eventually get imported by
the Godot Engine editor. When you download Type That Tune’s source code
for the first time, the there will be missing files and directories that
are needed for the {common.GODOT_PROJECT_DIR} directory to work
properly. This task will create those necessary files and directories.
This task may skip creating certain files if they already exist.
"""


def perform_task(settings: build_config.BuildConfig) -> None:
    run_task("ensure_export_templates_symlink", settings)
    run_task("ensure_exported_dir", settings)
    run_task("generate_info_files", settings)
    run_task("generate_license_files", settings)
    run_task("prepare_media_files", settings)
