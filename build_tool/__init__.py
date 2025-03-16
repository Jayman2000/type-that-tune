# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
from . import prepare_godot_project


def main() -> int:
    prepare_godot_project.perform_task()

    return 0
