# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import pathlib
import shutil
import warnings
from typing import Any, Final, Optional

from .. import common
from ..common import expected_versions
from ..common.config_files import build_config, search_item


INFO_DIR_PATH: Final = pathlib.Path(
    common.GENERATED_DIR,
    "info_from_build_tool"
)
__doc__ = f"""
Creates or recreates the {INFO_DIR_PATH} directory.

The {INFO_DIR_PATH} directory is used to take information that is known
by the ttt-build-tool at build time and give it to the Godot project so
that the Godot project can know that information at runtime.

Originally, I had thought to make a single JSON file that contains all
of the information, but I decided to split up the information into
multiple plain text files instead. Doing so made it easier to write the
GDScript code that parses the information. When I tried writing GDScript
code that would parse JSON, I had to write if statements that would
check to see if values were the correct type. Splitting the data up into
multiple different files makes it so that I don’t have to do that.
"""


def potentially_create_file_for_attribute(
    dir_path: pathlib.Path,
    object: Any,
    attribute_name: str
) -> Any:
    """Stores an attribute in a file if the attribute is not None."""
    ATTRIBUTE_VALUE: Final = getattr(object, attribute_name)
    if ATTRIBUTE_VALUE is not None:
        FILE_PATH: Final = pathlib.Path(
            dir_path,
            f"{attribute_name}.txt"
        )
        with FILE_PATH.open(mode="w", encoding="utf_8") as file:
            file.write(str(ATTRIBUTE_VALUE))
    return ATTRIBUTE_VALUE


def perform_task(settings: build_config.BuildConfig) -> None:
    INFO_DIR_PATH.mkdir(parents=True, exist_ok=True)
    # Expected Godot version
    EXPECTED_GODOT_VERSION_PATH: Final = pathlib.Path(
        INFO_DIR_PATH,
        "expected_godot_version.txt"
    )
    EXPECTED_GODOT_VERSION_FILE: Final = (
        EXPECTED_GODOT_VERSION_PATH.open(mode="w", encoding="utf_8")
    )
    with EXPECTED_GODOT_VERSION_FILE as file:
        file.write(
            # This version number always uses three digits, even if the
            # upstream version number only uses two. For example,
            # godotengine.org might mention Godot version 4.3. Here, we
            # wouldn’t call it version 4.3. Instead, we would call it
            # version 4.3.0.
            str(expected_versions.GODOT_VERSION_MAJOR)
            + "."
            + str(expected_versions.GODOT_VERSION_MINOR)
            + "."
            + str(expected_versions.GODOT_VERSION_PATCH)
            + "-"
            + str(expected_versions.GODOT_VERSION_STATUS)
        )
    # Python interpreter search list
    PYTHON_INTERPRETER_SEARCH_LIST_DIR_PATH: Final = pathlib.Path(
        INFO_DIR_PATH,
        "python_interpreter_search_list"
    )
    shutil.rmtree(
        PYTHON_INTERPRETER_SEARCH_LIST_DIR_PATH,
        ignore_errors=True
    )
    if settings.python_interpreter_search_list is not None:
        PYTHON_INTERPRETER_SEARCH_LIST_DIR_PATH.mkdir(parents=True)
        i: int
        for i in range(len(settings.python_interpreter_search_list)):
            current_item: search_item.PythonInterpreterSearchItem = (
                settings.python_interpreter_search_list[i]
            )
            current_item_dir_path: pathlib.Path = pathlib.Path(
                PYTHON_INTERPRETER_SEARCH_LIST_DIR_PATH,
                str(i)
            )
            current_item_dir_path.mkdir()
            current_type: Any = potentially_create_file_for_attribute(
                current_item_dir_path,
                current_item,
                "type"
            )
            potentially_create_file_for_attribute(
                current_item_dir_path,
                current_item,
                "command_name"
            )
            potentially_create_file_for_attribute(
                current_item_dir_path,
                current_item,
                "path"
            )

            # editorconfig-checker-disable
            if current_type == search_item.SearchItemType.download_at_build_time:
                # editorconfig-checker-enable
                path_to_copy: Optional[pathlib.Path] = (
                    current_item.locate_and_test()
                )
                if path_to_copy is None:
                    warnings.warn(
                        "Your build configuration "
                        + f"({current_item.build_config_path}) might "
                        + "have a problem. "
                        + f"{current_item.toml_value_path} is not "
                        + "usable. "
                    )
                else:
                    destination: pathlib.Path = pathlib.Path(
                        current_item_dir_path,
                        "download"
                    )
                    shutil.copytree(path_to_copy, destination)
                    # Prevent audio files from being imported.
                    pathlib.Path(destination, ".gdignore").touch()
