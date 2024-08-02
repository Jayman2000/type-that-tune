extends Node


signal correct_title_entered

var score = 0

@onready var ScoreLabel = $ScoreLabel
@onready var TextToType = $CenterContainer/VBoxContainer/TextToType
@onready var UserInput = $CenterContainer/VBoxContainer/UserInput


func _ready():
	update_text_to_type("8 Sides of Nico Nico Douga")


func update_text_to_type(new_text_to_type):
	TextToType.text = new_text_to_type
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
				UserInput.text = ""
				increase_score(len(TextToType.text))
				emit_signal("correct_title_entered")
