# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import abc
import enum
import pathlib
import shutil
import warnings
from typing import Any, Final, NoReturn, Optional, Self

import requests

from .. import run_command
from ..download import downloadables
from . import (
    build_config_error_message,
    pop_and_assert_correct_type,
    pop_and_assert_none_or_correct_type
)


class SearchItemType(enum.Enum):
    download_at_build_time = enum.auto()
    locate_using_path_env_var_at_build_time = enum.auto()
    use_path_that_exists_at_build_time = enum.auto()

    @classmethod
    def from_parsed_toml(
        cls,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        toml_value: str,
    ) -> Self:
        try:
            return cls[toml_value]
        except KeyError as original_exception:
            NEW_EXCEPTION: Final = ValueError(
                build_config_error_message(build_config_path)
                + f" {toml_value_path} was set to {repr(toml_value)}. "
                + f" It should never be set to {repr(toml_value)}. "
                + "Instead, it should be set to one of these values: "
                + repr(tuple(item.name for item in cls))
            )
            raise NEW_EXCEPTION from original_exception


class SearchItem(abc.ABC):
    """
    An object that can be used to locate a file or directory that the
    ttt-build-tool needs.
    """
    def __init__(
        self,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        type: SearchItemType,
        command_name: Optional[str],
        path: Optional[pathlib.Path]
    ) -> None:
        self.build_config_path: Final = build_config_path
        self.toml_value_path: Final = toml_value_path
        self.type: Final = type
        self.command_name: Final = command_name
        self.path: Final = path

    def assert_none_for_type(self, attribute_name: str) -> None:
        attribute_value = getattr(self, attribute_name)
        if attribute_value is not None:
            raise ValueError(
                build_config_error_message(self.build_config_path)
                + f" {self.toml_value_path}.type was set to "
                + f"{repr(self.type.name)}, and "
                + f"{self.toml_value_path}.{attribute_name} was set to "
                + f"{repr(attribute_value)}. When "
                + f"{self.toml_value_path}.type is set to "
                + f"{repr(self.type.name)}, "
                + f"{self.toml_value_path}.{attribute_name} shouldn’t "
                + "be used at all."
            )

    def assert_not_none_for_type(self, attribute_name: str) -> None:
        attribute_value = getattr(self, attribute_name)
        if attribute_value is None:
            raise ValueError(
                build_config_error_message(self.build_config_path)
                + f" {self.toml_value_path}.type was set to "
                + f"{repr(self.type.name)}, but "
                + "there was no "
                + f"{self.toml_value_path}.{attribute_name} key. When "
                + f"{self.toml_value_path}.type is set to "
                + f"{repr(self.type.name)}, there needs to be a "
                + f"{self.toml_value_path}.{attribute_name} key."
            )

    def raise_error_for_unsupported_type(self) -> NoReturn:
        raise ValueError(
            build_config_error_message(self.build_config_path)
            + f" {self.toml_value_path}.type was set to "
            + f"{repr(self.type.name)}. That type can’t be used in"
            + f" {self.toml_value_path}."
        )

    @abc.abstractmethod
    def locate(self) -> Optional[pathlib.Path]:
        """
        Tries to turn this SearchItem into a path.

        If this method successfully finds or obtains the item that’s
        being searched for, then it returns a pathlib.Path. If this
        method fails to find anything, then it returns None.

        Unlike SearchItem.locate_and_test, this method doesn’t test the
        path before returning it. The returned path might be unusable.
        """
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def test(cls, path: pathlib.Path) -> bool:
        """Returns True if path is usable."""
        raise NotImplementedError

    @staticmethod
    def test_godot(path: pathlib.Path) -> bool:
        print(f"Testing a Godot Engine editor executable ({path})…")
        COMMAND: Final = (path, "--version")
        try:
            run_command.run_command(
                COMMAND,
                pathlib.Path.cwd()
            )
            print("Test succeeded!")
            return True
        except (FileNotFoundError, run_command.NonZeroReturnCodeError):
            print("Test failed.")
            return False


    def locate_and_test(self) -> Optional[pathlib.Path]:
        """
        Tries to turn this SearchItem into a usable path.

        This method will make the SearchItem will try to find or obtain
        some sort of file or directory that the ttt-build-tool needs. If
        the item is found, then this function will return a pathlib.Path
        object. If the item cannot be found or if it fails a test, then
        this function will return a pathlib.Path
        """
        PATH: Final = self.locate()
        if PATH is not None and type(self).test(PATH):
            return PATH
        else:
            return None

    @classmethod
    def from_parsed_toml(
        cls,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        parsed_toml: dict[str, Any],
    ) -> Self:
        # TYPE
        TYPE_RAW: Final = pop_and_assert_correct_type(
            build_config_path,
            toml_value_path,
            parsed_toml,
            "type",
            str
        )
        TYPE: Final = SearchItemType.from_parsed_toml(
            build_config_path,
            f"{toml_value_path}.type",
            TYPE_RAW
        )
        # COMMAND_NAME
        COMMAND_NAME: Final = pop_and_assert_none_or_correct_type(
            build_config_path,
            toml_value_path,
            parsed_toml,
            "command_name",
            str
        )
        # PATH
        PATH_RAW: Final = pop_and_assert_none_or_correct_type(
            build_config_path,
            toml_value_path,
            parsed_toml,
            "path",
            str
        )
        PATH: Final = (
            None if PATH_RAW is None else pathlib.Path(PATH_RAW)
        )
        # End
        # TODO: Complain if there’s extra stuff.
        return cls(
            build_config_path,
            toml_value_path,
            TYPE,
            COMMAND_NAME,
            PATH
        )


