extends Node


signal correct_title_entered

var score = 0
var text_to_type_i = 0
var text_to_type = [""]

@onready var ScoreLabel = $ScoreLabel
@onready var TextToType = $CenterContainer/VBoxContainer/TextToType
@onready var UserInput = $CenterContainer/VBoxContainer/UserInput


func _ready():
	update_text_to_type("8 Sides of Nico Nico Douga")


func update_text_to_type(new_text_to_type):
	text_to_type_i = 0
	if new_text_to_type is Array:
		text_to_type = new_text_to_type
	else:
		text_to_type = [new_text_to_type]
	update_text_to_type_label()


func update_text_to_type_label():
	TextToType.text = text_to_type[text_to_type_i]
	UserInput.text = ""


func increase_score(amount_of_points_to_add):
	score += amount_of_points_to_add
	ScoreLabel.text = "Score: %s" % [score]


func _unhandled_key_input(event):
	if event is InputEventKey and event.pressed:
		if event.unicode != 0:
			UserInput.text += char(event.unicode)
		elif event.keycode == KEY_BACKSPACE and len(UserInput.text) != 0:
			UserInput.text = UserInput.text.substr(0, len(UserInput.text) - 1)
		elif event.keycode == KEY_ENTER:
			if TextToType.text == UserInput.text:
				increase_score(len(TextToType.text))
				emit_signal("correct_title_entered")
				text_to_type_i = (text_to_type_i + 1) % len(text_to_type)
				update_text_to_type_label()
