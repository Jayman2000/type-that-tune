# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


func _on_world_1_button_pressed() -> void:
    BackButtonHelper.change_scne_to_file(
        "res://scenes_and_scripts/level_or_world_select_screens/"
        + "world_1_level_select_screen.tscn"
    )


func _on_world_2_button_pressed() -> void:
    BackButtonHelper.change_scne_to_file(
        "res://scenes_and_scripts/level_or_world_select_screens/"
        + "world_2_level_select_screen.tscn"
    )


func _on_back_button_pressed() -> void:
    BackButtonHelper.go_back()