class GodotEditorExecutableSearchItem(SearchItem):
    def __init__(
        self,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        type: SearchItemType,
        command_name: Optional[str],
        path: Optional[pathlib.Path]
    ) -> None:
        super().__init__(
            build_config_path,
            toml_value_path,
            type,
            command_name,
            path
        )
        if self.type == SearchItemType.download_at_build_time:
            self.assert_none_for_type("command_name")
            self.assert_none_for_type("path")
            # editorconfig-checker-disable
        elif self.type == SearchItemType.locate_using_path_env_var_at_build_time:
            # editorconfig-checker-enable
            self.assert_not_none_for_type("command_name")
            self.assert_none_for_type("path")
            # editorconfig-checker-disable
        elif self.type == SearchItemType.use_path_that_exists_at_build_time:
            # editorconfig-checker-enable
            self.assert_none_for_type("command_name")
            self.assert_not_none_for_type("path")
        else:
            self.raise_error_for_unsupported_type()

    def locate(self) -> Optional[pathlib.Path]:
        if self.type == SearchItemType.download_at_build_time:
            GODOT_EDITOR_CURRENT_PLATFORM: Final = (
                downloadables.GODOT_EDITOR_CURRENT_PLATFORM
            )
            if GODOT_EDITOR_CURRENT_PLATFORM is None:
                warnings.warn(
                    "The ttt-build-tool doesn’t know how to download a "
                    + "copy of the Godot Engine editor for your current"
                    + " platform."
                )
                return None
            try:
                GODOT_EDITOR_EXECUTABLE_PATH: Final = (
                    GODOT_EDITOR_CURRENT_PLATFORM.extracted_path()
                )
                # TODO: I think that this is only needed because of a
                # Python bug.
                GODOT_EDITOR_EXECUTABLE_PATH.chmod(0o700)
                return GODOT_EDITOR_EXECUTABLE_PATH
            except requests.RequestException:
                return None
            # editorconfig-checker-disable
        elif self.type == SearchItemType.locate_using_path_env_var_at_build_time:
            assert self.command_name is not None
            PATH_STR_OR_NONE: Final = shutil.which(self.command_name)
            if PATH_STR_OR_NONE is None:
                return None
            else:
                return pathlib.Path(PATH_STR_OR_NONE)
        elif self.type == SearchItemType.use_path_that_exists_at_build_time:
            return self.path
        else:
            raise RuntimeError("This should never happen.")
        # editorconfig-checker-enable

    @classmethod
    def test(cls, path: pathlib.Path) -> bool:
        return cls.test_godot(path)


class GodotExportTemplatesSearchItem(SearchItem):
    def __init__(
        self,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        type: SearchItemType,
        command_name: Optional[str],
        path: Optional[pathlib.Path]
    ) -> None:
        super().__init__(
            build_config_path,
            toml_value_path,
            type,
            command_name,
            path
        )
        if self.type == SearchItemType.download_at_build_time:
            self.assert_none_for_type("command_name")
            self.assert_none_for_type("path")
            # editorconfig-checker-disable
        elif self.type == SearchItemType.use_path_that_exists_at_build_time:
            # editorconfig-checker-enable
            self.assert_none_for_type("command_name")
            self.assert_not_none_for_type("path")
        else:
            self.raise_error_for_unsupported_type()

    def locate(self) -> Optional[pathlib.Path]:
        if self.type == SearchItemType.download_at_build_time:
            try:
                # editorconfig-checker-disable
                return downloadables.GODOT_EXPORT_TEMPLATES.extracted_path()
                # editorconfig-checker-enable
            except requests.RequestException:
                return None
            # editorconfig-checker-disable
        elif self.type == SearchItemType.use_path_that_exists_at_build_time:
            # editorconfig-checker-enable
            return self.path
        else:
            raise RuntimeError("This should never happen.")

    @classmethod
    def test(cls, path: pathlib.Path) -> bool:
        return path.is_dir()
