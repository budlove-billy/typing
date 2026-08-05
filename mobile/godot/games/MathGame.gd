extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 10

var equation: Label
var status: Label
var round_label: Label
var answer_grid: GridContainer
var target := 0
var round_index := 0
var correct_count := 0
var locked := false
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
    intro_box.add_child(GameTools.label("CALCULATION  |  QUICK MATH", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("math_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("math_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 10", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    var card := PanelContainer.new()
    card.custom_minimum_size = Vector2(0, 220)
    card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 16, true))
    root.add_child(card)
    equation = GameTools.label("", 40, ThemeKit.BLUE_DARK, HORIZONTAL_ALIGNMENT_CENTER)
    equation.size_flags_vertical = Control.SIZE_EXPAND_FILL
    card.add_child(equation)
    answer_grid = GridContainer.new()
    answer_grid.columns = 2
    answer_grid.add_theme_constant_override("h_separation", 9)
    answer_grid.add_theme_constant_override("v_separation", 9)
    root.add_child(answer_grid)
    root.add_child(GameTools.label(I18n.t("math_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    var a := rng.randi_range(3, 24)
    var b := rng.randi_range(2, 12)
    var operation := rng.randi_range(0, 2)
    if operation == 0:
        target = a + b
        equation.text = "%d + %d = ?" % [a, b]
    elif operation == 1:
        target = a - b
        equation.text = "%d − %d = ?" % [a, b]
    else:
        target = a * b
        equation.text = "%d × %d = ?" % [a, b]
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("math_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for child in answer_grid.get_children():
        child.queue_free()
    var options: Array[int] = [target]
    while options.size() < 4:
        var candidate := target + rng.randi_range(-8, 8)
        if candidate not in options:
            options.append(candidate)
    options.shuffle()
    for value in options:
        var button: Button = GameTools.button(str(value), ThemeKit.BLUE_SOFT, ThemeKit.BLUE_DARK, 70, ThemeKit.BLUE)
        button.add_theme_font_size_override("font_size", 22)
        button.pressed.connect(_answer.bind(value, button))
        answer_grid.add_child(button)

func _answer(value: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if value == target:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("math_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("math_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.28).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct_count, ROUNDS]})
