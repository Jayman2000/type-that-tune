# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
from .. import common
from . import (
    generate_license_files,
    prepare_media_files,
    ensure_exported_dir,
    ensure_export_templates
)
__doc__ = f"""
Ensures that the Godot project is ready to be imported by the editor.

The {common.GODOT_PROJECT_DIR} directory will eventually get imported by
the Godot Engine editor. When you download Type That Tune’s source code
for the first time, the there will be missing files and directories that
are needed for the {common.GODOT_PROJECT_DIR} directory to work
properly. This task will create those necessary files and directories.
This task may skip creating certain files if they already exist.
"""


def perform_task(settings: common.Settings) -> None:
    generate_license_files.perform_task(settings)
    prepare_media_files.perform_task(settings)
    ensure_exported_dir.perform_task(settings)
    ensure_export_templates.perform_task(settings)
