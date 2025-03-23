# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
"""
Common code used by other modules in this package.

Some of the functions that are in this module have a parameter named
toml_value_path. The toml_value_path parameter is used in some error
messages to tell the user which part of the TOML file has a problem. For
example, consider this TOML file:

    [[godot_editor_executable.search_list]]
    path = "/usr/bin/godot"
    type = "use_path_that_exists_at_build_time"

In this example,
• the value path “godot_editor_executable” would refer to a table,
• the value path “godot_editor_executable.search_list” would refer to an
  array,
• the value path “godot_editor_executable.search_list[0]” would refer to
  a table, and
• the value path “godot_editor_executable.search_list[0].path” would
  refer to a string.

Some of the functions do something like this in order to copy their
parameters before using them:

    def do_something(example_dict):
        example_dict = dict(example_dict)

Functions do this so that they are less confusing. If they didn’t do
that, then the function could modify the value of one of the caller’s
variables which could be confusing.
"""
import collections.abc
import pathlib
import subprocess
import sys
import tomllib
import warnings
from typing import Any, Final, NamedTuple, Self, Union


GODOT_PROJECT_DIR: Final = pathlib.Path("godot_project")
GENERATED_DIR: Final = pathlib.Path(GODOT_PROJECT_DIR, "generated")


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


class SearchTupleItem(NamedTuple):
    type: str
    path: pathlib.Path

    @classmethod
    def from_parsed_toml_table(
        cls,
        path_to_build_config_file: pathlib.Path,
        toml_value_path: str,
        parsed_toml_table: dict[Any, Any]
    ) -> Self:
        # Beginning
        parsed_toml_table = dict(parsed_toml_table)
        # TYPE
        try:
            TYPE: Final = parsed_toml_table.pop("type")
        except KeyError as original_exception:
            NEW_EXCEPTION_1: Final = ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. The "
                + f"{toml_value_path} table is supposed to contain a "
                + "key named “type”, but it doesn’t."
            )
            raise NEW_EXCEPTION_1 from original_exception
        if not isinstance(TYPE, str):
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"{toml_value_path}.type is supposed to be a TOML "
                + "string, but it isn’t."
            )
        # PATH
        try:
            PATH: Final = parsed_toml_table.pop("path")
        except KeyError as original_exception:
            NEW_EXCEPTION_2: Final = ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. The "
                + f"{toml_value_path} table is supposed to contain a "
                + "key named “path”, but it doesn’t."
            )
            raise NEW_EXCEPTION_2 from original_exception
        if not isinstance(PATH, str):
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"{toml_value_path}.path is supposed to be a TOML "
                + "string, but it isn’t."
            )
        # End
        if len(parsed_toml_table) != 0:
            UNEXPECTED_KEYS: Final = tuple(parsed_toml_table.keys())
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"Its {toml_value_path} table contains some extra "
                + "keys that ttt-build-tool doesn’t understand. Here’s "
                + "the list of extra TOML keys that weren’t understood:"
                + f" {UNEXPECTED_KEYS}."
            )
        return cls(TYPE, pathlib.Path(PATH))


