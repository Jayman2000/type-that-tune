# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
extends Node


var license_info = Engine.get_license_info()

@onready var project_selector: Node = \
    $MarginContainer/Panel/MarginContainer/VBoxContainer/ProjectSelector
@onready var legal_notices_for_godot: Node = \
    project_selector.get_node("Legal notices for Godot")
@onready var godot_authors_text_box: TextEdit = \
    legal_notices_for_godot.get_node("Authors")
@onready var godot_donors_text_box: TextEdit = \
    legal_notices_for_godot.get_node("Donors")
@onready var godot_copyright_notices: TextEdit = \
    legal_notices_for_godot.get_node("Copyright notices")
@onready var godot_licenes_names: ItemList = \
    legal_notices_for_godot.get_node("Licenses/Names")
@onready var godot_licenes_contents: TextEdit = \
    legal_notices_for_godot.get_node("Licenses/Contents")


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


func _ready() -> void:
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

    for license_name: String in license_info.keys():
        godot_licenes_names.add_item(license_name)


func _on_godot_license_names_item_selected(index: int) -> void:
    var item_name: String = godot_licenes_names.get_item_text(index)
    godot_licenes_contents.text = license_info[item_name]
