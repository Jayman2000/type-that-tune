# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Code for running other programs.
"""
import pathlib
import subprocess
import sys
from typing import Final, Union


class NonZeroReturnCodeError(RuntimeError):
    pass


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
        raise NonZeroReturnCodeError(f"This command failed: {command}")
