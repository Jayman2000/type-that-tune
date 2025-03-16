# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
from typing import Final, NamedTuple, Optional


GODOT_PROJECT_DIR: Final = pathlib.Path("godot_project")
GENERATED_DIR: Final = pathlib.Path(GODOT_PROJECT_DIR, "generated")


class Settings(NamedTuple):
    """User preferences available to all tasks."""
    godot_editor_path: Optional[pathlib.Path]
