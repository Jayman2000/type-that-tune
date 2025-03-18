# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Makes sure that the Godot Editor has the export templates that it needs
in order to export this project.
"""
import pathlib
import shutil
from typing import Final

from .. import common


EXPORT_TEMPLATES_DIR: Final = pathlib.Path(
    common.GODOT_ENGINE_DIR,
    "export_templates"
)


def perform_task(settings: common.Settings) -> None:
    if (
        EXPORT_TEMPLATES_DIR.is_symlink()
        or EXPORT_TEMPLATES_DIR.is_file()
    ):
        EXPORT_TEMPLATES_DIR.unlink(missing_ok=True)
    elif EXPORT_TEMPLATES_DIR.is_dir():
        shutil.rmtree(EXPORT_TEMPLATES_DIR)

    if settings.godot_export_templates_path is None:
        common.run_command(
            ("scons", "target=template_release", "production=yes"),
            common.GODOT_SRC_DIR
        )
        EXPORT_TEMPLATES_DIR.mkdir()
        for path in common.GODOT_BUILD_BIN_DIR.glob("*"):
            if path.name == "godot.linuxbsd.template_release.x86_64":
                pathlib.Path(
                    EXPORT_TEMPLATES_DIR,
                    "linux_release.x86_64"
                ).symlink_to(path.absolute())
            # TODO: Every time we add a new preset to
            # export_presets.cfg, we need to add an elif here.
    else:
        common.remove_then_symlink(
            settings.godot_export_templates_path.absolute(),
            EXPORT_TEMPLATES_DIR
        )
