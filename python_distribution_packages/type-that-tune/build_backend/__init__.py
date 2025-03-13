# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import os
import pathlib
import subprocess
from typing import Final, Union


def git_find_files(path: Union[os.PathLike[str], str]) -> list[str]:
    # We don’t know what datatype path is going to be, so we make sure
    # that it’s the type that we want.
    ROOT: Final = pathlib.Path(path)
    if pathlib.Path(ROOT, ".git").exists():
        COMMAND: Final = (
            "git",
            "ls-files",
            "--recurse-submodules",
            "-z"
        )
        RESULT: Final = subprocess.run(
            COMMAND,
            cwd=ROOT,
            capture_output=True,
            text=True
        )
        if RESULT.returncode != 0:
            raise RuntimeError(
                f"The command {COMMAND}. Its exit status was "
                + f"{RESULT.returncode}."
            )
        return RESULT.stdout.split(sep="\0")
    else:
        return [str(subpath) for subpath in ROOT.glob("**")]
