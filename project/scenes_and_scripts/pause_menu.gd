# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends ColorRect


signal unpaused


func show_tutorial_skip_tip() -> void:
    var input_for_skip: String
    var skip_events: Array[InputEvent] = \
        InputMap.action_get_events(&"skip")
    if len(skip_events) > 0:
        input_for_skip = skip_events[0].as_text()
        if len(skip_events) > 1:
            push_warning(
                "Having multiple events for the skip action is not "
                + "supported yet."
            )
    else:
        push_error("There were no events for the skip action.")
        input_for_skip = "ERROR"
    $MarginContainer/TipText.text = (
        "Tip: You can skip the tutorial by pressing "
        + input_for_skip
        + "."
    )


func resume():
    visible = false
    get_tree().paused = false
    unpaused.emit()


func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("pause"):
        var scene_tree: SceneTree = get_tree()
        if scene_tree.paused:
            resume()
        else:
            visible = true
            scene_tree.paused = true
        get_viewport().set_input_as_handled()
