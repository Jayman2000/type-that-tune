# -*- coding: utf-8 -*-
# mypy: ignore-errors
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import ttt_build_tool
import setuptools.build_meta as original_build_meta
from setuptools.build_meta import *  # noqa: F403


def build_wheel(*args, **kwargs) -> str:
    exit_status = ttt_build_tool.main()
    if exit_status != 0:
        raise RuntimeError(
            f"ttt-build failed. Its exit status was {exit_status}."
        )
    return original_build_meta.build_wheel(*args, **kwargs)
