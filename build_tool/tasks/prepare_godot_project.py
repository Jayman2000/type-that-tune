# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
from .. import common
from . import generate_license_files, prepare_media_files
__doc__ = f"""
Ensures that the Godot project is ready to be imported by the editor.

The {common.GODOT_PROJECT_DIR} directory will eventually get imported by
the Godot Engine editor. When you download Type That Tune’s source code
for the first time, the {common.GODOT_PROJECT_DIR} directory will lack
certain files and directories that the Godot Engine editor needs in
order to successfully import the project. This task will create those
necessary files. This task may skip creating certain files if they
already exist.
"""


def perform_task() -> None:
    generate_license_files.perform_task()
    prepare_media_files.perform_task()
