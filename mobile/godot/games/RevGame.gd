extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 3

var sequence_label: Label
var status: Label
var round_label: Label
var keypad: GridContainer
var buttons: Array[Button] = []
var sequence: Array[int] = []
var input_position := -1
var round_index := 0
var completed := 0
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.PINK_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("MEMORY  |  REVERSE", 10, ThemeKit.PINK))
    intro_box.add_child(GameTools.label(I18n.t("rev_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("rev_watch"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 03", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    var sequence_card := PanelContainer.new()
    sequence_card.custom_minimum_size = Vector2(0, 220)
    sequence_card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    sequence_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 16, true))
    root.add_child(sequence_card)
    sequence_label = GameTools.label("", 42, ThemeKit.PINK, HORIZONTAL_ALIGNMENT_CENTER)
    sequence_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
    sequence_card.add_child(sequence_label)
    keypad = GridContainer.new()
    keypad.columns = 3
    keypad.add_theme_constant_override("h_separation", 8)
    keypad.add_theme_constant_override("v_separation", 8)
    root.add_child(keypad)
    for value in range(10):
        var key: Button = GameTools.button(str(value), ThemeKit.PINK_SOFT, ThemeKit.PINK, 52, ThemeKit.PINK)
        key.add_theme_font_size_override("font_size", 22)
        key.pressed.connect(_digit_pressed.bind(value, key))
        keypad.add_child(key)
        buttons.append(key)
    root.add_child(GameTools.label(I18n.t("rev_tap"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    accepting = false
    sequence.clear()
    var length := 3 + round_index
    for i in range(length):
        sequence.append(rng.randi_range(1, 9))
    input_position = sequence.size() - 1
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("rev_watch")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for button in buttons:
        button.disabled = true
    _show_sequence()

func _show_sequence() -> void:
    sequence_label.text = ""
    for digit in sequence:
        sequence_label.text += str(digit) + "  "
        await get_tree().create_timer(0.38).timeout
    await get_tree().create_timer(0.42).timeout
    sequence_label.text = "?"
    status.text = I18n.t("rev_tap")
    accepting = true
    for button in buttons:
        button.disabled = false

func _digit_pressed(value: int, button: Button) -> void:
    if not accepting:
        return
    GameTools.animate_press(button)
    if value == sequence[input_position]:
        AudioDirector.good()
        input_position -= 1
        status.text = I18n.t("rev_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
        if input_position < 0:
            accepting = false
            completed += 1
            await get_tree().create_timer(0.38).timeout
            round_index += 1
            if round_index >= ROUNDS:
                _finish()
            else:
                _new_round()
    else:
        accepting = false
        mistakes += 1
        AudioDirector.bad()
        status.text = I18n.t("rev_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
        await get_tree().create_timer(0.48).timeout
        round_index += 1
        if round_index >= ROUNDS:
            _finish()
        else:
            _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(completed) / float(ROUNDS) * 1000.0 - float(mistakes) * 35.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %d mistakes" % [completed, ROUNDS, mistakes]})
