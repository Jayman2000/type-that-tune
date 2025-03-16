# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
from typing import Final

from .. import common

EXPORTED_PROJECT_DIR: Final = pathlib.Path("exported_godot_project")
__doc__ = """
Makes sure that there’s a place for the Godot Editor to put the Godot
project once it’s exported.
"""


def perform_task(settings: common.Settings) -> None:
    EXPORTED_PROJECT_DIR.mkdir(exist_ok=True)
