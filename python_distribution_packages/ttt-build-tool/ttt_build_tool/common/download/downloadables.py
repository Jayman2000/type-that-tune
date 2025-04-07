# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
A bunch of premade Downloadable objects.

All Downloadable objects should be constructed in this file. Putting
them all in this file will make it easier to update them in the future
(for example, when we want to switch to a new version of Godot).
"""
import pathlib
import platform
from typing import Final, Optional

from ..expected_versions import GODOT_VERSION
from . import Downloadable


# The Godot Engine Editor
GODOT_EDITOR_X86_64_LINUX: Final = Downloadable(
    # editorconfig-checker-disable
    f"https://github.com/godotengine/godot/releases/download/{GODOT_VERSION}/Godot_v{GODOT_VERSION}_linux.x86_64.zip",
    # editorconfig-checker-enable
    "84513e316c75bd7897d8b34c2fc2b7eb662f65af2c7401d8298dbc2a450ed652",
    pathlib.Path("Editor.zip"),
    pathlib.Path(f"Godot_v{GODOT_VERSION}_linux.x86_64")
)
GODOT_EDITOR_X86_64_WINDOWS: Final = Downloadable(
    # editorconfig-checker-disable
    f"https://github.com/godotengine/godot/releases/download/{GODOT_VERSION}/Godot_v{GODOT_VERSION}_win64.exe.zip",
    # editorconfig-checker-enable
    "1f5eedae63243aff5a6822d18cc9c8bd909cb8968f97ab80d1653124a1714c9f",
    pathlib.Path("Editor.zip"),
    pathlib.Path(f"Godot_v{GODOT_VERSION}_win64.exe")
)
# Godot Engine export templates
GODOT_EXPORT_TEMPLATES: Final = Downloadable(
    # editorconfig-checker-disable
    f"https://github.com/godotengine/godot/releases/download/{GODOT_VERSION}/Godot_v{GODOT_VERSION}_export_templates.tpz",
    # editorconfig-checker-enable
    "c29f8a9e53b610b8441849936b8a637330c395c17c3cfb52fe8963d44408d985",
    # .tpz files are actually the same thing as .zip files [1]. We’re
    # saving the .tpz file as a .zip file in order to make
    # shutil.unpack_archive do the right thing.
    #
    # editorconfig-checker-disable
    # [1]: <https://docs.godotengine.org/en/4.3/tutorials/export/exporting_projects.html#export-templates>
    # editorconfig-checker-enable
    pathlib.Path("Export templates.zip"),
    pathlib.Path("templates")
)


# Variables that are derived from the previous ones
godot_editor_current_platform: Optional[Downloadable] = None
if platform.machine() == "x86_64":
    if platform.system() == "Linux":
        godot_editor_current_platform = GODOT_EDITOR_X86_64_LINUX
    elif platform.system() == "Windows":
        godot_editor_current_platform = GODOT_EDITOR_X86_64_WINDOWS
GODOT_EDITOR_CURRENT_PLATFORM: Final = godot_editor_current_platform
del godot_editor_current_platform
