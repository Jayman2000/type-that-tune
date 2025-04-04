# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
"""
Code for reading and parsing build configuration files.

Some of the functions that are in this module and its submodules have a
parameter named toml_value_path. The toml_value_path parameter is used
in some error messages to tell the user which part of the TOML file has
a problem. For example, consider this TOML file:

    [[godot_editor_executable_search_list]]
    path = "/usr/bin/godot"
    type = "use_path_that_exists_at_build_time"

In this example,
• the value path “godot_editor_executable_search_list” would refer to an
array,
• the value path “godot_editor_executable_search_list[0]” would refer to
a table, and
• the value path “godot_editor_executable_search_list[0].path” would
refer to the string "/usr/bin/godot".
"""
import pathlib
from typing import Any, Final, Optional


def build_config_error_message(build_config_path: pathlib.Path) -> str:
    return (
        f"Your build configuration ({build_config_path}) has a problem."
    )


# This part comes from the tomllib conversion table [1]. There’s other
# items in that table, but we don’t actually use any of those other
# items, so I’m ignoring them. We can always add them later if they’re
# needed.
#
# editorconfig-checker-disable
# [1]: <https://docs.python.org/3/library/tomllib.html#conversion-table>.
# editorconfig-checker-enable
type TOMLConversionResult = dict[str, Any] | list[Any] | str


def assert_correct_type[T: TOMLConversionResult](
    build_config_path: pathlib.Path,
    toml_value_path: str,
    parsed_toml: Any,
    expected_python_type: type[T]
) -> T:
    if isinstance(parsed_toml, expected_python_type):
        return parsed_toml
    else:
        PYTHON_TYPE_TO_TOML_TYPE: Final[dict[type[Any], str]] = {
            dict: "table",
            list: "array",
            str: "string"
        }
        raise ValueError(
            build_config_error_message(build_config_path)
            + " {toml_value_path} is supposed to be a TOML "
            + f"{PYTHON_TYPE_TO_TOML_TYPE[expected_python_type]}, but "
            + "it was a different data type."
        )


def pop_and_assert_none_or_correct_type[T: TOMLConversionResult](
    build_config_path: pathlib.Path,
    toml_value_path: str,
    parsed_toml: dict[str, Any],
    expected_key: str,
    expected_python_type: type[T],
) -> Optional[T]:
    try:
        RETURN_VALUE: Final = parsed_toml.pop(expected_key)
    except KeyError:
        return None
    return assert_correct_type(
        build_config_path,
        f"{toml_value_path}.{expected_key}",
        RETURN_VALUE,
        expected_python_type
    )


def pop_and_assert_correct_type[T: TOMLConversionResult](
    build_config_path: pathlib.Path,
    toml_value_path: str,
    parsed_toml: dict[str, Any],
    expected_key: str,
    expected_python_type: type[T],
) -> T:
    RETURN_VALUE: Final = pop_and_assert_none_or_correct_type(
        build_config_path,
        toml_value_path,
        parsed_toml,
        expected_key,
        expected_python_type
    )
    if RETURN_VALUE is None:
        raise ValueError(
            build_config_error_message(build_config_path)
            + f" {toml_value_path} is supposed to contain a TOML key "
            + f"named “{expected_key}”, but it doesn’t."
        )
    else:
        return RETURN_VALUE
