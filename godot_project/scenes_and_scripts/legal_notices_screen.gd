# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends CanvasItem


const DocumentViewer := preload(
    "res://scenes_and_scripts/document_viewer.gd"
)

@onready var project_selector: Node = \
    $MarginContainer/Panel/MarginContainer/VBoxContainer/ProjectSelector


func dictionary_to_nicely_formatted_list(
    to_convert: Dictionary,
    keys: Array[String],
    titles: Array[String]
) -> String:
    assert(len(keys) == len(titles))
    for key in to_convert.keys():
        assert(key in keys)

    var return_value: String = ""
    for i in len(keys):
        var key: String = keys[i]
        var title: String = titles[i]

        return_value += title + ":\n"
        for item in to_convert[key]:
            return_value += "\t" + str(item) + "\n"
        return_value += "\n"
    return return_value


func set_up_godot_legal_notices() -> void:

    var legal_notices_for_godot: Node = \
        project_selector.get_node("Legal notices for Godot")
    var godot_authors_text_box: TextEdit = \
        legal_notices_for_godot.get_node("Authors")
    var godot_donors_text_box: TextEdit = \
        legal_notices_for_godot.get_node("Donors")
    var godot_copyright_notices: TextEdit = \
        legal_notices_for_godot.get_node("Copyright notices")
    var godot_licenes: DocumentViewer = \
        legal_notices_for_godot.get_node("Licenses")
    const AUTHOR_INFO_KEYS: Array[String] = [
        "founders",
        "lead_developers",
        "project_managers",
        "developers"
    ]
    const AUTHOR_INFO_TITLES: Array[String] = [
        "Founders",
        "Lead Developers",
        "Project Managers",
        "Developers"
    ]
    godot_authors_text_box.text = dictionary_to_nicely_formatted_list(
        Engine.get_author_info(),
        AUTHOR_INFO_KEYS,
        AUTHOR_INFO_TITLES
    )

    const DONOR_INFO_KEYS: Array[String] = [
        "patrons",
        "platinum_sponsors",
        "gold_sponsors",
        "silver_sponsors",
        "diamond_members",
        "titanium_members",
        "platinum_members",
        "gold_members",
    ]
    const DONOR_INFO_TITLES: Array[String] = [
        "Patrons",
        "Platinum Sponsors",
        "Gold Sponsors",
        "Silver Sponsors",
        "Diamond Members",
        "Titanium Members",
        "Platinum Members",
        "Gold Members",
    ]
    godot_donors_text_box.text = dictionary_to_nicely_formatted_list(
        Engine.get_donor_info(),
        DONOR_INFO_KEYS,
        DONOR_INFO_TITLES
    )

    var copyright_info: Array[Dictionary] = Engine.get_copyright_info()
    var copyright_info_as_a_string: String = ""
    for piece_of_copyright_information: Dictionary in copyright_info:
        copyright_info_as_a_string += \
            str(piece_of_copyright_information["name"]) \
            + ":\n"
        for part: Dictionary in piece_of_copyright_information["parts"]:
            # Files for this part
            copyright_info_as_a_string += "\tFiles:\n"
            for file in part["files"]:
                copyright_info_as_a_string += "\t\t" + str(file) + ":\n"
            # Copyright notices for this part
            copyright_info_as_a_string += "\tCopyright notices:\n"
            for copyright_notice in part["copyright"]:
                copyright_info_as_a_string += \
                    str(copyright_notice).indent("\t\t") \
                    + "\n"
            # License name for this part
            copyright_info_as_a_string += \
                "\tLicense name: " \
                + str(part["license"]) \
                + "\n"
        copyright_info_as_a_string += "\n"
    godot_copyright_notices.text = copyright_info_as_a_string
    godot_licenes.change_documents_list(Engine.get_license_info())


func set_up_ttt_legal_notices() -> void:
    const LONG_NAME := "Legal notices for Type That Tune’s source code"
    const LONG_NAME2 := "Text of licenses used in SPDX document"
    var legal_notices_for_ttt: Node = \
        project_selector.get_node(LONG_NAME)
    var spdx_document_text_box: Node = \
        legal_notices_for_ttt.get_node("SPDX document")
    var licenses_document_viewer: DocumentViewer = \
        legal_notices_for_ttt.get_node(LONG_NAME2)

    var spdx_document_file = FileAccess.open(
        "res://generated/type_that_tune_legal_notices.spdx",
        FileAccess.READ
    )
    spdx_document_text_box.text = spdx_document_file.get_as_text()
    spdx_document_file.close()

    var document_list: Dictionary = {}
    const LICENSES_DIR_PATH: String = "res://generated/licenses/"
    var license_filenames: PackedStringArray = \
        DirAccess.get_files_at(LICENSES_DIR_PATH)
    for license_filename: String in license_filenames:
        var license_file: FileAccess = FileAccess.open(
            LICENSES_DIR_PATH + license_filename,
            FileAccess.READ
        )
        document_list[license_filename] = license_file.get_as_text()
    licenses_document_viewer.change_documents_list(document_list)


func _ready() -> void:
    set_up_godot_legal_notices()
    set_up_ttt_legal_notices()


func _on_close_button_pressed():
    hide()


func _on_ttt_readme_meta_clicked(meta) -> void:
    OS.shell_open(str(meta))
