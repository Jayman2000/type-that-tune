# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
import pathlib
import shutil
from typing import Final

import reuse._main
import reuse.project
import reuse.spdx
import reuse.vcs


def main() -> int:
    GENERATED_DIR: Final = pathlib.Path("project", "generated")
    GENERATED_DIR.mkdir(exist_ok=True)

    ORIGINAL_LICENSES_PATH: Final = pathlib.Path("LICENSES")
    GENERATED_LICENSES_PATH: Final = pathlib.Path(
        GENERATED_DIR,
        "licenses"
    )
    if GENERATED_LICENSES_PATH.exists():
        shutil.rmtree(GENERATED_LICENSES_PATH)
    shutil.copytree(ORIGINAL_LICENSES_PATH, GENERATED_LICENSES_PATH)

    BOM_PATH: Final = pathlib.Path(
        GENERATED_DIR,
        "type_that_tune_legal_notices.spdx"
    )
    # I wish that calling reuse.spdx.run() didn’t require that I create
    # an ArgumentParser, but it does.
    REUSE_ARGUMENT_PARSER: Final = reuse._main.parser()
    reuse.spdx.add_arguments(REUSE_ARGUMENT_PARSER)
    REUSE_PROJECT: Final = reuse.project.Project(
        pathlib.Path.cwd(),
        vcs_strategy=reuse.vcs.VCSStrategyGit
    )
    with BOM_PATH.open(mode="w", encoding="utf-8") as bom_file:
        return reuse.spdx.run(
            REUSE_ARGUMENT_PARSER.parse_args(args=tuple()),
            REUSE_PROJECT,
            out=bom_file
        )
