extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const SHAPES := ["▲", "▶", "▼", "◀"]
const ROUNDS := 8

var target_label: Label
var status: Label
var round_label: Label
var options: GridContainer
var target_index := 0
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
    intro_box.add_child(GameTools.label("SPACE  |  ROTATE", 10, ThemeKit.TEAL))
    intro_box.add_child(GameTools.label(I18n.t("rotate_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("rotate_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 08", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(round_label)
    var target_card := PanelContainer.new()
    target_card.custom_minimum_size = Vector2(0, 180)
    target_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 26, 16, true))
    root.add_child(target_card)
    target_label = GameTools.label("", 64, ThemeKit.TEAL, HORIZONTAL_ALIGNMENT_CENTER)
    target_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
    target_card.add_child(target_label)
    options = GridContainer.new()
    options.columns = 2
    options.add_theme_constant_override("h_separation", 9)
    options.add_theme_constant_override("v_separation", 9)
    root.add_child(options)
    root.add_child(GameTools.label(I18n.t("rotate_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    target_index = rng.randi_range(0, 3)
    target_label.text = SHAPES[target_index]
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("rotate_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for child in options.get_children():
        child.queue_free()
    var choices := [target_index, (target_index + 1) % 4, (target_index + 2) % 4, (target_index + 3) % 4]
    choices.shuffle()
    for choice in choices:
        var button: Button = GameTools.button(SHAPES[choice], ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 88, ThemeKit.TEAL)
        button.add_theme_font_size_override("font_size", 34)
        button.pressed.connect(_answer.bind(choice, button))
        options.add_child(button)

func _answer(choice: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if choice == target_index:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("rotate_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("rotate_wrong")
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
