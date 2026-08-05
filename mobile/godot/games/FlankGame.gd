extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 12
const LEFT := "←"
const RIGHT := "→"

var prompt: Label
var status: Label
var round_label: Label
var round_index := 0
var correct_count := 0
var total_ms := 0
var started_at := 0
var target := LEFT
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
    intro_box.add_child(GameTools.label("FOCUS  |  FLANKER", 10, ThemeKit.AMBER))
    intro_box.add_child(GameTools.label(I18n.t("flank_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("flank_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 12", ThemeKit.AMBER_SOFT, ThemeKit.AMBER)
    row.add_child(round_label)
    var prompt_card := PanelContainer.new()
    prompt_card.custom_minimum_size = Vector2(0, 290)
    prompt_card.size_flags_vertical = Control.SIZE_EXPAND_FILL
    prompt_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 28, 16, true))
    root.add_child(prompt_card)
    prompt = GameTools.label("", 46, ThemeKit.BLUE_DARK, HORIZONTAL_ALIGNMENT_CENTER)
    prompt.size_flags_vertical = Control.SIZE_EXPAND_FILL
    prompt_card.add_child(prompt)
    var answers := HBoxContainer.new()
    answers.add_theme_constant_override("separation", 10)
    root.add_child(answers)
    var left := GameTools.button(I18n.t("flank_left"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, 78, ThemeKit.BLUE)
    var right := GameTools.button(I18n.t("flank_right"), ThemeKit.PINK_SOFT, ThemeKit.PINK, 78, ThemeKit.PINK)
    left.pressed.connect(_answer.bind(LEFT, left))
    right.pressed.connect(_answer.bind(RIGHT, right))
    answers.add_child(left)
    answers.add_child(right)
    root.add_child(GameTools.label("IGNORE THE OUTSIDE  •  FOLLOW THE CENTER", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_prompt() -> void:
    locked = false
    target = LEFT if rng.randi_range(0, 1) == 0 else RIGHT
    var distractor := RIGHT if target == LEFT else LEFT
    var arrows := [distractor, distractor, target, distractor, distractor]
    if rng.randf() < 0.38:
        arrows = [target, target, target, target, target]
    prompt.text = "  ".join(arrows)
    prompt.add_theme_color_override("font_color", ThemeKit.BLUE_DARK if target == LEFT else ThemeKit.PINK)
    prompt.scale = Vector2(0.9, 0.9)
    prompt.pivot_offset = prompt.size * 0.5
    var tween := create_tween()
    tween.tween_property(prompt, "scale", Vector2.ONE, 0.18).set_trans(Tween.TRANS_BACK)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("flank_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    started_at = Time.get_ticks_msec()

func _answer(value: String, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    total_ms += maxi(1, Time.get_ticks_msec() - started_at)
    if value == target:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("flank_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("flank_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.3).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_prompt()

func _finish() -> void:
    var accuracy := float(correct_count) / float(ROUNDS)
    var average_ms := int(round(float(total_ms) / float(ROUNDS)))
    var speed := clampf(1.0 - (float(average_ms) - 300.0) / 1000.0, 0.0, 1.0)
    var score := clampi(int(round(accuracy * 760.0 + speed * 240.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %dms" % [correct_count, ROUNDS, average_ms]})
