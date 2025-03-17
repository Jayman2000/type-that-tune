# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import json
import pathlib
import shutil
from typing import Final

from .. import common


def perform_task(settings: common.Settings) -> None:
    EXTERNAL_TOOL_INFO_DIR: Final = pathlib.Path(
        common.GENERATED_DIR,
        "external_tool_info"
    )
    if EXTERNAL_TOOL_INFO_DIR.exists():
        shutil.rmtree(EXTERNAL_TOOL_INFO_DIR)
    EXTERNAL_TOOL_INFO_DIR.mkdir()

    ttt_runtime_info_json: str
    if settings.ttt_runtime_tool_path is None:
        ttt_runtime_info_json = json.dumps({"find_on_path": True})
    else:
        ttt_runtime_info_json = json.dumps({
            "find_on_path": True,
            "location": settings.ttt_runtime_tool_path
        })
    TTT_RUNTIME_INFO_PATH: Final = pathlib.Path(
        EXTERNAL_TOOL_INFO_DIR,
        "ttt_build_tool.json"
    )
    with TTT_RUNTIME_INFO_PATH.open(mode="w", encoding="utf_8") as file:
        file.write(ttt_runtime_info_json)
