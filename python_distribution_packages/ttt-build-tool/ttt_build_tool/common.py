# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
import os
import pathlib
import subprocess
import sys
from typing import Final, NamedTuple, Optional, Union


GODOT_PROJECT_DIR: Final = pathlib.Path("godot_project")
GENERATED_DIR: Final = pathlib.Path(GODOT_PROJECT_DIR, "generated")
GODOT_ENGINE_DIR: Final = pathlib.Path("godot_engine")
GODOT_SRC_DIR: Final = pathlib.Path(GODOT_ENGINE_DIR, "src")
GODOT_BUILD_BIN_DIR: Final = pathlib.Path(
    GODOT_SRC_DIR,
    "bin"
)
EDITOR_EXECUTABLE_SYMLINK_PATH: Final = pathlib.Path(
    GODOT_ENGINE_DIR,
    "editor.exe" if os.name == "nt" else "editor"
)


class Settings(NamedTuple):
    """User preferences available to all tasks."""
    godot_editor_path: Optional[pathlib.Path]
    ttt_runtime_tool_path: Optional[pathlib.Path]


def run_command(
    command: tuple[Union[str, pathlib.Path], ...],
    cwd: pathlib.Path
) -> None:
    RESULT: Final = subprocess.run(
        command,
        cwd=cwd,
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    if RESULT.returncode != 0:
        raise RuntimeError(f"This command failed: {command}")


def remove_then_symlink(
    target: pathlib.Path,
    symlink_path: pathlib.Path
) -> None:
    symlink_path.unlink(missing_ok=True)
    symlink_path.symlink_to(target)
