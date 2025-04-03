# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
"""
Common code used by other modules in this package.
"""
import pathlib
from typing import Final

import appdirs


GODOT_PROJECT_DIR: Final = pathlib.Path("godot_project")
GENERATED_DIR: Final = pathlib.Path(GODOT_PROJECT_DIR, "generated")
EXPORTED_DIR: Final = pathlib.Path("exported_godot_project")
CACHE_DIRECTORY: Final = pathlib.Path(appdirs.user_cache_dir(
    appname="ttt-build-tool",
    appauthor="Type That Tune contributors"
))
DOWNLOADS_DIR: Final = pathlib.Path(CACHE_DIRECTORY, "downloads")
