# -*- coding: utf-8 -*-
# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
import os
import pathlib
import tomllib
from typing import Any, Final, NamedTuple, Self

from .. import EXPORTED_DIR
from . import pop_and_assert_correct_type, search_item, search_tuple


class BuildConfig(NamedTuple):
    build_config_path: pathlib.Path
    export_preset: str
    # editorconfig-checker-disable
    godot_editor_executable_search_list: search_tuple.GodotEditorExecutableSearchTuple
    godot_export_templates_search_list: search_tuple.GodotExportTemplatesSearchTuple
    # editorconfig-checker-enable

    def exported_project_executable_path(self) -> pathlib.Path:
        filename: str = "type-that-tune"
        if os.name == "nt":
            filename += ".exe"
        return pathlib.Path(
            EXPORTED_DIR,
            filename
        )


    @staticmethod
    def convert_toml_search_list[T: search_item.SearchItem](
        build_config_path: pathlib.Path,
        parsed_toml_document: dict[str, Any],
        key: str,
        search_item_type: type[T]
    ) -> search_tuple.SearchTuple[T]:
        SEARCH_LIST_RAW: Final = pop_and_assert_correct_type(
            build_config_path,
            "The build configuration",
            parsed_toml_document,
            key,
            list
        )
        return search_tuple.SearchTuple.from_parsed_toml(
            build_config_path,
            key,
            SEARCH_LIST_RAW,
            search_item_type
        )

    @classmethod
    def from_path(cls, build_config_path: pathlib.Path) -> Self:
        # Beginning
        with build_config_path.open(mode="rb") as file:
            try:
                PARSED_TOML_DOCUMENT: Final = tomllib.load(file)
            except tomllib.TOMLDecodeError as original_exception:
                NEW_EXCEPTION: Final = ValueError(
                    "Failed to interpret your build configuration "
                    + f"as TOML. Are you sure that {build_config_path} "
                    + "contains valid TOML?"
                )
                raise NEW_EXCEPTION from original_exception
        # Middle
        EXPORT_PRESET: Final = pop_and_assert_correct_type(
            build_config_path,
            "The build configuration",
            PARSED_TOML_DOCUMENT,
            "export_preset",
            str
        )
        GODOT_EDITOR_EXECUTABLE_SEARCH_LIST: Final = (
            cls.convert_toml_search_list(
                build_config_path,
                PARSED_TOML_DOCUMENT,
                "godot_editor_executable_search_list",
                search_item.GodotEditorExecutableSearchItem
            )
        )
        GODOT_EXPORT_TEMPLATES_SEARCH_LIST: Final = (
            cls.convert_toml_search_list(
                build_config_path,
                PARSED_TOML_DOCUMENT,
                "godot_export_templates_search_list",
                search_item.GodotExportTemplatesSearchItem
            )
        )
        # End
        # TODO: Complain if there’s extra stuff.
        return cls(
            build_config_path,
            EXPORT_PRESET,
            GODOT_EDITOR_EXECUTABLE_SEARCH_LIST,
            GODOT_EXPORT_TEMPLATES_SEARCH_LIST
        )