class GodotEditorSearchTuple(tuple[SearchTupleItem]):
    def __new__(
        cls,
        items: collections.abc.Iterable[SearchTupleItem]
    ) -> Self:
        return super().__new__(cls, items)

    def __repr__(self) -> str:
        return f"{type(self).__name__}({super().__repr__()})"

    @classmethod
    def from_parsed_toml_table(
        cls,
        path_to_build_config_file: pathlib.Path,
        toml_value_path: str,
        parsed_toml_table: dict[Any, Any]
    ) -> Self:
        # Create our own copy of the dict so that we don’t inadvertently
        # modify one of the caller’s variables.
        # Beginning
        parsed_toml_table = dict(parsed_toml_table)
        # SEARCH_LIST
        try:
            SEARCH_LIST: Final = parsed_toml_table.pop("search_list")
        except KeyError as original_exception:
            NEW_EXCEPTION: Final = ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. The "
                + f"{toml_value_path} table is supposed to contain a "
                + "TOML key named “search_list”, but there’s no key "
                + "with that name."
            )
            raise NEW_EXCEPTION from original_exception
        if not isinstance(SEARCH_LIST, list):
            raise TypeError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"{toml_value_path}.search_list is supposed to be a "
                + "TOML array, but it’s not."
            )
        # TO_INCLUDE_IN_RETURN_VALUE
        TO_INCLUDE_IN_RETURN_VALUE: Final[list[SearchTupleItem]] = []
        i: int
        for i in range(len(SEARCH_LIST)):
            search_list_item: Any = SEARCH_LIST[i]
            if not isinstance(search_list_item, dict):
                raise TypeError(
                    "Your build configuration "
                    + f"({path_to_build_config_file}) has a problem. "
                    + f"Each item in {toml_value_path}.search_list is "
                    + " supposed to be a TOML table. "
                    + f"{toml_value_path}.search_list[{i}] is not a "
                    + "TOML table."
                )
            TO_INCLUDE_IN_RETURN_VALUE.append(
                SearchTupleItem.from_parsed_toml_table(
                    path_to_build_config_file,
                    f"{toml_value_path}.search_list[{i}]",
                    search_list_item
                )
            )
        # End
        if len(parsed_toml_table) != 0:
            UNEXPECTED_KEYS: Final = tuple(parsed_toml_table.keys())
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"Its {toml_value_path} table contains some extra "
                + "keys that ttt-build-tool doesn’t understand. Here’s "
                + "the list of extra TOML keys that weren’t understood:"
                + f" {UNEXPECTED_KEYS}."
            )
        return cls(TO_INCLUDE_IN_RETURN_VALUE)

    def locate(self) -> pathlib.Path:
        """
        Finds the first item in self that is usable.

        This function will either return the absolute path of a usable
        Godot editor executable, or it will raise an exception.
        """
        VALID_TYPES: Final = ("use_path_that_exists_at_build_time",)
        item: SearchTupleItem
        path_to_test: pathlib.Path
        for item in self:
            if item.type == VALID_TYPES[0]:
                path_to_test = item.path.absolute()
            else:
                raise ValueError(
                    "One of the items in "
                    + "godot_editor_executable.search_list has an "
                    + f"invalid type: {repr(item.type)}. Its type "
                    + "should have been one of these: "
                    + repr(VALID_TYPES)
                )
            try:
                print(
                    "Testing Godot Editor executable at this path:",
                    path_to_test
                )
                run_command(
                    (path_to_test, "--version"),
                    cwd=pathlib.Path.cwd()
                )
                print("Test succeeded!")
                return path_to_test
            except (NonZeroReturnCodeError, FileNotFoundError):
                print("Test failed.")
                warnings.warn(
                    "One of the items on the build configuration’s "
                    + "godot_editor_executable.search_list is not "
                    + "usable."
                )
        raise ValueError(
            "None of the items on the build configuration’s "
            + "godot_editor_executable.search_list were usable."
        )



class BuildConfig:
    """User preferences available to all tasks."""

    def __init__(self, path_to_build_config_file: pathlib.Path) -> None:
        # Beginning
        with path_to_build_config_file.open(mode='rb') as file:
            try:
                PARSED_TOML_DOCUMENT: Final = tomllib.load(file)
            except tomllib.TOMLDecodeError as ORIGINAL_EXCEPTION:
                NEW_EXCEPTION_1: Final = ValueError(
                    f"We tried to interpret {path_to_build_config_file}"
                    + " as a TOML file, but we failed. Are you sure "
                    + "that that file contains valid TOML?"
                )
                raise NEW_EXCEPTION_1 from ORIGINAL_EXCEPTION
        # godot_editor_search_tuple
        try:
            GODOT_EDITOR_EXECUTABLE_TABLE: Final = (
                PARSED_TOML_DOCUMENT.pop("godot_editor_executable")
            )
        except KeyError as original_exception:
            NEW_EXCEPTION_2: Final = ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. It’s "
                + "supposed to contain a key named "
                + "“godot_editor_executable”, but it doesn’t."
            )
            raise NEW_EXCEPTION_2 from original_exception
        if not isinstance(GODOT_EDITOR_EXECUTABLE_TABLE, dict):
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + "godot_editor_executable is supposed to be a TOML "
                + "table, but it isn’t."
            )
        self.godot_editor_search_tuple: Final = (
            GodotEditorSearchTuple.from_parsed_toml_table(
                path_to_build_config_file,
                "godot_editor_executable",
                GODOT_EDITOR_EXECUTABLE_TABLE
            )
        )
        # End
        if len(PARSED_TOML_DOCUMENT) != 0:
            UNEXPECTED_KEYS: Final = tuple(PARSED_TOML_DOCUMENT.keys())
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) contained some extra "
                + "TOML keys that ttt-build-tool doesn’t understand. "
                + "Here’s the list of extra TOML keys that weren’t "
                + f"understood: {UNEXPECTED_KEYS}."
            )

    def godot_editor_path(self) -> pathlib.Path:
        """
        Returns the absolute path to a usable Godot editor executable or
        raises an exception.

        The first time this method is called, it will will use
        self.godot_editor_search_tuple.locate() in order to determine
        the path to a useable Godot Editor executable, and it will save
        the result for later. All subsequent times this method is
        called, it will return that same saved value. This ensures that
        the same path is returned every time this method is called (at
        least, until the user reruns ttt-build-tool).
        """
        return_value: Any
        try:
            return_value = self._godot_editor_path
        except AttributeError:
            self._godot_editor_path: pathlib.Path = (
                self.godot_editor_search_tuple.locate()
            )
            return_value = self._godot_editor_path
        if not isinstance(return_value, pathlib.Path):
            raise TypeError(
                "self._godot_editor_path’s type should be pathlib.Path,"
                + f"but its type is actually {type(return_value)}."
            )
        return return_value
