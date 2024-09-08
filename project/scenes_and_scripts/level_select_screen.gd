# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


func _on_level_1_button_pressed() -> void:
    get_tree().change_scene_to_file(
        "res://scenes_and_scripts/levels/clowns_tenth_anniversary.tscn"
    )


func _on_level_2_button_pressed() -> void:
    get_tree().change_scene_to_file(
        "res://scenes_and_scripts/levels/"
        + "glorious_octagon_of_destiny.tscn"
    )


func _on_return_to_menu_button_pressed() -> void:
    get_tree().change_scene_to_file(
        "res://scenes_and_scripts/title_screen.tscn"
    )
