# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
from typing import Final

from .. import common


EXPORTED_DIR: Final = pathlib.Path("exported_godot_project")
__doc__ = f"""
Ensures that {EXPORTED_DIR} exists.

This directory is used by Type That Tune’s export presets. If this
directory doesn’t exist, then attempting to export Type That Tune the
Godot Engine editor won’t be able to export the project correctly.
"""


def perform_task(settings: common.BuildConfig) -> None:
    EXPORTED_DIR.mkdir(exist_ok=True)
