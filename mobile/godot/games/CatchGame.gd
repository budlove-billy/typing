extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 10

var stage: CatchStage
var status: Label
var round_label: Label
var round_index := 0
var correct_count := 0
var mistakes := 0
var target_lane := 0
var locked := false
var rng := RandomNumberGenerator.new()

class CatchStage extends Control:
    var lane := 0
    var progress := 0.0
    var active := false

    func _ready() -> void:
        mouse_filter = Control.MOUSE_FILTER_IGNORE
        set_process(true)

    func start_drop(next_lane: int) -> void:
        lane = next_lane
        progress = 0.0
        active = true
        queue_redraw()

    func _process(delta: float) -> void:
        if not active:
            return
        progress = minf(1.0, progress + delta * 0.42)
        queue_redraw()

    func _draw() -> void:
        if size.x < 20.0 or size.y < 20.0:
            return
        var panel_rect := Rect2(Vector2(6, 8), size - Vector2(12, 14))
        draw_style_box(ThemeKit.box(Color.WHITE, 26, Color("#e4e9f3"), 1, true), panel_rect)
        var left := 44.0
        var width := maxf(1.0, (size.x - 88.0) / 4.0)
        for i in range(4):
            var x := left + width * float(i) + width * 0.5
            draw_line(Vector2(x, 32), Vector2(x, size.y - 36), Color("#e6eaf3"), 2.0, true)
            draw_style_box(ThemeKit.box(ThemeKit.TEAL_SOFT, 14), Rect2(x - 29, size.y - 58, 58, 24))
        if active:
            var ball_x := left + width * float(lane) + width * 0.5
            var ball_y := lerpf(58.0, size.y - 82.0, progress)
            draw_circle(Vector2(ball_x, ball_y + 7), 25, Color(0.08, 0.12, 0.25, 0.12))
            draw_circle(Vector2(ball_x, ball_y), 24, ThemeKit.PINK)
            draw_circle(Vector2(ball_x - 8, ball_y - 8), 7, Color(1, 1, 1, 0.52))

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
    intro_box.add_child(GameTools.label("COORDINATION  |  CATCH", 10, ThemeKit.TEAL))
    intro_box.add_child(GameTools.label(I18n.t("catch_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("catch_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 10", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(round_label)
    stage = CatchStage.new()
    stage.custom_minimum_size = Vector2(0, 300)
    stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
    root.add_child(stage)
    var lanes := HBoxContainer.new()
    lanes.add_theme_constant_override("separation", 8)
    root.add_child(lanes)
    for lane in range(4):
        var button: Button = GameTools.button(str(lane + 1), ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 66, ThemeKit.TEAL)
        button.pressed.connect(_answer.bind(lane, button))
        lanes.add_child(button)
    root.add_child(GameTools.label(I18n.t("catch_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    target_lane = rng.randi_range(0, 3)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("catch_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    stage.start_drop(target_lane)

func _answer(lane: int, button: Button) -> void:
    if locked:
        return
    locked = true
    GameTools.animate_press(button)
    if lane == target_lane:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("catch_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        mistakes += 1
        AudioDirector.bad()
        status.text = I18n.t("catch_wrong")
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
