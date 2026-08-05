extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const ROUNDS := 8

var stage: RunStage
var status: Label
var round_label: Label
var round_index := 0
var correct_count := 0
var mistakes := 0
var total_ms := 0
var started_at := 0
var locked := false
var rng := RandomNumberGenerator.new()

class RunStage extends Control:
    signal obstacle_reached
    var progress := 0.0
    var active := false

    func _ready() -> void:
        mouse_filter = Control.MOUSE_FILTER_IGNORE
        set_process(true)

    func start_run() -> void:
        progress = 0.0
        active = true
        queue_redraw()

    func _process(delta: float) -> void:
        if not active:
            return
        progress += delta * 0.58
        if progress >= 1.0:
            active = false
            obstacle_reached.emit()
        queue_redraw()

    func _draw() -> void:
        if size.x < 20.0 or size.y < 20.0:
            return
        var panel_rect := Rect2(Vector2(6, 8), size - Vector2(12, 14))
        draw_style_box(ThemeKit.box(Color.WHITE, 26, Color("#e4e9f3"), 1, true), panel_rect)
        var ground_y := size.y - 78.0
        draw_line(Vector2(26, ground_y), Vector2(size.x - 26, ground_y), Color("#c9d5ff"), 5, true)
        for x in range(0, int(size.x), 42):
            draw_line(Vector2(x, ground_y + 12), Vector2(x + 18, ground_y + 12), Color("#e8ecf6"), 2, true)
        var obstacle_x := lerpf(size.x - 58.0, 122.0, minf(progress, 1.0))
        draw_style_box(ThemeKit.box(ThemeKit.PINK, 12), Rect2(obstacle_x, ground_y - 48, 28, 48))
        var jump := 0.0
        if active and progress > 0.64 and progress < 0.93:
            jump = sin((progress - 0.64) / 0.29 * PI) * 46.0
        var player := Vector2(92, ground_y - 29 - jump)
        draw_circle(player, 25, Color("#95e3c6"))
        draw_circle(player + Vector2(-9, -6), 5, ThemeKit.INK)
        draw_circle(player + Vector2(9, -6), 5, ThemeKit.INK)
        draw_line(player + Vector2(-8, 9), player + Vector2(8, 9), ThemeKit.PINK, 4, true)

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
    intro_box.add_child(GameTools.label("SPEED  |  RUN", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("run_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("run_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 08", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    stage = RunStage.new()
    stage.custom_minimum_size = Vector2(0, 300)
    stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
    stage.obstacle_reached.connect(_timeout)
    root.add_child(stage)
    var jump := GameTools.button(I18n.t("run_jump"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, 82, ThemeKit.BLUE)
    jump.pressed.connect(_jump.bind(jump))
    root.add_child(jump)
    root.add_child(GameTools.label(I18n.t("run_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("run_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    started_at = Time.get_ticks_msec()
    stage.start_run()

func _jump(button: Button) -> void:
    if locked or not stage.active:
        return
    locked = true
    GameTools.animate_press(button)
    total_ms += maxi(1, Time.get_ticks_msec() - started_at)
    var good_window := stage.progress >= 0.60 and stage.progress <= 0.94
    if good_window:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("run_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        mistakes += 1
        AudioDirector.bad()
        status.text = I18n.t("run_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    stage.active = false
    await get_tree().create_timer(0.34).timeout
    _advance()

func _timeout() -> void:
    if locked:
        return
    locked = true
    mistakes += 1
    AudioDirector.bad()
    status.text = I18n.t("run_wrong")
    status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.34).timeout
    _advance()

func _advance() -> void:
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var accuracy := float(correct_count) / float(ROUNDS)
    var score := clampi(int(round(accuracy * 1000.0 - float(mistakes) * 16.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %d misses" % [correct_count, ROUNDS, mistakes]})
