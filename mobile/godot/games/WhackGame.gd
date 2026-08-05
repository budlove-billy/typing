extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 12

var grid: GridContainer
var status: Label
var round_label: Label
var buttons: Array[Button] = []
var target_index := 0
var round_index := 0
var hit_count := 0
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.TEAL_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("COORDINATION  |  TAP", 10, ThemeKit.TEAL))
    intro_box.add_child(GameTools.label(I18n.t("whack_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("whack_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 12", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(round_label)
    grid = GridContainer.new()
    grid.columns = 3
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 10)
    grid.add_theme_constant_override("v_separation", 10)
    root.add_child(grid)
    root.add_child(GameTools.label("TAP THE MALLOW  •  IGNORE THE EMPTY HOLES", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    target_index = rng.randi_range(0, 8)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("whack_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    buttons.clear()
    for child in grid.get_children():
        child.queue_free()
    for index in range(9):
        var target := index == target_index
        var button: Button = GameTools.button("●" if target else "", ThemeKit.TEAL_SOFT if target else Color("#f2f5f8"), ThemeKit.TEAL if target else ThemeKit.SUBTLE, 76, ThemeKit.TEAL)
        button.add_theme_font_size_override("font_size", 33)
        button.pressed.connect(_tap.bind(index, button))
        grid.add_child(button)
        buttons.append(button)
    buttons[target_index].scale = Vector2(0.94, 0.94)
    buttons[target_index].pivot_offset = buttons[target_index].size * 0.5
    var tween := create_tween()
    tween.tween_property(buttons[target_index], "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK)

func _tap(index: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if index == target_index:
        hit_count += 1
        AudioDirector.good()
        status.text = I18n.t("whack_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        mistakes += 1
        AudioDirector.bad()
        status.text = I18n.t("whack_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.3).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(hit_count) / float(ROUNDS) * 1000.0 - float(mistakes) * 18.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %d mistakes" % [hit_count, ROUNDS, mistakes]})
