# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends "res://scenes_and_scripts/base_level.gd"


@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var video_stream_player: VideoStreamPlayer = $VideoStreamPlayer


func set_up_part_1_signals() -> void:
    text_queue_completed.connect(
        func(): animation_player.play(&"part_2"),
        CONNECT_ONE_SHOT
    )
    text_queue_completed.connect(
        func(): $TutorialContainer/FadeOutPlayer.play(&"fade_out"),
        CONNECT_ONE_SHOT
    )


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
    if event is InputEventKey and event.pressed:
        if event.keycode == KEY_ESCAPE:
            if animation_player.is_playing():
                if animation_player.current_animation == "part_1":
                    # Skip to the end of the tutorial:
                    animation_player.advance(
                        animation_player.current_animation_length
                    )
                    get_viewport().set_input_as_handled()
                    return
    super._unhandled_key_input(event)
