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

The bodies of all of the abstract methods in this module raise a
NotImplementedError. Rasing an exception helps avoid this problem:
<https://stackoverflow.com/q/51818797/7593853>.
"""
import abc
import collections.abc
import hashlib
import pathlib
import shutil
import subprocess
import sys
import tomllib
import warnings
from typing import Any, Final, NamedTuple, Optional, Self, Union

import appdirs
import requests
import requests_cache


GODOT_PROJECT_DIR: Final = pathlib.Path("godot_project")
GENERATED_DIR: Final = pathlib.Path(GODOT_PROJECT_DIR, "generated")
SEARCH_TUPLE_ITEM_VALID_TYPES: Final = (
    "use_path_that_exists_at_build_time",
    "locate_using_path_env_var_at_build_time",
    "download_at_build_time"
)
CACHE_DIRECTORY: Final = pathlib.Path(appdirs.user_cache_dir(
    appname="ttt-build-tool",
    appauthor="Type That Tune contributors"
))
DOWNLOADS_DIR: Final = pathlib.Path(CACHE_DIRECTORY, "downloads")
REQUESTS_CACHE_CACHE_DIR: Final = (
    pathlib.Path(CACHE_DIRECTORY, "requests_cache")
)
REQUESTS_CACHE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
REQUESTS_SESSION: Final = requests_cache.CachedSession(
    REQUESTS_CACHE_CACHE_DIR,
    backend="filesystem",
    cache_control=True,
    # This is a workaround for this bug:
    # <https://github.com/requests-cache/requests-cache/issues/1078>
    serializer="yaml"
)


def dir_to_put_download_in(url: str) -> pathlib.Path:
    """
    Determines where inside DOWNLOADS_DIR a file should be saved.

    Even if the ttt-build-tool is run multiple times, it should only
    ever download files once. The ttt-build-tool stores its downloads in
    subdirectories of the DOWNLOADS_DIR directory so that they can be
    reused when the ttt-build-tool is run again.
    """
    URL_HASH: Final = hashlib.sha3_256(url.encode("utf-8")).hexdigest()
    return pathlib.Path(DOWNLOADS_DIR, URL_HASH)


def download_if_needed(
    url: str,
    relative_path: pathlib.Path,
    expected_hash: str
) -> pathlib.Path:
    """
    Download a regular file from url if necessary.

    This function will download a regular file. It can’t be used to
    download a video from sites like Niconico.

    This function caches its output. It won’t try to redownload
    something if it was already downloaded during a previous run of the
    ttt-build-tool.

    Parameters:
    url — The Web address of the file that you want to download.

    expected_hash — The SHA3-256 hash of the file that we’re going to
    download. After the file is downloaded, its hash will be calculated
    and compared to expected_hash. If they don’t match, then an
    exception will be raised. This helps ensure that the code in this
    repo is reproducible. expected_hash should be set to a string of
    hexadecimal digits.

    relative_path — Where to save the file, relative to
    dir_to_put_download_in(url).

    Return value: The path to the downloaded file.

    Raises a requests.RequestException if the file fails to download.
    """
    DESTINATION: Final = pathlib.Path(
        dir_to_put_download_in(url),
        relative_path
    )
    if DESTINATION.exists():
        with DESTINATION.open(mode="rb") as file:
            ACTUAL_HASH_1: Final = (
                hashlib.sha3_256(file.read()).hexdigest()
            )
        if ACTUAL_HASH_1 != expected_hash:
            raise ValueError(
                f"A file was downloaded from {repr(url)} and saved to "
                + f"{DESTINATION}. ttt-build-tool expected that its "
                + f"SHA3-256 hash would be {repr(expected_hash)}, but "
                + "its hash was actually {repr(ACTUAL_HASH_1)}."
            )
    else:
        RESPONSE: Final = REQUESTS_SESSION.get(url)
        RESPONSE.raise_for_status()
        ACTUAL_HASH_2: Final = (
            hashlib.sha3_256(RESPONSE.content).hexdigest()
        )
        if ACTUAL_HASH_2 != expected_hash:
            raise ValueError(
                f"A file was downloaded from {repr(url)}. "
                + "ttt-build-tool expected that its SHA3-256 hash would"
                + f" be {repr(expected_hash)}, but its hash was "
                + f"actually {repr(ACTUAL_HASH_2)}."
            )
        DESTINATION.parent.mkdir(parents=True, exist_ok=True)
        with DESTINATION.open(mode="wb") as file:
            file.write(RESPONSE.content)
    return DESTINATION


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
    path: Optional[pathlib.Path]
    command_name: Optional[str]

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
        PATH: Final = parsed_toml_table.pop("path", None)
        if PATH is not None and not isinstance(PATH, str):
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"{toml_value_path}.path is supposed to be a TOML "
                + "string, but it isn’t."
            )
        # COMMAND_NAME
        COMMAND_NAME: Final = parsed_toml_table.pop(
            "command_name",
            None
        )
        if (
            COMMAND_NAME is not None
            and not isinstance(COMMAND_NAME, str)
        ):
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"{toml_value_path}.command_name is supposed to be a"
                + " TOML string, but it isn’t."
            )
        # End
        if TYPE == SEARCH_TUPLE_ITEM_VALID_TYPES[0]:
            if PATH is None:
                raise ValueError(
                    "Your build configuration "
                    + f"({path_to_build_config_file}) has a problem. "
                    + f"{toml_value_path}.type is set to {TYPE}, but "
                    + f"there was no {toml_value_path}.path "
                    + f"TOML key. When {toml_value_path}.type is set to"
                    + " {TYPE}, you need to set "
                    + f"{toml_value_path}.path to a TOML string."
                )
            if COMMAND_NAME is not None:
                raise ValueError(
                    "Your build configuration "
                    + f"({path_to_build_config_file}) has a problem. "
                    + f"{toml_value_path}.type is set to {TYPE}, and "
                    + f"{toml_value_path}.command_name is set to "
                    + f"{COMMAND_NAME}. When {toml_value_path}.type is "
                    + f"set to {TYPE}, {toml_value_path}.command_name "
                    + "shouldn’t be used at all."
                )
        elif TYPE == SEARCH_TUPLE_ITEM_VALID_TYPES[1]:
            if PATH is not None:
                raise ValueError(
                    "Your build configuration "
                    + f"({path_to_build_config_file}) has a problem. "
                    + f"{toml_value_path}.type is set to {TYPE}, and "
                    + f"{toml_value_path}.path is set to {PATH}. When "
                    + f"{toml_value_path}.type is set to {TYPE}, "
                    + f"{toml_value_path}.path shouldn’t be used at "
                    + "all."
                )
            if COMMAND_NAME is None:
                raise ValueError(
                    "Your build configuration "
                    + f"({path_to_build_config_file}) has a problem. "
                    + f"{toml_value_path}.type is set to {TYPE}, but "
                    + f"there was no {toml_value_path}.command_name "
                    + f"TOML key. When {toml_value_path}.type is set to"
                    + f" {TYPE}, you need to set "
                    + f"{toml_value_path}.command_name to a TOML "
                    + "string."
                )
        elif TYPE == SEARCH_TUPLE_ITEM_VALID_TYPES[2]:
            if PATH is not None:
                raise ValueError(
                    "Your build configuration "
                    + f"({path_to_build_config_file}) has a problem. "
                    + f"{toml_value_path}.type is set to {TYPE}, and "
                    + f"{toml_value_path}.path is set to {PATH}. When "
                    + f"{toml_value_path}.type is set to {TYPE}, "
                    + f"{toml_value_path}.path shouldn’t be used at "
                    + "all."
                )
            if COMMAND_NAME is not None:
                raise ValueError(
                    "Your build configuration "
                    + f"({path_to_build_config_file}) has a problem. "
                    + f"{toml_value_path}.type is set to {TYPE}, and "
                    + f"{toml_value_path}.command_name is set to "
                    + f"{COMMAND_NAME}. When {toml_value_path}.type is "
                    + f"set to {TYPE}, {toml_value_path}.command_name "
                    + "shouldn’t be used at all."
                )
        else:
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + f"{toml_value_path}.type is set to {TYPE}. It should "
                + "not be set to that. Instead, it should be set to one"
                + f" of these: {SEARCH_TUPLE_ITEM_VALID_TYPES}."
            )
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
        return cls(
            TYPE,
            None if PATH is None else pathlib.Path(PATH),
            COMMAND_NAME
        )


class SearchTuple(abc.ABC, tuple[SearchTupleItem]):
    """
    A sequence that can be used to determine the location of a file or
    directory that the ttt-build-tool needs to use.
    """
    def __new__(
        cls,
        items: collections.abc.Iterable[SearchTupleItem]
    ) -> Self:
        return_value = super().__new__(cls, items)
        # This is a workaround for this problem:
        # <https://stackoverflow.com/q/24990397/7593853>.
        assert len(return_value.__abstractmethods__) == 0 # type: ignore
        return return_value

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

    @abc.abstractmethod
    def locate(self) -> pathlib.Path:
        """
        Finds the first item in self that is usable.

        This function will either return the absolute path of a usable
        item that’s in self, or it will raise an exception.
        """
        raise NotImplementedError


class GodotEditorSearchTuple(SearchTuple):
    @staticmethod
    def downloaded_godot_editor_path() -> pathlib.Path:
        """
        Downloads and extracts the Godot Engine editor if needed and
        then returns the path to the editor’s executable.

        If the Godot Engine editor hasn’t already been downloaded and
        the attempting to download it fails, then a
        requests.RequestException will be raised.
        """
        ZIP_FILE_PATH: Final = download_if_needed(
            "https://github.com/godotengine/godot-builds/releases/download/4.2.2-stable/Godot_v4.2.2-stable_linux.x86_64.zip",
            pathlib.Path("editor.zip"),
            "18f3ff63fb4359c26e76fa52d1a7c5ccd6aaf17c063a2863fe3600aba66a49d4"
        )
        EXTRACTED_DIR_PATH: Final = pathlib.Path(
            ZIP_FILE_PATH.parent,
            "extracted"
        )
        EXECUTABLE_PATH: Final = pathlib.Path(
            EXTRACTED_DIR_PATH,
            "Godot_v4.2.2-stable_linux.x86_64"
        )
        if not EXTRACTED_DIR_PATH.exists():
            shutil.unpack_archive(ZIP_FILE_PATH, EXTRACTED_DIR_PATH)
            EXECUTABLE_PATH.chmod(0o755)
        return EXECUTABLE_PATH

    def locate(self) -> pathlib.Path:
        VALID_TYPES: Final = (
            "use_path_that_exists_at_build_time",
            "locate_using_path_env_var_at_build_time",
            "download_at_build_time"
        )
        item: SearchTupleItem
        path_to_test: Optional[pathlib.Path]
        for item in self:
            if item.type == VALID_TYPES[0]:
                assert item.path is not None
                path_to_test = item.path.absolute()
            elif item.type == VALID_TYPES[1]:
                assert item.command_name is not None
                shutil_result = shutil.which(item.command_name)
                if shutil_result is None:
                    path_to_test = None
                    print(f"Failed to find command {item.command_name}.")
                else:
                    path_to_test = pathlib.Path(shutil_result)
            elif item.type == VALID_TYPES[2]:
                try:
                    path_to_test = self.downloaded_godot_editor_path()
                except requests.RequestException:
                    warnings.warn(
                        "Failed to download the Godot Engine editor."
                    )
                    path_to_test = None
            else:
                raise ValueError(
                    "One of the items in "
                    + "godot_editor_executable.search_list has an "
                    + f"invalid type: {repr(item.type)}. Its type "
                    + "should have been one of these: "
                    + repr(VALID_TYPES)
                )
            if path_to_test is not None:
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


class GodotExportTemplatesSearchTuple(SearchTuple):
    @staticmethod
    def downloaded_godot_export_templates_path() -> pathlib.Path:
        """
        Downloads and extracts the Godot export templates if needed and
        then returns the path to their directory.

        If the export templates haven’t already been downloaded and
        attempting to download them fails, then a
        requests.RequestException will be raised.
        """
        ZIP_FILE_PATH: Final = download_if_needed(
            "https://github.com/godotengine/godot-builds/releases/download/4.2.2-stable/Godot_v4.2.2-stable_export_templates.tpz",
            # A .tpz file is actually just a ZIP file with a different
            # file extension [1]. We need its name to actually end with
            # “.zip”, though, or else shutil.unpack_archive will fail.
            #
            # [1]: <https://docs.godotengine.org/en/4.2/tutorials/export/exporting_projects.html#export-templates>
            pathlib.Path("export_templates.zip"),
            "df791307a118baf29a665db166a233ff221099499888b580a3af2a4198ac33fc"
        )
        EXTRACTED_DIR_PATH: Final = pathlib.Path(
            ZIP_FILE_PATH.parent,
            "extracted"
        )
        if not EXTRACTED_DIR_PATH.exists():
            shutil.unpack_archive(ZIP_FILE_PATH, EXTRACTED_DIR_PATH)
        return EXTRACTED_DIR_PATH

    def locate(self) -> pathlib.Path:
        VALID_TYPES: Final = (
            "use_path_that_exists_at_build_time",
            "download_at_build_time"
        )
        item: SearchTupleItem
        path_to_test: Optional[pathlib.Path]
        for item in self:
            if item.type == VALID_TYPES[0]:
                assert item.path is not None
                path_to_test = item.path
            elif item.type == VALID_TYPES[1]:
                try:
                    path_to_test = (
                        self.downloaded_godot_export_templates_path()
                    )
                except requests.RequestException:
                    warnings.warn(
                        "Failed to download the Godot export templates."
                    )
                    path_to_test = None
            else:
                raise ValueError(
                    "One of the items in "
                    + "godot_export_templates.search_list has an "
                    + f"invalid type: {repr(item.type)}. Its type "
                    + "should have been one of these: "
                    + repr(VALID_TYPES)
                )
            if path_to_test is not None:
                if path_to_test.is_dir():
                    return path_to_test
                else:
                    print(
                        "The Godot export templates can’t possibly in "
                        + f"the {path_to_test} directory. "
                        + f"{path_to_test} either does not exist or is "
                        + "not actually a directory."
                    )
            warnings.warn(
                "One of the items on the build configuration’s "
                + "godot_export_templates.search_list is not "
                + "usable."
            )
        raise ValueError(
            "None of the items on the build configuration’s "
            + "godot_export_templates.search_list were usable."
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
        # godot_export_templates_search_tuple
        try:
            GODOT_EXPORT_TEMPLATES_TABLE: Final = (
                PARSED_TOML_DOCUMENT.pop("godot_export_templates")
            )
        except KeyError as original_exception:
            NEW_EXCEPTION_3: Final = ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. It’s "
                + "supposed to contain a key named "
                + "“godot_export_templates”, but it doesn’t."
            )
            raise NEW_EXCEPTION_3 from original_exception
        if not isinstance(GODOT_EXPORT_TEMPLATES_TABLE, dict):
            raise ValueError(
                "Your build configuration "
                + f"({path_to_build_config_file}) has a problem. "
                + "godot_export_templates is supposed to be a TOML "
                + "table, but it isn’t."
            )
        self.godot_export_templates_tuple: Final = (
            GodotExportTemplatesSearchTuple.from_parsed_toml_table(
                path_to_build_config_file,
                "godot_export_templates",
                GODOT_EXPORT_TEMPLATES_TABLE
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
