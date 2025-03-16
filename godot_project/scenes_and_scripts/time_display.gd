# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Label


@onready var animation_player: AnimationPlayer = $"../AnimationPlayer"
@onready var video_stream_player: VideoStreamPlayer = \
    $"../AspectRatioContainer/VideoStreamPlayer"


func _ready() -> void:
    disable()


func disable() -> void:
    hide()
    set_process(false)


func enable() -> void:
    set_process(true)
    show()


func _process(_delta) -> void:
    text = (
        "AnimationPlayer  : "
        + str(animation_player.current_animation_position)
        + "\n"
        + "VideoStreamPlayer: "
        + str(video_stream_player.stream_position)
    )
