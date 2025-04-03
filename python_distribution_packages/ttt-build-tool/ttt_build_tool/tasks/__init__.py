# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import importlib
import pkgutil
from types import ModuleType
from typing import Final, Optional

from ..common import build_config


TASK_NAMES: Final = tuple(
    module_info.name
    for
    module_info
    in
    pkgutil.iter_modules(path=__spec__.submodule_search_locations)
)
already_imported_tasks: dict[str, ModuleType] = {}
task_stack: list[str] = []


def task_module(task_name: str) -> ModuleType:
    try:
        return already_imported_tasks[task_name]
    except KeyError:
        already_imported_tasks[task_name] = importlib.import_module(
            f".{task_name}",
            package=__name__
        )
        return already_imported_tasks[task_name]


def task_description(task_name: str) -> Optional[str]:
    return task_module(task_name).__doc__


def run_task(
    task_name: str,
    settings: build_config.BuildConfig
) -> None:
    if len(task_stack) == 0:
        print(f"Starting the {task_name} task…")
    else:
        print(
            f"Starting the {task_name} task as a dependency of the "
            + f"{task_stack[-1]} task…"
        )
    task_stack.append(task_name)
    task_module(task_name).perform_task(settings)
    print(f"Finished the {task_name} task.")
    task_stack.pop()
