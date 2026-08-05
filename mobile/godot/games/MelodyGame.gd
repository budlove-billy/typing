extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const PADS := 4
const ROUNDS := 5

var status: Label
var round_label: Label
var pads: Array[Button] = []
var sequence: Array[int] = []
var input_position := 0
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("SOUND  |  MELODY", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("melody_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("melody_listen"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 05", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    var pads_grid := GridContainer.new()
    pads_grid.columns = 2
    pads_grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    pads_grid.add_theme_constant_override("h_separation", 10)
    pads_grid.add_theme_constant_override("v_separation", 10)
    root.add_child(pads_grid)
    var fills := [ThemeKit.PINK_SOFT, ThemeKit.BLUE_SOFT, ThemeKit.TEAL_SOFT, ThemeKit.AMBER_SOFT]
    var inks := [ThemeKit.PINK, ThemeKit.BLUE, ThemeKit.TEAL, ThemeKit.AMBER]
    for index in range(PADS):
        var pad: Button = GameTools.button("♪", fills[index], inks[index], 100, inks[index])
        pad.add_theme_font_size_override("font_size", 32)
        pad.pressed.connect(_pad_pressed.bind(index, pad))
        pads_grid.add_child(pad)
        pads.append(pad)
    root.add_child(GameTools.label(I18n.t("melody_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    accepting = false
    sequence.clear()
    var length := 2 + round_index
    for i in range(length):
        sequence.append(rng.randi_range(0, PADS - 1))
    input_position = 0
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("melody_listen")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for pad in pads:
        pad.disabled = true
    _play_sequence()

func _play_sequence() -> void:
    for value in sequence:
        status.text = I18n.t("melody_listen")
        AudioDirector.note(value)
        var pad := pads[value]
        GameTools.animate_press(pad)
        await get_tree().create_timer(0.34).timeout
    status.text = I18n.t("melody_tap")
    accepting = true
    for pad in pads:
        pad.disabled = false

func _pad_pressed(index: int, pad: Button) -> void:
    if not accepting:
        return
    GameTools.animate_press(pad)
    AudioDirector.note(index)
    if index != sequence[input_position]:
        accepting = false
        mistakes += 1
        AudioDirector.bad()
        status.text = I18n.t("melody_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
        await get_tree().create_timer(0.44).timeout
        round_index += 1
        if round_index >= ROUNDS:
            _finish()
        else:
            _new_round()
        return
    input_position += 1
    status.text = I18n.t("melody_good")
    status.add_theme_color_override("font_color", ThemeKit.TEAL)
    if input_position >= sequence.size():
        accepting = false
        completed += 1
        AudioDirector.good()
        await get_tree().create_timer(0.44).timeout
        round_index += 1
        if round_index >= ROUNDS:
            _finish()
        else:
            _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(completed) / float(ROUNDS) * 1000.0 - float(mistakes) * 28.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %d mistakes" % [completed, ROUNDS, mistakes]})
