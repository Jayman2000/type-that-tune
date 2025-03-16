# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
import shutil
from typing import Final

import reuse.project
import reuse.report

from . import common


def perform_task() -> None:
    ORIGINAL_LICENSES_PATH: Final = pathlib.Path("LICENSES")
    GENERATED_LICENSES_PATH: Final = pathlib.Path(
        common.GENERATED_DIR,
        "licenses"
    )
    if GENERATED_LICENSES_PATH.exists():
        shutil.rmtree(GENERATED_LICENSES_PATH)
    shutil.copytree(ORIGINAL_LICENSES_PATH, GENERATED_LICENSES_PATH)

    BOM_PATH: Final = pathlib.Path(
        common.GENERATED_DIR,
        "type_that_tune_legal_notices.spdx"
    )
    PROJECT: Final = reuse.project.Project.from_directory(
        pathlib.Path.cwd()
    )
    REPORT: Final = reuse.report.ProjectReport.generate(PROJECT)
    with BOM_PATH.open(mode="w", encoding="utf-8") as file:
        file.write(REPORT.bill_of_materials())
