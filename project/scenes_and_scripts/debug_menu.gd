# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends MarginContainer


@onready var animation_player: AnimationPlayer = \
    $"../../AnimationPlayer"
@onready var seek_position_input_box: LineEdit = \
    $Panel/VBoxContainer/HBoxContainer/SeekPositionInputBox
@onready var video_stream_player: VideoStreamPlayer = \
    $"../../VideoStreamPlayer"


func _on_seek_button_pressed():
    if seek_position_input_box.text.is_valid_float():
        var time: float = seek_position_input_box.text.to_float()
        animation_player.seek(
            time,
            # I don’t really know if we need to set update to true here,
            #but I’m guessing that it can’t hurt to do so.
            true
        )
        video_stream_player.stream_position = time
    else:
        push_error(
            "The seek position that you entered is not a valid float."
        )


func _on_rich_text_label_meta_clicked(meta) -> void:
    OS.shell_open(str(meta))
