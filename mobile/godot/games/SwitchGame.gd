extends Control

signal finished(result: Dictionary)

const ROUNDS := 6
const SHAPE_RULE := 0
const COLOR_RULE := 1

var status: Label
var round_label: Label
var rule_label: Label
var stimulus: StimulusTile
var answer_buttons: Array[Button] = []
var round_index := 0
var correct_count := 0
var total_ms := 0
var round_started_at := 0
var locked := false
var rule_mode := SHAPE_RULE
var current_shape := "circle"
var current_color := "blue"
var rng := RandomNumberGenerator.new()


class StimulusTile extends Control:
    var shape_name := "circle"
    var color_name := "blue"
    var feedback_strength := 0.0
    var feedback_color := Color.TRANSPARENT
    var pulse := 0.0

    func _ready() -> void:
        mouse_filter = Control.MOUSE_FILTER_IGNORE
        set_process(true)

    func set_stimulus(next_shape: String, next_color: String) -> void:
        shape_name = next_shape
        color_name = next_color
        feedback_strength = 0.0
        feedback_color = Color.TRANSPARENT
        queue_redraw()

    func set_feedback(success: bool) -> void:
        feedback_color = ThemeKit.TEAL if success else ThemeKit.PINK
        feedback_strength = 1.0
        queue_redraw()

    func _process(delta: float) -> void:
        pulse += delta
        feedback_strength = move_toward(feedback_strength, 0.0, delta * 3.2)
        queue_redraw()

    func _draw() -> void:
        if size.x < 10.0 or size.y < 10.0:
            return
        var panel_rect := Rect2(Vector2(7, 9), size - Vector2(14, 14))
        draw_style_box(ThemeKit.box(Color(0.06, 0.1, 0.22, 0.10), 34), panel_rect)
        var surface_rect := Rect2(Vector2(7, 4), size - Vector2(14, 14))
        draw_style_box(ThemeKit.box(Color.WHITE, 34, Color("#e4e9f3"), 1), surface_rect)
        var center := size * 0.5 + Vector2(0, 2)
        var accent := Color("#4c6fff") if color_name == "blue" else Color("#f06f91")
        var glow_alpha := 0.13 + sin(pulse * 2.5) * 0.025
        draw_circle(center, min(size.x, size.y) * 0.29, Color(accent, glow_alpha))
        var scale_factor := 1.0 + sin(pulse * 3.0) * 0.018 + feedback_strength * 0.045
        var shape_size: float = min(size.x, size.y) * 0.22 * scale_factor
        draw_circle(center + Vector2(0, 8), shape_size + 7, Color(0.08, 0.12, 0.25, 0.12))
        if shape_name == "circle":
            draw_circle(center, shape_size, accent)
            draw_circle(center + Vector2(-shape_size * 0.30, -shape_size * 0.34), shape_size * 0.20, Color(1, 1, 1, 0.46))
        else:
            var square_rect := Rect2(center - Vector2(shape_size, shape_size), Vector2(shape_size, shape_size) * 2.0)
            draw_style_box(ThemeKit.box(accent, 22), square_rect)
            draw_circle(center + Vector2(-shape_size * 0.32, -shape_size * 0.36), shape_size * 0.18, Color(1, 1, 1, 0.44))
        if feedback_strength > 0.0:
            draw_style_box(ThemeKit.box(Color(feedback_color, feedback_strength * 0.16), 34, Color(feedback_color, feedback_strength * 0.7), 2), surface_rect)


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
    intro_box.add_child(_label("FOCUS  |  FLEXIBILITY", 10, ThemeKit.TEAL))
    intro_box.add_child(_label(I18n.t("switch_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))

    var state_row := HBoxContainer.new()
    state_row.add_theme_constant_override("separation", 8)
    root.add_child(state_row)
    status = _label(I18n.t("switch_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    state_row.add_child(status)
    round_label = _pill("01 / 06", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    state_row.add_child(round_label)

    var rule_card := PanelContainer.new()
    rule_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 18, 12, false))
    root.add_child(rule_card)
    var rule_box := VBoxContainer.new()
    rule_box.add_theme_constant_override("separation", 3)
    rule_card.add_child(rule_box)
    rule_box.add_child(_label("RULE  |  FOLLOW THE CUE", 10, ThemeKit.BLUE))
    rule_label = _label("", 16, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true)
    rule_box.add_child(rule_label)

    stimulus = StimulusTile.new()
    stimulus.custom_minimum_size = Vector2(0, 270)
    stimulus.size_flags_vertical = Control.SIZE_EXPAND_FILL
    stimulus.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    root.add_child(stimulus)

    var answers := HBoxContainer.new()
    answers.add_theme_constant_override("separation", 10)
    root.add_child(answers)
    var left := _answer_button(I18n.t("switch_left"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, ThemeKit.BLUE_DARK)
    var right := _answer_button(I18n.t("switch_right"), ThemeKit.PINK_SOFT, ThemeKit.PINK, Color("#c84e72"))
    left.pressed.connect(_answer.bind(true))
    right.pressed.connect(_answer.bind(false))
    answers.add_child(left)
    answers.add_child(right)
    answer_buttons = [left, right]
    root.add_child(_label("LEFT  /  RIGHT  •  TAP ONE ANSWER", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))


func _new_round() -> void:
    if round_index >= ROUNDS:
        _finish()
        return
    locked = false
    rule_mode = COLOR_RULE if (round_index / 2) % 2 == 1 else SHAPE_RULE
    current_shape = "circle" if rng.randi_range(0, 1) == 0 else "square"
    current_color = "blue" if rng.randi_range(0, 1) == 0 else "pink"
    stimulus.set_stimulus(current_shape, current_color)
    if rule_mode == SHAPE_RULE:
        rule_label.text = I18n.t("switch_shape_rule")
        rule_label.add_theme_color_override("font_color", ThemeKit.BLUE_DARK)
    else:
        rule_label.text = I18n.t("switch_color_rule")
        rule_label.add_theme_color_override("font_color", ThemeKit.PINK)
    status.text = I18n.t("switch_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    round_started_at = Time.get_ticks_msec()
    var entry := create_tween()
    stimulus.modulate = Color(1, 1, 1, 0.4)
    stimulus.scale = Vector2(0.96, 0.96)
    stimulus.pivot_offset = stimulus.size * 0.5
    entry.set_parallel(true)
    entry.tween_property(stimulus, "modulate", Color.WHITE, 0.22).set_trans(Tween.TRANS_SINE)
    entry.tween_property(stimulus, "scale", Vector2.ONE, 0.28).set_trans(Tween.TRANS_BACK)


func _answer(is_left: bool) -> void:
    if locked:
        return
    locked = true
    var elapsed := maxi(1, Time.get_ticks_msec() - round_started_at)
    total_ms += elapsed
    var expected_left := current_shape == "circle" if rule_mode == SHAPE_RULE else current_color == "blue"
    var is_correct := is_left == expected_left
    var chosen: Button = answer_buttons[0] if is_left else answer_buttons[1]
    chosen.pivot_offset = chosen.size * 0.5
    var tap_tween := create_tween()
    tap_tween.tween_property(chosen, "scale", Vector2(0.96, 0.96), 0.07).set_trans(Tween.TRANS_SINE)
    tap_tween.tween_property(chosen, "scale", Vector2(1.03, 1.03), 0.10).set_trans(Tween.TRANS_BACK)
    tap_tween.tween_property(chosen, "scale", Vector2.ONE, 0.16).set_trans(Tween.TRANS_SINE)
    stimulus.set_feedback(is_correct)
    if is_correct:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("switch_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("switch_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.42).timeout
    round_index += 1
    _new_round()


func _finish() -> void:
    var accuracy := float(correct_count) / float(ROUNDS)
    var average_ms := float(total_ms) / float(ROUNDS)
    var speed := clampf(1.0 - (average_ms - 250.0) / 900.0, 0.0, 1.0)
    var score := clampi(int(round(accuracy * 650.0 + speed * 350.0)), 100, 1000)
    finished.emit({
        "score": score,
        "detail": "%d/%d · %dms %s" % [correct_count, ROUNDS, int(round(average_ms)), I18n.t("switch_round")]
    })


func _answer_button(text_value: String, fill: Color, ink: Color, pressed_color: Color) -> Button:
    var button := Button.new()
    button.text = text_value
    button.custom_minimum_size = Vector2(0, 76)
    button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    button.add_theme_font_size_override("font_size", 18)
    button.add_theme_color_override("font_color", ink)
    button.add_theme_color_override("font_hover_color", ink)
    button.add_theme_color_override("font_pressed_color", Color.WHITE)
    button.add_theme_stylebox_override("normal", ThemeKit.button_style(fill, 22, Color(fill, 0.75)))
    button.add_theme_stylebox_override("hover", ThemeKit.button_style(Color.WHITE, 22, ink))
    button.add_theme_stylebox_override("pressed", ThemeKit.button_style(pressed_color, 22, pressed_color))
    button.add_theme_stylebox_override("focus", ThemeKit.button_style(fill, 22, ink))
    return button


func _pill(text_value: String, fill: Color, color: Color) -> Label:
    var label := _label(text_value, 12, color, HORIZONTAL_ALIGNMENT_CENTER)
    var style := ThemeKit.box(fill, 18)
    style.content_margin_left = 10
    style.content_margin_right = 10
    style.content_margin_top = 6
    style.content_margin_bottom = 6
    label.add_theme_stylebox_override("normal", style)
    return label


func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT, wrap: bool = false) -> Label:
    var label := Label.new()
    label.text = text_value
    label.add_theme_font_size_override("font_size", font_size)
    label.add_theme_color_override("font_color", color)
    label.horizontal_alignment = align
    if wrap:
        label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
        label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    else:
        label.autowrap_mode = TextServer.AUTOWRAP_OFF
    return label
