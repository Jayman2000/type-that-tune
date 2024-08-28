# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends "res://scenes_and_scripts/base_level.gd"


const PauseMenu := preload("res://scenes_and_scripts/pause_menu.gd")

var player_has_confirmed_they_know_how_to_pause: bool = false
var waiting_for_player_to_pause: bool = false

@onready var pause_menu: PauseMenu = $PauseMenu
@onready var tutorial_text_box: RichTextLabel = \
    $TutorialContainer/Panel/MarginContainer/TutorialTextBox


func set_up_for_part_1() -> void:
    tutorial_text_box.text = (
        "[center]Welcome to Type That Tune![/center]\n\n"
        + "You can pause the game at any time by pressing one of these "
        + "keys:\n\n"
    )
    for event: InputEvent in InputMap.action_get_events(&"pause"):
        tutorial_text_box.text += "• " + event.as_text() + "\n"
    tutorial_text_box.text += \
        "\nTry pausing and unpausing the game now."


    text_queue_completed.connect(
        func(): animation_player.play(&"part_2"),
        CONNECT_ONE_SHOT
    )
    text_queue_completed.connect(
        func(): $TutorialContainer/FadeOutPlayer.play(&"fade_out"),
        CONNECT_ONE_SHOT
    )


func switch_to_second_message_for_part_1() -> void:
    pause_menu.show_tutorial_skip_tip()
    tutorial_text_box.text = (
        "Good job!\n\n"
        + "Whenever you see text appear in the center of your screen, "
        + "type it in, and then press ENTER. Make sure that you "
        + "capitalize everything correctly."
    )


func make_sure_player_knows_how_to_pause() -> void:
    if not player_has_confirmed_they_know_how_to_pause:
        animation_player.pause()
        waiting_for_player_to_pause = true



func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("skip"):
        if animation_player.is_playing():
            if animation_player.current_animation == "part_1":
                # Skip to the end of the tutorial:
                player_has_confirmed_they_know_how_to_pause = true
                animation_player.advance(
                    animation_player.current_animation_length
                )
                get_viewport().set_input_as_handled()
                return


func _on_pause_menu_unpaused():
    player_has_confirmed_they_know_how_to_pause = true
    if waiting_for_player_to_pause:
        waiting_for_player_to_pause = false
        animation_player.play()
