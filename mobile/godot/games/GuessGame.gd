extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 10

var equation: Label
var status: Label
var round_label: Label
var options: GridContainer
var answer := 0
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.AMBER_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("CALCULATION  |  ESTIMATE", 10, ThemeKit.AMBER))
    intro_box.add_child(GameTools.label(I18n.t("guess_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("guess_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 10", ThemeKit.AMBER_SOFT, ThemeKit.AMBER)
    row.add_child(round_label)
    var card := PanelContainer.new()
    card.custom_minimum_size = Vector2(0, 220)
    card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 16, true))
    root.add_child(card)
    equation = GameTools.label("", 37, ThemeKit.AMBER, HORIZONTAL_ALIGNMENT_CENTER)
    equation.size_flags_vertical = Control.SIZE_EXPAND_FILL
    card.add_child(equation)
    options = GridContainer.new()
    options.columns = 2
    options.add_theme_constant_override("h_separation", 9)
    options.add_theme_constant_override("v_separation", 9)
    root.add_child(options)
    root.add_child(GameTools.label(I18n.t("guess_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    var a := rng.randi_range(12, 90)
    var b := rng.randi_range(3, 20)
    answer = a * b
    equation.text = "%d × %d ≈ ?" % [a, b]
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("guess_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for child in options.get_children():
        child.queue_free()
    var step := maxi(5, int(round(float(answer) / 20.0)))
    var values: Array[int] = [answer, answer - step, answer + step, answer + step * 2]
    values.shuffle()
    for value in values:
        var button: Button = GameTools.button(str(value), ThemeKit.AMBER_SOFT, ThemeKit.AMBER, 70, ThemeKit.AMBER)
        button.add_theme_font_size_override("font_size", 21)
        button.pressed.connect(_answer.bind(value, button))
        options.add_child(button)

func _answer(value: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    var closest: bool = abs(value - answer) <= abs(answer - (answer - maxi(5, int(round(float(answer) / 20.0)))))
    if closest:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("guess_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("guess_wrong")
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
