extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const N := 2
const TOTAL := 10
const LETTERS := ["A", "C", "E", "G", "K", "M", "R", "T"]

var prompt: Label
var status: Label
var round_label: Label
var sequence: Array[String] = []
var index := 0
var correct_count := 0
var total_ms := 0
var started_at := 0
var locked := false
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.randomize()
    _build()
    _new_game()

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
    intro_box.add_child(GameTools.label("MEMORY  |  N-BACK", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("nback_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))

    var state := HBoxContainer.new()
    root.add_child(state)
    status = GameTools.label(I18n.t("nback_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    state.add_child(status)
    round_label = GameTools.pill("01 / 10", ThemeKit.PINK_SOFT, ThemeKit.PINK)
    state.add_child(round_label)

    var prompt_card := PanelContainer.new()
    prompt_card.custom_minimum_size = Vector2(0, 300)
    prompt_card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    prompt_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 30, 18, true))
    root.add_child(prompt_card)
    prompt = GameTools.label("?", 76, ThemeKit.BLUE_DARK, HORIZONTAL_ALIGNMENT_CENTER)
    prompt.size_flags_vertical = Control.SIZE_EXPAND_FILL
    prompt_card.add_child(prompt)

    var answers := HBoxContainer.new()
    answers.add_theme_constant_override("separation", 10)
    root.add_child(answers)
    var same := GameTools.button(I18n.t("nback_same"), ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 78, ThemeKit.TEAL)
    var different := GameTools.button(I18n.t("nback_different"), ThemeKit.PINK_SOFT, ThemeKit.PINK, 78, ThemeKit.PINK)
    same.pressed.connect(_answer.bind(true, same))
    different.pressed.connect(_answer.bind(false, different))
    answers.add_child(same)
    answers.add_child(different)
    root.add_child(GameTools.label("MATCH  /  NO MATCH", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_game() -> void:
    sequence.clear()
    for i in range(TOTAL):
        var value: String = LETTERS[rng.randi_range(0, LETTERS.size() - 1)]
        if i >= N and rng.randf() < 0.34:
            value = sequence[i - N]
        elif i > 0 and value == sequence[i - 1]:
            value = LETTERS[(LETTERS.find(value) + 1) % LETTERS.size()]
        sequence.append(value)
    index = 0
    correct_count = 0
    total_ms = 0
    _present()

func _present() -> void:
    locked = false
    prompt.text = sequence[index]
    prompt.modulate = Color(1, 1, 1, 0.3)
    prompt.scale = Vector2(0.92, 0.92)
    prompt.pivot_offset = prompt.size * 0.5
    var tween := create_tween()
    tween.set_parallel(true)
    tween.tween_property(prompt, "modulate", Color.WHITE, 0.16).set_trans(Tween.TRANS_SINE)
    tween.tween_property(prompt, "scale", Vector2.ONE, 0.22).set_trans(Tween.TRANS_BACK)
    round_label.text = "%02d / %02d" % [index + 1, TOTAL]
    status.text = I18n.t("nback_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    started_at = Time.get_ticks_msec()

func _answer(is_match: bool, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    total_ms += maxi(1, Time.get_ticks_msec() - started_at)
    var expected := index >= N and sequence[index] == sequence[index - N]
    if is_match == expected:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("nback_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("nback_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.32).timeout
    index += 1
    if index >= TOTAL:
        _finish()
    else:
        _present()

func _finish() -> void:
    var accuracy := float(correct_count) / float(TOTAL)
    var average_ms := int(round(float(total_ms) / float(TOTAL)))
    var speed_bonus := clampf(1.0 - (float(average_ms) - 350.0) / 1100.0, 0.0, 1.0)
    var score := clampi(int(round(accuracy * 760.0 + speed_bonus * 240.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %dms" % [correct_count, TOTAL, average_ms]})
