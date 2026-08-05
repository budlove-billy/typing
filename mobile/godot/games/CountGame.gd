extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")

const ROUNDS := 5

var stage: CountStage
var status: Label
var round_label: Label
var answer_grid: GridContainer
var answer_buttons: Array[Button] = []
var rng := RandomNumberGenerator.new()
var current_answer := 0
var correct_count := 0
var round_index := 0
var answered := false


class CountStage extends Control:
    signal sequence_done

    var events: Array[int] = []
    var elapsed := 0.0
    var event_index := -1
    var running := false
    const EVENT_TIME := 0.46

    func _ready() -> void:
        mouse_filter = Control.MOUSE_FILTER_IGNORE
        set_process(true)

    func play_sequence(next_events: Array[int]) -> void:
        events = next_events.duplicate()
        elapsed = 0.0
        event_index = -1
        running = true
        queue_redraw()

    func _process(delta: float) -> void:
        if not running:
            return
        elapsed += delta
        event_index = mini(int(elapsed / EVENT_TIME), events.size() - 1)
        if elapsed >= float(events.size()) * EVENT_TIME + 0.25:
            running = false
            event_index = events.size() - 1
            sequence_done.emit()
        queue_redraw()

    func _draw() -> void:
        if size.x < 20.0 or size.y < 20.0:
            return
        var panel_rect := Rect2(Vector2(6, 8), size - Vector2(12, 14))
        draw_style_box(ThemeKit.box(Color.WHITE, 26, Color("#e4e9f3"), 1, true), panel_rect)
        var center := size * 0.5
        var house := Rect2(center + Vector2(-100, -24), Vector2(200, 132))
        draw_style_box(ThemeKit.box(Color("#e8f5ef"), 18, Color("#9ed9c3"), 2), house)
        draw_colored_polygon(PackedVector2Array([
            center + Vector2(-124, -24), center + Vector2(0, -112), center + Vector2(124, -24)
        ]), Color("#56b895"))
        draw_style_box(ThemeKit.box(Color("#4d8b79"), 12), Rect2(center + Vector2(-25, 36), Vector2(50, 72)))
        draw_circle(center + Vector2(0, 61), 4, Color("#d5f2e5"))
        draw_circle(center + Vector2(-138, 100), 22, Color("#edf1ff"))
        draw_circle(center + Vector2(138, 100), 22, Color("#ffebf0"))
        if not running and events.is_empty():
            return
        if running and event_index >= 0:
            var event_sign: int = events[event_index]
            var phase := fmod(elapsed, EVENT_TIME) / EVENT_TIME
            var start_x := -190.0 if event_sign > 0 else 190.0
            var end_x := -86.0 if event_sign > 0 else 86.0
            var person_x := lerpf(start_x, end_x, phase)
            _draw_person(center + Vector2(person_x, 93), Color("#4c6fff" if event_sign > 0 else "#f06f91"))
        elif not running:
            draw_string(ThemeDB.fallback_font, center + Vector2(-82, -134), "HIDDEN INSIDE", HORIZONTAL_ALIGNMENT_LEFT, -1, 10, ThemeKit.SUBTLE)

    func _draw_person(position: Vector2, color: Color) -> void:
        draw_circle(position + Vector2(0, -22), 10, Color("#172033"))
        draw_line(position + Vector2(0, -11), position + Vector2(0, 16), color, 8, true)
        draw_line(position + Vector2(-2, 2), position + Vector2(-14, 18), color, 6, true)
        draw_line(position + Vector2(2, 2), position + Vector2(14, 18), color, 6, true)


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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.PINK_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("MEMORY  |  TRACK THE FLOW", 10, ThemeKit.PINK))
    intro_box.add_child(GameTools.label(I18n.t("count_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))

    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("count_watch"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 05", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)

    stage = CountStage.new()
    stage.custom_minimum_size = Vector2(0, 300)
    stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
    stage.sequence_done.connect(_sequence_done)
    root.add_child(stage)
    answer_grid = GridContainer.new()
    answer_grid.columns = 3
    answer_grid.add_theme_constant_override("h_separation", 8)
    answer_grid.add_theme_constant_override("v_separation", 8)
    root.add_child(answer_grid)
    for value in range(9):
        var answer: Button = GameTools.button(str(value), ThemeKit.BLUE_SOFT, ThemeKit.BLUE_DARK, 55, ThemeKit.BLUE)
        answer.pressed.connect(_answer.bind(value, answer))
        answer_grid.add_child(answer)
        answer_buttons.append(answer)

func _new_round() -> void:
    answered = false
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("count_watch")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    for button in answer_buttons:
        button.disabled = true
    var inside := 0
    var events: Array[int] = []
    var target := rng.randi_range(1, 6)
    while events.size() < rng.randi_range(5, 8) or inside != target:
        var sign := 1 if rng.randi_range(0, 1) == 0 else -1
        if inside == 0:
            sign = 1
        if events.size() >= 7 and inside != target:
            sign = 1 if inside < target else -1
        if inside + sign < 0 or inside + sign > 7:
            continue
        inside += sign
        events.append(sign)
        if events.size() >= 9 and inside == target:
            break
    current_answer = inside
    stage.play_sequence(events)

func _sequence_done() -> void:
    status.text = I18n.t("count_question")
    for button in answer_buttons:
        button.disabled = false

func _answer(value: int, button: Button) -> void:
    if answered:
        return
    answered = true
    GameTools.animate_press(button)
    var is_correct := value == current_answer
    if is_correct:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("count_correct")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("count_wrong") + "  " + str(current_answer)
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.45).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct_count, ROUNDS]})
