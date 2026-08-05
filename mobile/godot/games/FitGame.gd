extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 8
const PATTERNS := [
    [1, 1, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0, 0, 0]
]

var target: Label
var status: Label
var round_label: Label
var options: GridContainer
var correct_index := 0
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.TEAL_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("SPACE  |  FIT", 10, ThemeKit.TEAL))
    intro_box.add_child(GameTools.label(I18n.t("fit_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("fit_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 08", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(round_label)
    var target_card := PanelContainer.new()
    target_card.custom_minimum_size = Vector2(0, 220)
    target_card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    target_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 16, true))
    root.add_child(target_card)
    target = GameTools.label("", 34, ThemeKit.TEAL, HORIZONTAL_ALIGNMENT_CENTER)
    target.size_flags_vertical = Control.SIZE_EXPAND_FILL
    target_card.add_child(target)
    options = GridContainer.new()
    options.columns = 2
    options.add_theme_constant_override("h_separation", 9)
    options.add_theme_constant_override("v_separation", 9)
    root.add_child(options)
    root.add_child(GameTools.label(I18n.t("fit_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    correct_index = rng.randi_range(0, 3)
    var pattern: Array = PATTERNS[rng.randi_range(0, PATTERNS.size() - 1)]
    target.text = _pattern_text(pattern)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("fit_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for child in options.get_children():
        child.queue_free()
    var choices: Array[String] = []
    for i in range(4):
        var choice_pattern: Array = pattern if i == correct_index else PATTERNS[(i + round_index + 1) % PATTERNS.size()]
        choices.append(_pattern_text(choice_pattern))
    var order := [0, 1, 2, 3]
    order.shuffle()
    for index in order:
        var button: Button = GameTools.button(choices[index], ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 94, ThemeKit.TEAL)
        button.add_theme_font_size_override("font_size", 25)
        button.pressed.connect(_answer.bind(index, button))
        options.add_child(button)

func _pattern_text(pattern: Array) -> String:
    var output := ""
    for index in range(pattern.size()):
        output += "■" if int(pattern[index]) == 1 else "·"
        if index % 3 == 2:
            output += "\n"
        else:
            output += " "
    return output

func _answer(index: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if index == correct_index:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("fit_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("fit_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.3).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct_count, ROUNDS]})
