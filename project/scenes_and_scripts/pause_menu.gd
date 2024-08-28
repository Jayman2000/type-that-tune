# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends ColorRect


signal unpaused


func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause"):
        var scene_tree: SceneTree = get_tree()
        if scene_tree.paused:
            visible = false
            scene_tree.paused = false
            unpaused.emit()
        else:
            visible = true
            scene_tree.paused = true
        get_viewport().set_input_as_handled()
