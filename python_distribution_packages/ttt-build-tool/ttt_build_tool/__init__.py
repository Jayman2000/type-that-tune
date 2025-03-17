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
    EXPORT_PRESETS_PATH: Final = pathlib.Path(
        common.GODOT_PROJECT_DIR,
        "export_presets.cfg"
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
    ARGUMENT_PARSER.add_argument(
        "--godot-editor-path",
        help=(
            "Some tasks require a copy of the Godot Engine editor in "
            + "order to run. By default, ttt-build-tool will try to "
            + "build and use its own copy of the Godot Engine editor. "
            + "You can use the --godot-editor-absolute-path option to "
            + "tell ttt-build-tool to use an existing copy of the Godot"
            + "Engine editor instead of building its own."
        ),
        type=pathlib.Path,
        metavar="PATH"
    )
    ARGUMENT_PARSER.add_argument(
        "--godot-export-templates-path",
        help=(
            "Some tasks require Godot Engine export templates in order "
            + "to run. By default, ttt-build-tool wil try to build and "
            + "use its own export templates from source. You can use "
            + "the --godot-export-templates-path option to tell "
            + "ttt-build-tool to use an existing set of export "
            + "templates instead of building its own from source."
        ),
        type=pathlib.Path,
        metavar="PATH"
    )
    ARGUMENT_PARSER.add_argument(
        "--godot-export-preset",
        help=(
            "Some tasks will try to export the Type That Tune Godot "
            + "project. Godot projects can have multiple different "
            + "export templates, and the ttt-build-tool needs to know "
            + "which one you want to use. A list of valid preset names "
            + f"can be found in {EXPORT_PRESETS_PATH}."
        ),
        type=str,
        metavar="NAME"
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
        SETTINGS: Final = common.Settings(
            godot_editor_path=ARGS.godot_editor_path,
            godot_export_templates_path=ARGS.godot_export_templates_path,
            godot_export_preset=ARGS.godot_export_preset
        )
        MODULE_FOR_CURRENT_TASK.perform_task(SETTINGS)

    return 0
