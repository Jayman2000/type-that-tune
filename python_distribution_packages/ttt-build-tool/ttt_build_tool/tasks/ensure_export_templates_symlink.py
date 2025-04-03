# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
from typing import Final

from ..common import build_config


GODOT_EXPORT_TEMPLATES_SYMLINK: Final = (
    pathlib.Path("godot_export_templates")
)
__doc__ = f"""
Ensures that {GODOT_EXPORT_TEMPLATES_SYMLINK} exists.

In order Type That Tune’s export export templates won’t work properly
unless {GODOT_EXPORT_TEMPLATES_SYMLINK} exists. This task creates makes
sure that {GODOT_EXPORT_TEMPLATES_SYMLINK} is symlinked to a directory
that contains the export templates.
"""


def perform_task(settings: build_config.BuildConfig) -> None:
    GODOT_EXPORT_TEMPLATES_SYMLINK.unlink(missing_ok=True)
    GODOT_EXPORT_TEMPLATES_SYMLINK.symlink_to(
        settings.godot_export_templates_tuple.locate()
    )
