# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
The expected version numbers of Type That Tune’s dependencies.

The ttt-build-tool and Type That Tune itself may give warnings if the
actual version numbers of its dependencies don’t match the version
numbers listed here. The version numbers listed here are also used to
determine the versions of anything that the ttt-build-tool will try to
download.

For the most part, this file should be updated by running the
update_expected_versions task. If you ever manually update this file,
then you should run updated_expected_versions in order to make sure that
it still works properly.
"""
from typing import Final


# TODO: There needs to be a way to keep this in sync with
# godot_project/scenes_and_scripts/autoload/startup_checker.gd.
GODOT_VERSION_MAJOR: Final = 4
GODOT_VERSION_MINOR: Final = 3
GODOT_VERSION_PATCH: Final = 0
GODOT_VERSION_STATUS: Final = 'stable'

GODOT_VERSION: Final = (
    f"{GODOT_VERSION_MAJOR}.{GODOT_VERSION_MINOR}"
    + ("" if GODOT_VERSION_PATCH == 0 else f".{GODOT_VERSION_PATCH}")
    + f"-{GODOT_VERSION_STATUS}"
)

PYTHON_VERSION: Final = '3.12.8'
