extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 3

var grid: GridContainer
var status: Label
var round_label: Label
var buttons: Array[Button] = []
var values: Array[int] = []
var next_value := 1
var round_index := 0
var tapped := 0
var mistakes := 0
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.randomize()
    _build()
    _new_board()

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
    intro_box.add_child(GameTools.label("SPEED  |  NUMBER TRAIL", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("trail_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("trail_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 03", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(round_label)
    grid = GridContainer.new()
    grid.columns = 4
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 9)
    grid.add_theme_constant_override("v_separation", 9)
    root.add_child(grid)
    root.add_child(GameTools.label("TAP 1 → 2 → 3 → ...", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_board() -> void:
    values.clear()
    buttons.clear()
    next_value = 1
    var count := 8 + round_index * 2
    for value in range(1, count + 1):
        values.append(value)
    values.shuffle()
    for child in grid.get_children():
        child.queue_free()
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("trail_round_ready")
    for value in values:
        var button: Button = GameTools.button(str(value), ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 68, ThemeKit.TEAL)
        button.add_theme_font_size_override("font_size", 24)
        button.pressed.connect(_tap_value.bind(value, button))
        grid.add_child(button)
        buttons.append(button)

func _tap_value(value: int, button: Button) -> void:
    if value != next_value:
        mistakes += 1
        AudioDirector.bad()
        GameTools.animate_press(button)
        status.text = I18n.t("trail_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
        await get_tree().create_timer(0.24).timeout
        status.text = I18n.t("trail_round_ready")
        status.add_theme_color_override("font_color", ThemeKit.MUTED)
        return
    GameTools.animate_press(button)
    button.disabled = true
    button.modulate = Color(1, 1, 1, 0.45)
    next_value += 1
    tapped += 1
    AudioDirector.good()
    status.text = I18n.t("trail_good")
    status.add_theme_color_override("font_color", ThemeKit.TEAL)
    if next_value > values.size():
        await get_tree().create_timer(0.38).timeout
        round_index += 1
        if round_index >= ROUNDS:
            _finish()
        else:
            _new_board()

func _finish() -> void:
    var base := float(tapped) / 30.0 * 900.0
    var penalty := float(mistakes) * 20.0
    var score := clampi(int(round(base - penalty)), 100, 1000)
    finished.emit({"score": score, "detail": "%d taps · %d mistakes" % [tapped, mistakes]})
