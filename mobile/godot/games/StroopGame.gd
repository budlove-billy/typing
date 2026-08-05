extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const COLORS := [Color("#e85c70"), Color("#4c6fff"), Color("#1f9d78"), Color("#d99327"), Color("#9b63d7")]
const COLOR_KEYS := ["color_red", "color_blue", "color_green", "color_yellow", "color_purple"]
const ROUNDS := 14

var word: Label
var status: Label
var round_label: Label
var buttons: Array[Button] = []
var target_index := 0
var round_index := 0
var correct_count := 0
var locked := false
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.randomize()
    _build()
    _new_prompt()

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
    intro_box.add_child(GameTools.label("FOCUS  |  STROOP", 10, ThemeKit.AMBER))
    intro_box.add_child(GameTools.label(I18n.t("stroop_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("stroop_pick"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 14", ThemeKit.AMBER_SOFT, ThemeKit.AMBER)
    row.add_child(round_label)
    var word_card := PanelContainer.new()
    word_card.custom_minimum_size = Vector2(0, 250)
    word_card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    word_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 18, true))
    root.add_child(word_card)
    word = GameTools.label("", 42, ThemeKit.INK, HORIZONTAL_ALIGNMENT_CENTER)
    word.size_flags_vertical = Control.SIZE_EXPAND_FILL
    word_card.add_child(word)
    var colors := GridContainer.new()
    colors.columns = 2
    colors.add_theme_constant_override("h_separation", 9)
    colors.add_theme_constant_override("v_separation", 9)
    root.add_child(colors)
    for index in range(COLORS.size()):
        var color_button: Button = GameTools.button(I18n.t(COLOR_KEYS[index]), COLORS[index].lightened(0.36), COLORS[index].darkened(0.25), 66, COLORS[index])
        color_button.pressed.connect(_answer.bind(index, color_button))
        colors.add_child(color_button)
        buttons.append(color_button)
    root.add_child(GameTools.label(I18n.t("stroop_pick"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_prompt() -> void:
    locked = false
    target_index = rng.randi_range(0, COLORS.size() - 1)
    var word_index := target_index
    if rng.randf() < 0.72:
        word_index = rng.randi_range(0, COLORS.size() - 1)
        if word_index == target_index:
            word_index = (word_index + 1) % COLORS.size()
    word.text = I18n.t(COLOR_KEYS[word_index])
    word.add_theme_color_override("font_color", COLORS[target_index])
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("stroop_pick")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    word.scale = Vector2(0.9, 0.9)
    word.pivot_offset = word.size * 0.5
    var tween := create_tween()
    tween.tween_property(word, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK)

func _answer(index: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if index == target_index:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("stroop_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("stroop_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.3).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_prompt()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct_count, ROUNDS]})
