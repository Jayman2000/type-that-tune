# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


@onready var legal_notices_screen: CanvasItem = $LegalNoticesScreen


func _on_rich_text_label_meta_clicked(_meta) -> void:
    legal_notices_screen.show()


func _on_play_button_pressed():
    get_tree().change_scene_to_file(
        "res://scenes_and_scripts/levels/clowns_tenth_anniversary.tscn"
    )
