# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


var documents_list: Dictionary = {}


func change_documents_list_from_directory(path: String) -> void:
    var new_documents_list: Dictionary = {}
    var dir = DirAccess.open(path)
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
            "Failed to list contents of this directory: ",
            var_to_str(path),
            ". Error code: ",
            error_code
        )
        return
    var filename: String = dir.get_next()
    while filename != "":
        var subpath := path + "/" + filename
        if dir.current_is_dir():
            push_error(
                "Encountered subdirectory at ",
                subpath,
                ". This should never happen."
            )
        else:
            var file_contents := FileAccess.get_file_as_string(subpath)
            if file_contents == "":
                push_error(
                    "Failed to open ",
                    subpath,
                    " as a UTF-8 text file. Error code: ",
                    FileAccess.get_open_error()
                )
            new_documents_list[filename] = file_contents
        filename = dir.get_next()
    change_documents_list(new_documents_list)


func change_documents_list(new_documents_list: Dictionary) -> void:
    documents_list = new_documents_list
    var names: ItemList = $Names
    names.clear()
    for document_name in documents_list.keys():
        names.add_item(document_name)


func _on_names_item_selected(index: int) -> void:
    var document_name: String = $Names.get_item_text(index)
    $Contents.text = documents_list[document_name]
