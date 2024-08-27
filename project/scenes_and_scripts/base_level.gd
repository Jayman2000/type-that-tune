# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


var text_queue_i: int = 0
var text_queue: Array[String] = []:
    set(new_text_queue):
        text_queue = new_text_queue
        update_displayed_text()

@onready var text_to_type_label: Label = \
    $CenterContainer/VBoxContainer/TextToType
@onready var user_input_label: Label = \
    $CenterContainer/VBoxContainer/UserInput


func update_displayed_text() -> void:
    if len(text_queue) > 0:
        text_to_type_label.text = text_queue[text_queue_i]


func next_correct_character() -> String:
    var current_string: String = text_queue[text_queue_i]
    var current_string_i: int = len(user_input_label.text)
    if len(current_string) > current_string_i:
        return current_string[current_string_i]
    return ""


func _unhandled_input(event: InputEvent) -> void:
    if len(text_queue) > 0:
        if event is InputEventKey and event.pressed:
            if event.unicode != 0:
                var character_entered: String = char(event.unicode)
                if character_entered == next_correct_character():
                    user_input_label.text += character_entered
            elif event.keycode == KEY_ENTER:
                if text_to_type_label.text == user_input_label.text:
                    user_input_label.text = ""
