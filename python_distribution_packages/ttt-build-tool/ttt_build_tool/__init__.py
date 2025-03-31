# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
import argparse
import collections.abc
import importlib
import pathlib
import pkgutil
from typing import Final

from . import common, tasks


def task_names() -> collections.abc.Iterable[str]:
    SEARCH_PATHS: Final = tasks.__spec__.submodule_search_locations
    for module_info in pkgutil.iter_modules(path=SEARCH_PATHS):
        yield module_info.name


def main() -> int:
    DESCRIPTION: Final =(
        "Transform Type That Tune’s source code into something that can"
        + " be be used with the Godot Engine editor."
    )
    TASK_NAMES: Final = tuple(task_names())
    DEFAULT_TASK: Final = "prepare_godot_project"
    ARGUMENT_PARSER: Final = argparse.ArgumentParser(
        description=DESCRIPTION
    )
    ARGUMENT_PARSER.add_argument(
        "build_config_file_path",
        type=pathlib.Path,
        help=(
            "The build configuration file that you want to use. Build "
            + "configuration files allow you to customize your build of"
            + " Type That Tune. Build configuration files allow you to "
            + "customize your build of Type That Tune. They mainly "
            + "allow you to determine the locations of Type That Tune’s"
            + " dependencies."
        ),
        metavar="BUILD_CONFIG_FILE_PATH",
    )
    ARGUMENT_PARSER.add_argument(
        "task_name",
        nargs="?",
        default=DEFAULT_TASK,
        choices=TASK_NAMES,
        help=(
            "The preparation task that you want the build tool to "
            + f"perform. If not specified, {DEFAULT_TASK} will be used "
            + "by default. Some tasks will automatically run other "
            + "tasks as dependencies. For example, the "
            + "prepare_godot_project task will run the "
            + "generate_license_files because that task needs to be run"
            + " before the Godot project directory is ready to be used."
            + " Here’s a list of all valid tasks: "
            + f"{", ".join(TASK_NAMES)}. You can use the "
            + "--describe-task option to get help on specific tasks."
        ),
        metavar="TASK",
    )
    ARGUMENT_PARSER.add_argument(
        "--describe-task",
        action="store_true",
        help="Print help text about the task instead of running it."
    )
    ARGS: Final = ARGUMENT_PARSER.parse_args()

    MODULE_FOR_CURRENT_TASK: Final = importlib.import_module(
        f".tasks.{ARGS.task_name}",
        package=__name__
    )
    if ARGS.describe_task:
        print(f"{ARGS.task_name}:")
        DOC_STRING: Final = MODULE_FOR_CURRENT_TASK.__doc__
        if DOC_STRING is None:
            print(
                "Unfortunately, this task doesn’t have a description "
                + "yet."
            )
        else:
            print(DOC_STRING)
    else:
        BUILD_CONFIG: Final = common.BuildConfig(
            ARGS.build_config_file_path
        )
        MODULE_FOR_CURRENT_TASK.perform_task(BUILD_CONFIG)

    return 0
