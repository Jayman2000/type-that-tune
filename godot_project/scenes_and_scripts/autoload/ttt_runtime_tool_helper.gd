# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
extends Node


var ttt_runtime_tool_command: String


func _init() -> void:
    const PATH = "res://generated/external_tool_info/ttt_build_tool.json"
    var file := FileAccess.open(PATH, FileAccess.READ)
    var contents := file.get_as_text()
    var parsed: Variant = JSON.parse_string(contents)
    if parsed != null:
        if parsed is Dictionary:
            var find_on_path = parsed.get("find_on_path")
            if find_on_path is bool:
                if find_on_path:
                    ttt_runtime_tool_command = "ttt-runtime-tool"
                    return
                else:
                    var location = parsed.get("location")
                    if location is String:
                        ttt_runtime_tool_command = location
                        return
                    else:
                        push_error(
                            PATH + " had find_on_path set to false, but"
                            + " it lacks a location variable, or its "
                            + "location variable isn’t a string."
                        )
            else:
                push_error(
                    PATH + " did not contain a find_on_path variable, "
                    + "or its find_on_path variable had the wrong type."
                )
        else:
            push_error(
                "The contents of %s were not a JSON object." % [PATH]
            )
    else:
        push_error("Failed to parse the contents of %s." % [PATH])

    push_warning(
        "Faling back to assuming that ttt-runtime-tool is on the "
        + "player’s PATH."
    )
    ttt_runtime_tool_command = "ttt-runtime-tool"


func _ready() -> void:
    # This is just a test.
    var output := []
    var exit_status := OS.execute(
        ttt_runtime_tool_command,
        [],
        output,
        true
    )
    print(output.pop_front())
    print("Exit status: ", exit_status)
