# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


const TITLE_SCREEN_PATH: String = \
    "res://scenes_and_scripts/title_screen.tscn"

var paths_for_previous_scenes: Array[String] = []


func change_scne_to_file(new_scene_path: String) -> void:
    var scene_tree: SceneTree = get_tree()
    paths_for_previous_scenes.append(
        scene_tree.current_scene.scene_file_path
    )
    scene_tree.change_scene_to_file(new_scene_path)


func go_back() -> void:
    var scene_tree: SceneTree = get_tree()
    var previous_scene_path = paths_for_previous_scenes.pop_back()
    if previous_scene_path is String:
        # TODO: Why isn’t this type safe?
        scene_tree.change_scene_to_file(previous_scene_path)
    else:
        push_warning(
            "Tried to go back, but paths_for_previous_scenes was empty."
            + " Going back to the title screen…"
        )
        scene_tree.change_scene_to_file(TITLE_SCREEN_PATH)


func return_to_title_screen() -> void:
    paths_for_previous_scenes = []
    get_tree().change_scene_to_file(TITLE_SCREEN_PATH)
