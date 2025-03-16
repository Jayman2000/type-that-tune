# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


var documents_list: Dictionary = {}

@onready var names: ItemList = $Names
@onready var contents: Node = $Contents


func change_documents_list(new_documents_list: Dictionary) -> void:
    documents_list = new_documents_list
    names.clear()
    for document_name in documents_list.keys():
        names.add_item(document_name)


func _on_names_item_selected(index: int) -> void:
    var document_name: String = names.get_item_text(index)
    contents.text = documents_list[document_name]
