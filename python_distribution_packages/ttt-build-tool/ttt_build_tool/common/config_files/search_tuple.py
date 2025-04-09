# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import collections.abc
import pathlib
import warnings
from typing import Any, Final, Optional, Self

from . import (
    assert_correct_type,
    build_config_error_message,
    search_item
)


class SearchTuple[T: search_item.SearchItem](tuple[T]):
    """
    A sequence of search_item.SearchItems.

    SearchTuples are used to determine the path that ttt-build-tool
    should use to find something. For example, a SearchTuple of
    search_item.GodotEditorExecutableSearchItems would allow you to
    figure out the path to the Godot Engine editor executable that the
    ttt-build-tool should use.
    """
    def __new__(
        cls,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        items: collections.abc.Iterable[T]
    ) -> Self:
        return super().__new__(cls, items)

    def __init__(
        self,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        items: collections.abc.Iterable[T]
    ) -> None:
        super().__init__()
        self.build_config_path: Final = build_config_path
        self.toml_value_path: Final = toml_value_path
        self._path_to_use: Optional[pathlib.Path] = None

    def path_to_use(
        self,
        skip_downloadables: bool = False
    ) -> pathlib.Path:
        """
        Returns the path to the first usable item in self.

        An item is said to be usable if it can locate itself and if it
        passes its own test. Specifically, this is done via the
        search_item.SearchItem.locate and search_item.SearchItem.test
        methods.

        If skip_downloadables is set to True, then items that have the
        download_at_build_time type will be ignored.
        """
        if self._path_to_use is None:
            i: int
            for i in range(len(self)):
                item: T = self[i]
                # editorconfig-checker-disable
                if (
                    not skip_downloadables
                    or not item.type == search_item.SearchItemType.download_at_build_time
                ):
                # editorconfig-checker-enable
                    result: Optional[pathlib.Path] = (
                        item.locate_and_test()
                    )
                    if result is not None:
                        self._path_to_use = result
                        return self._path_to_use
                    warnings.warn(
                        f"{self.toml_value_path}[{i}] could not be "
                        + "used."
                    )
            raise ValueError(
                build_config_error_message(self.build_config_path)
                + " None of the items on the "
                + f"{self.toml_value_path} were usable."
            )
        else:
            return self._path_to_use

    @classmethod
    def from_parsed_toml(
        cls,
        build_config_path: pathlib.Path,
        toml_value_path: str,
        parsed_toml: list[Any],
        search_item_type: type[T]
    ) -> Self:
        TO_INCLUDE_IN_RESULT: Final = []
        i: int
        for i in range(len(parsed_toml)):
            item_toml_value_path: str = f"{toml_value_path}[{i}]"
            item: Any = parsed_toml[i]
            item = assert_correct_type(
                build_config_path,
                item_toml_value_path,
                item,
                dict
            )
            TO_INCLUDE_IN_RESULT.append(
                search_item_type.from_parsed_toml(
                    build_config_path,
                    item_toml_value_path,
                    item
                )
            )
        return cls(
            build_config_path,
            toml_value_path,
            TO_INCLUDE_IN_RESULT
        )


type GodotEditorExecutableSearchTuple = (
    SearchTuple[search_item.GodotEditorExecutableSearchItem]
)
type GodotExportTemplatesSearchTuple = (
    SearchTuple[search_item.GodotExportTemplatesSearchItem]
)
type PythonInterpreterSearchTuple = (
    SearchTuple[search_item.PythonInterpreterSearchItem]
)
