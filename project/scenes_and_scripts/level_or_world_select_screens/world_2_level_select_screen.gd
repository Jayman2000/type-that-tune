# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


func _on_level_1_button_pressed() -> void:
    BackButtonHelper.change_scne_to_file(
        "res://scenes_and_scripts/levels/ronald_mcdonald_insanity.tscn"
    )


func _on_level_2_button_pressed() -> void:
    BackButtonHelper.change_scne_to_file(
        "res://scenes_and_scripts/levels/mcdonalds_countdown.tscn"
    )


func _on_back_button_pressed() -> void:
    BackButtonHelper.go_back()
