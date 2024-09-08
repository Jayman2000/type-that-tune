# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


signal text_queue_completed


var text_queue_i: int = 0

@export var queue_loops: bool = false
@export var text_queue: Array[String] = []:
    set(new_text_queue):
        text_queue = new_text_queue
        text_queue_i = 0
        update_displayed_text()

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var text_to_type_label: Label = \
    $CenterContainer/VBoxContainer/TextToType
@onready var user_input_label: Label = \
    $CenterContainer/VBoxContainer/UserInput
@onready var video_stream_player: VideoStreamPlayer = $VideoStreamPlayer


func _ready() -> void:
    update_displayed_text()


func update_displayed_text() -> void:
    if text_to_type_label != null:
        if len(text_queue) == 0:
                text_to_type_label.text = ""
        else:
            text_to_type_label.text = text_queue[text_queue_i]
    if user_input_label != null:
        user_input_label.text = ""


func advance_text_queue() -> void:
    text_queue_i += 1
    if text_queue_i >= len(text_queue):
        text_queue_i = 0
        if not queue_loops:
            text_queue = []
        emit_signal("text_queue_completed")
    update_displayed_text()


func next_correct_character() -> String:
    var current_string: String = text_queue[text_queue_i]
    var current_string_i: int = len(user_input_label.text)
    if len(current_string) > current_string_i:
        return current_string[current_string_i]
    return ""


func wait_for_text_queue_to_be_finished(
    # I’m using a PackedStringArray here instead of an Array[String] in
    # order to work around this bug:
    # <https://github.com/godotengine/godot/issues/78681>
    new_text_queue: PackedStringArray
) -> void:
    animation_player.pause()
    video_stream_player.paused = true

    if not new_text_queue.is_empty():
        var new_text_queue_as_a_reqular_array: Array[String] = []
        for item in new_text_queue:
            new_text_queue_as_a_reqular_array.append(item)
        text_queue = new_text_queue_as_a_reqular_array

    text_queue_completed.connect(
        func():
            animation_player.play()
            video_stream_player.paused = false,
        CONNECT_ONE_SHOT
    )


func _unhandled_key_input(event: InputEvent) -> void:
    if len(text_queue) > 0:
        if event is InputEventKey and event.pressed:
            var viewport: Viewport = get_viewport()
            if event.unicode != 0:
                var character_entered: String = char(event.unicode)
                if character_entered == next_correct_character():
                    user_input_label.text += character_entered
                viewport.set_input_as_handled()
            elif event.keycode == KEY_ENTER:
                if text_to_type_label.text == user_input_label.text:
                    user_input_label.text = ""
                    advance_text_queue()
                viewport.set_input_as_handled()


func display_end_screen() -> void:
    $EndScreen.show()


func _on_main_menu_button_pressed() -> void:
    get_tree().change_scene_to_packed(
        preload("res://scenes_and_scripts/title_screen.tscn")
    )
