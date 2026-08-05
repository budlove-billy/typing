extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const QUESTIONS := [
    {"prompt": "2  ·  4  ·  6  ·  ?", "options": [7, 8, 9, 10], "answer": 8},
    {"prompt": "1  ·  3  ·  6  ·  10  ·  ?", "options": [12, 14, 15, 16], "answer": 15},
    {"prompt": "3  ·  6  ·  12  ·  24  ·  ?", "options": [36, 42, 48, 54], "answer": 48},
    {"prompt": "1  ·  1  ·  2  ·  3  ·  5  ·  ?", "options": [6, 7, 8, 9], "answer": 8},
    {"prompt": "○  △  ○  △  ○  ?", "options": ["○", "△", "□", "◇"], "answer": "△"},
    {"prompt": "5  ·  10  ·  8  ·  16  ·  14  ·  ?", "options": [18, 20, 24, 28], "answer": 28}
]

var prompt: Label
var status: Label
var round_label: Label
var options: GridContainer
var index := 0
var correct_count := 0
var locked := false

func _ready() -> void:
    _build()
    _new_question()

func _build() -> void:
    var root := VBoxContainer.new()
    root.add_theme_constant_override("separation", 12)
    root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(root)
    var intro := PanelContainer.new()
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("LOGIC  |  PATTERN TEST", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("iq_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("iq_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 06", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    var card := PanelContainer.new()
    card.custom_minimum_size = Vector2(0, 250)
    card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 16, true))
    root.add_child(card)
    prompt = GameTools.label("", 31, ThemeKit.BLUE_DARK, HORIZONTAL_ALIGNMENT_CENTER, true)
    prompt.size_flags_vertical = Control.SIZE_EXPAND_FILL
    card.add_child(prompt)
    options = GridContainer.new()
    options.columns = 2
    options.add_theme_constant_override("h_separation", 9)
    options.add_theme_constant_override("v_separation", 9)
    root.add_child(options)
    root.add_child(GameTools.label(I18n.t("iq_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_question() -> void:
    locked = false
    var question: Dictionary = QUESTIONS[index]
    prompt.text = str(question["prompt"])
    round_label.text = "%02d / %02d" % [index + 1, QUESTIONS.size()]
    status.text = I18n.t("iq_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for child in options.get_children():
        child.queue_free()
    for value in question["options"]:
        var button: Button = GameTools.button(str(value), ThemeKit.BLUE_SOFT, ThemeKit.BLUE_DARK, 70, ThemeKit.BLUE)
        button.add_theme_font_size_override("font_size", 22)
        button.pressed.connect(_answer.bind(value, button))
        options.add_child(button)

func _answer(value, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if value == QUESTIONS[index]["answer"]:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("iq_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("iq_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.34).timeout
    index += 1
    if index >= QUESTIONS.size():
        _finish()
    else:
        _new_question()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(QUESTIONS.size()) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct_count, QUESTIONS.size()]})
