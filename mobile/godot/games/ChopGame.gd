extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 8

var stage: ChopStage
var status: Label
var round_label: Label
var round_index := 0
var correct_count := 0
var total_ms := 0
var started_at := 0
var branch_side := 0
var locked := false
var rng := RandomNumberGenerator.new()

class ChopStage extends Control:
    var branch_side := 0
    var pulse := 0.0

    func _ready() -> void:
        mouse_filter = Control.MOUSE_FILTER_IGNORE
        set_process(true)

    func set_branch(side: int) -> void:
        branch_side = side
        pulse = 0.0
        queue_redraw()

    func _process(delta: float) -> void:
        pulse += delta
        queue_redraw()

    func _draw() -> void:
        if size.x < 20.0 or size.y < 20.0:
            return
        var panel_rect := Rect2(Vector2(6, 8), size - Vector2(12, 14))
        draw_style_box(ThemeKit.box(Color.WHITE, 26, Color("#e4e9f3"), 1, true), panel_rect)
        var center := size * 0.5
        var trunk := Rect2(center + Vector2(-27, -112), Vector2(54, 230))
        draw_style_box(ThemeKit.box(Color("#c98550"), 18, Color("#a9663e"), 2), trunk)
        draw_line(center + Vector2(-10, -82), center + Vector2(12, 92), Color("#e8ad75"), 5, true)
        var branch_y := center.y - 54
        if branch_side == 0:
            draw_line(Vector2(center.x - 4, branch_y), Vector2(center.x - 126, branch_y - 68), Color("#c98550"), 30, true)
        else:
            draw_line(Vector2(center.x + 4, branch_y), Vector2(center.x + 126, branch_y - 68), Color("#c98550"), 30, true)
        var mallow_pos := center + Vector2(0, 96 + sin(pulse * 4.0) * 3.0)
        draw_circle(mallow_pos, 30, Color("#95e3c6"))
        draw_circle(mallow_pos + Vector2(-10, -6), 6, ThemeKit.INK)
        draw_circle(mallow_pos + Vector2(10, -6), 6, ThemeKit.INK)
        draw_line(mallow_pos + Vector2(-8, 9), mallow_pos + Vector2(8, 9), ThemeKit.PINK, 4, true)

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
    intro_box.add_child(GameTools.label("SPEED  |  MALLOW TOWER", 10, ThemeKit.AMBER))
    intro_box.add_child(GameTools.label(I18n.t("chop_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("chop_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 08", ThemeKit.AMBER_SOFT, ThemeKit.AMBER)
    row.add_child(round_label)
    stage = ChopStage.new()
    stage.custom_minimum_size = Vector2(0, 320)
    stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
    root.add_child(stage)
    var answers := HBoxContainer.new()
    answers.add_theme_constant_override("separation", 10)
    root.add_child(answers)
    var left := GameTools.button(I18n.t("chop_left"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, 76, ThemeKit.BLUE)
    var right := GameTools.button(I18n.t("chop_right"), ThemeKit.PINK_SOFT, ThemeKit.PINK, 76, ThemeKit.PINK)
    left.pressed.connect(_answer.bind(0, left))
    right.pressed.connect(_answer.bind(1, right))
    answers.add_child(left)
    answers.add_child(right)
    root.add_child(GameTools.label(I18n.t("chop_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    branch_side = rng.randi_range(0, 1)
    stage.set_branch(branch_side)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("chop_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    started_at = Time.get_ticks_msec()

func _answer(side: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    total_ms += maxi(1, Time.get_ticks_msec() - started_at)
    var is_correct := side != branch_side
    if is_correct:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("chop_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("chop_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.32).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var accuracy := float(correct_count) / float(ROUNDS)
    var average_ms := float(total_ms) / float(ROUNDS)
    var speed := clampf(1.0 - (average_ms - 300.0) / 1100.0, 0.0, 1.0)
    var score := clampi(int(round(accuracy * 760.0 + speed * 240.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %dms" % [correct_count, ROUNDS, int(round(average_ms))]})
