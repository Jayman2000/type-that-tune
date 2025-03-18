# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
import shutil
from typing import Final

import reuse.project
import reuse.report

from .. import common


GENERATED_LICENSES_PATH: Final = pathlib.Path(
    common.GENERATED_DIR,
    "licenses"
)
BOM_PATH: Final = pathlib.Path(
    common.GENERATED_DIR,
    "type_that_tune_legal_notices.spdx"
)
__doc__ = f"""
Creates the {GENERATED_LICENSES_PATH} directory and the {BOM_PATH} file.

{GENERATED_LICENSES_PATH} and {BOM_PATH}
are needed for Type That Tune’s Legal Notices screen. Those two files
help make sure that Type That Tune’s legal notices screen contains all
required legal notices (as well as some legal notices that aren’t
required).
"""


def perform_task(settings: common.Settings) -> None:
    common.GENERATED_DIR.mkdir(exist_ok=True, parents=True)
    ORIGINAL_LICENSES_PATH: Final = pathlib.Path("LICENSES")
    if GENERATED_LICENSES_PATH.exists():
        shutil.rmtree(GENERATED_LICENSES_PATH)
    shutil.copytree(ORIGINAL_LICENSES_PATH, GENERATED_LICENSES_PATH)

    PROJECT: Final = reuse.project.Project.from_directory(
        pathlib.Path.cwd()
    )
    REPORT: Final = reuse.report.ProjectReport.generate(PROJECT)
    with BOM_PATH.open(mode="w", encoding="utf-8") as file:
        file.write(REPORT.bill_of_materials())
