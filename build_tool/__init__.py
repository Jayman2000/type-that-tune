# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
from . import generate_license_files, prepare_media_files


def main() -> int:
    generate_license_files.perform_task()
    prepare_media_files.perform_task()

    return 0
