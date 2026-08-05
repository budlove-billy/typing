extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const PADS := 4
const ROUNDS := 6

var status: Label
var round_label: Label
var position_buttons: Array[Button] = []
var odd_position := 0
var round_index := 0
var correct_count := 0
var mistakes := 0
var accepting := false
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.randomize()
    _build()
    _new_round()

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
    intro_box.add_child(GameTools.label("SOUND  |  PITCH", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("pitch_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("pitch_listen"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 06", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    var sound_card := PanelContainer.new()
    sound_card.custom_minimum_size = Vector2(0, 260)
    sound_card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    sound_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 18, true))
    root.add_child(sound_card)
    sound_card.add_child(GameTools.label("♪   ♪   ♪   ♪", 42, ThemeKit.BLUE, HORIZONTAL_ALIGNMENT_CENTER))
    var answers := GridContainer.new()
    answers.columns = 2
    answers.add_theme_constant_override("h_separation", 9)
    answers.add_theme_constant_override("v_separation", 9)
    root.add_child(answers)
    for index in range(PADS):
        var button: Button = GameTools.button(str(index + 1), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, 72, ThemeKit.BLUE)
        button.add_theme_font_size_override("font_size", 22)
        button.pressed.connect(_answer.bind(index, button))
        answers.add_child(button)
        position_buttons.append(button)
    root.add_child(GameTools.label(I18n.t("pitch_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    accepting = false
    odd_position = rng.randi_range(0, PADS - 1)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("pitch_listen")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    _play_notes()

func _play_notes() -> void:
    var base := rng.randi_range(0, 2)
    for position in range(PADS):
        var note_index := base
        if position == odd_position:
            note_index = base + 1 if base < 2 else base - 1
        AudioDirector.note(note_index)
        GameTools.animate_press(position_buttons[position])
        await get_tree().create_timer(0.38).timeout
    status.text = I18n.t("pitch_tap")
    accepting = true

func _answer(index: int, button: Button) -> void:
    if not accepting:
        return
    accepting = false
    GameTools.animate_press(button)
    if index == odd_position:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("pitch_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        mistakes += 1
        AudioDirector.bad()
        status.text = I18n.t("pitch_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.42).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0 - float(mistakes) * 20.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %d mistakes" % [correct_count, ROUNDS, mistakes]})
