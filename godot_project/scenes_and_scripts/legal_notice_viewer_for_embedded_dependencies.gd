# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
extends TabContainer


const DocumentViewer := preload(
    "res://scenes_and_scripts/document_viewer.tscn"
)

var legal_notice_document_viewers: Array[Node] = []
var _legal_notice_dir_paths: Array[String] = []
var legal_notice_dir_paths: Array[String]:
    get = get_legal_notice_dir_paths, set = set_legal_notice_dir_paths

var _readme_text: String = ""
@export_multiline
var readme_text: String:
    get = get_readme_text, set = set_readme_text


func get_legal_notice_dir_paths() -> Array[String]:
    return _legal_notice_dir_paths


func set_legal_notice_dir_paths(new_legal_notice_dir_paths) -> void:
    _legal_notice_dir_paths = new_legal_notice_dir_paths
    for node in legal_notice_document_viewers:
        node.queue_free()
    for i in len(_legal_notice_dir_paths):
        var legal_notice_dir := _legal_notice_dir_paths[i]
        var legal_notice_document_viewer := DocumentViewer.instantiate()
        legal_notice_document_viewer.name = "Legal notices (%s)" % [i]
        # editorconfig-checker-disable
        legal_notice_document_viewer.change_documents_list_from_directory(
            legal_notice_dir
        )
        # editorconfig-checker-enable
        add_child(legal_notice_document_viewer)
        legal_notice_document_viewers.append(
            legal_notice_document_viewer
        )


func get_readme_text() -> String:
    return _readme_text


func set_readme_text(new_readme_text: String) -> void:
    _readme_text = new_readme_text
    var README: RichTextLabel = $README
    if README != null:
        README.text = _readme_text


func _ready() -> void:
    if readme_text == "":
        push_error(
            "The readme_text property should have been set, but it ",
            "wasn’t."
        )
    set_readme_text(readme_text)


func _on_readme_meta_clicked(meta: Variant) -> void:
    OS.shell_open(str(meta))
