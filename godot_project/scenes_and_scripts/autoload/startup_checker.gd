# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
extends Node
## Performs checks, and then self-descructs.
##
## This script will cause a [Node] to run some checks and then delete
## itself. If any of the checks fail, then warnings will be emitted.
## This script is meant to be used an an autoload script.


## Does some checks, and then calls [method Node.queue_free].
func _init() -> void:
    # actual_godot_version
    var version_info: Dictionary = Engine.get_version_info()
    var actual_godot_version = "%s.%s.%s-%s" % [
        extract_version_component(version_info, "major"),
        extract_version_component(version_info, "minor"),
        extract_version_component(version_info, "patch"),
        extract_version_component(version_info, "status")
    ]
    # expected_godot_version
    const EXPECTED_GODOT_VERSION_FILE_PATH := (
        # editorconfig-checker-disable
        "res://generated/info_from_build_tool/expected_godot_version.txt"
        # editorconfig-checker-enable
    )
    var expected_godot_version := FileAccess.get_file_as_string(
        EXPECTED_GODOT_VERSION_FILE_PATH
    )
    var error_code: Error = FileAccess.get_open_error()
    if error_code != OK:
        push_error(
            "Failed to read %s as a text file. Error code: %s"
            % [EXPECTED_GODOT_VERSION_FILE_PATH, error_code]
        )
    if actual_godot_version != expected_godot_version:
        push_warning(
            "This game is intended to be played with Godot Engine ",
            "version ",
            expected_godot_version,
            ". You are currently using a different version of Godot ",
            "Engine: ",
            extract_version_component(version_info, "string")
        )
    queue_free()


## Returns part of [param version_info] in a type-safe manner.
##
## [param version_info] should be set to a [Dictionary] that was
## returned by [method Engine.get_version_info]. [param component_name]
## should be set to a key that you expect to be in the
## [param version_info] [Dictionary].
##
## This only reason why this method returns a [String] is to guarantee
## type safety. This method could have been written to return an [int]
## in a type-safe manner, but that would have been more work, and I
## don’t really know if it would have any benefits.
func extract_version_component(
    version_info: Dictionary,
    component_name: String
) -> String:
    return str(version_info.get(component_name, "(unknown)"))
