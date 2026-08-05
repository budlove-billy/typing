extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 8

var grid: GridContainer
var status: Label
var round_label: Label
var target_index := 0
var round_index := 0
var correct_count := 0
var mistakes := 0
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
    intro_box.add_child(GameTools.label("SIGHT  |  COMPARE", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("diff_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("diff_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 08", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    grid = GridContainer.new()
    grid.columns = 4
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 8)
    grid.add_theme_constant_override("v_separation", 8)
    root.add_child(grid)
    root.add_child(GameTools.label("COMPARE LEFT  •  RIGHT  |  TAP THE DIFFERENT PAIR", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    target_index = rng.randi_range(0, 15)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("diff_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for child in grid.get_children():
        child.queue_free()
    for index in range(16):
        var same := "●   ●"
        var different := "●   ○"
        var button: Button = GameTools.button(different if index == target_index else same, ThemeKit.BLUE_SOFT, ThemeKit.BLUE_DARK, 70, ThemeKit.BLUE)
        button.add_theme_font_size_override("font_size", 19)
        button.pressed.connect(_tap.bind(index, button))
        grid.add_child(button)

func _tap(index: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if index == target_index:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("diff_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        mistakes += 1
        AudioDirector.bad()
        status.text = I18n.t("diff_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.3).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0 - float(mistakes) * 18.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %d mistakes" % [correct_count, ROUNDS, mistakes]})
