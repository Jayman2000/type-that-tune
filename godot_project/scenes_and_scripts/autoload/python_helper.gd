# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
extends Node


const EXTRACTED_FILES_DIR_PATH := "user://extracted_files"
var python_interpreter_to_use: String = ""
var legal_notice_dir_paths: Array[String] = []


func get_search_item_attribute(
    item_dir_path: String,
    attribute_name: String,
    push_error_for_file_not_found: bool
) -> String:
    var full_path := item_dir_path + "/" + attribute_name + ".txt"
    var return_value := FileAccess.get_file_as_string(full_path)
    var error_code: Error = FileAccess.get_open_error()
    if error_code != OK:
        # editorconfig-checker-disable
        if error_code != ERR_FILE_NOT_FOUND or push_error_for_file_not_found:
            # editorconfig-checker-enable
            push_error(
                "Failed to open and read “",
                full_path,
                "” as a UTF-8 text file. Error code: ",
                error_code
            )
    return return_value


func parent_directory(path: String) -> String:
    return path.rsplit("/", true, 1)[0]


func remove_dir_recursive(path: String) -> void:
    if not DirAccess.dir_exists_absolute(path):
        return

    var dir := DirAccess.open(path)
    if dir == null:
        push_error(
            "Failed to open ",
            var_to_str(path),
            " as a directory. Error code: ",
            DirAccess.get_open_error()
        )
        return
    var error_code: Error = dir.list_dir_begin()
    if error_code != OK:
        push_error(
            "Failed to list files in the ",
            var_to_str(path),
            " directory. Error code: ",
            error_code
        )
        return
    var filename: String = dir.get_next()
    while filename != "":
        if dir.current_is_dir():
            remove_dir_recursive(path + "/" + filename)
        error_code = dir.remove(filename)
        if error_code != OK:
            push_error(
                "Failed to delete ",
                var_to_str(filename),
                ". Error code: ",
                error_code
            )
        filename = dir.get_next()


func copy_dir_recursive(source: String, destination: String) -> void:
    var dir := DirAccess.open(source)
    if dir == null:
        push_error(
            "Failed to open ",
            var_to_str(source),
            " as a directory. Error code: ",
            DirAccess.get_open_error()
        )
        return
    var error_code: Error = dir.list_dir_begin()
    if error_code != OK:
        push_error(
            "Failed to list files in the ",
            var_to_str(source),
            " directory. Error code: ",
            error_code
        )
        return
    error_code = DirAccess.make_dir_absolute(destination)
    if error_code != OK:
        push_error(
            "Failed to create directory at this location: ",
            destination,
            ". Error code: ",
            error_code
        )
    var filename: String = dir.get_next()
    while filename != "":
        var source_subpath := source + "/" + filename
        var destination_subpath := destination + "/" + filename
        if dir.current_is_dir():
            copy_dir_recursive(source_subpath, destination_subpath)
        else:
            error_code = DirAccess.copy_absolute(
                source_subpath,
                destination_subpath
            )
            if error_code != OK:
                push_error(
                    "Failed to copy ",
                    var_to_str(source_subpath),
                    " to ",
                    var_to_str(destination_subpath),
                    ". Error code: ",
                    error_code
                )
        filename = dir.get_next()


func copy_dir_to_user_dir(source: String) -> String:
    var destination := source.trim_prefix("res://")
    destination = EXTRACTED_FILES_DIR_PATH + "/" + destination
    var error_code: Error = DirAccess.make_dir_recursive_absolute(
        parent_directory(destination)
    )
    if error_code != OK:
        push_error(
            "Failed to create a ",
            destination,
            " directory. Error code: ",
            error_code
        )
    copy_dir_recursive(source, destination)
    return destination


func _init() -> void:
    remove_dir_recursive(EXTRACTED_FILES_DIR_PATH)
    const PYTHON_INTERPRETER_SEARCH_LIST_DIR_PATH := (
        "res://generated/info_from_build_tool"
        + "/python_interpreter_search_list"
    )
    var search_list_index := 0
    while true:
        var current_item_dir_path := (
            PYTHON_INTERPRETER_SEARCH_LIST_DIR_PATH
            + "/"
            + str(search_list_index)
        )
        if not DirAccess.dir_exists_absolute(current_item_dir_path):
            break
        var type := get_search_item_attribute(
            current_item_dir_path,
            "type",
            true
        )
        var command_name := get_search_item_attribute(
            current_item_dir_path,
            "command_name",
            false
        )
        var path := get_search_item_attribute(
            current_item_dir_path,
            "path",
            false
        )
        var path_to_test: String
        match type:
            "download_at_build_time":
                var extracted_path := copy_dir_to_user_dir(
                    current_item_dir_path + "/download"
                )
                legal_notice_dir_paths.append(
                    extracted_path
                    + "/licenses"
                )
                path_to_test = ProjectSettings.globalize_path(
                    extracted_path + "/install/bin/python"
                )
                const FILE_PERMISSIONS := (
                    FileAccess.UNIX_READ_OWNER
                    | FileAccess.UNIX_WRITE_OWNER
                    | FileAccess.UNIX_EXECUTE_OWNER
                )
                var error_code: Error = FileAccess.set_unix_permissions(
                    path_to_test,
                    FILE_PERMISSIONS
                )
                if error_code != OK:
                    push_error(
                        "Failed to set UNIX-style file permisions for ",
                        var_to_str(path_to_test),
                        ". Error code: ",
                        error_code
                    )
            "locate_using_path_env_var_at_runtime":
                path_to_test = command_name
            "use_path_that_exists_at_runtime":
                path_to_test = path
            _:
                push_error(
                    "Unsupported type ",
                    var_to_str(type),
                    " for this Python interpreter search item: ",
                    var_to_str(current_item_dir_path)
                )
        var output: Array[String] = []
        print("Testing Python interpreter (%s)…" % [path_to_test])
        var exit_status := OS.execute(
            path_to_test,
            PackedStringArray(["--version"]),
            output,
            true
        )
        for item in output:
            print(item.trim_suffix("\n"))
        if exit_status == 0:
            print("Test suceeded!")
            if python_interpreter_to_use == "":
                python_interpreter_to_use = path_to_test
        else:
            print("Test failed. Exit status: ", exit_status)
            push_warning(
                "One of the items of the Python interpreter search ",
                "list isn’t usable."
            )
        search_list_index += 1
    if python_interpreter_to_use == "":
        print("No usable Python interpreters found. This is likely OK.")
    else:
        print(
            "Using this python interpreter: ",
            var_to_str(python_interpreter_to_use)
        )
