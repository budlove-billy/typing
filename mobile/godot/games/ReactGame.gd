extends Control

signal finished(result: Dictionary)

const ROUNDS := 5

var arena: Button
var status: Label
var round_label: Label
var completed_rounds := 0
var total_ms := 0
var go_started_at := 0
var waiting_for_go := false
var can_tap := false
var rng := RandomNumberGenerator.new()
var round_token := 0

func _ready() -> void:
	rng.randomize()
	_build()
	_start_round()

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
	intro_box.add_child(_label("FOCUS  |  REACTION", 10, ThemeKit.AMBER))
	intro_box.add_child(_label(I18n.t("react_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))

	var state_row := HBoxContainer.new()
	state_row.alignment = BoxContainer.ALIGNMENT_CENTER
	state_row.add_theme_constant_override("separation", 8)
	root.add_child(state_row)
	status = _label(I18n.t("react_wait"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
	status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	state_row.add_child(status)
	round_label = _pill("01 / 05", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
	state_row.add_child(round_label)

	arena = Button.new()
	arena.custom_minimum_size = Vector2(0, 350)
	arena.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	arena.size_flags_vertical = Control.SIZE_EXPAND_FILL
	arena.add_theme_font_size_override("font_size", 32)
	arena.add_theme_color_override("font_color", ThemeKit.AMBER)
	arena.add_theme_color_override("font_hover_color", ThemeKit.AMBER)
	arena.pressed.connect(_arena_pressed)
	root.add_child(arena)
	root.add_child(_label("WAIT FOR BLUE  |  TAP ONCE", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _start_round() -> void:
	round_token += 1
	var token := round_token
	waiting_for_go = true
	can_tap = false
	arena.text = I18n.t("react_wait")
	arena.add_theme_color_override("font_color", ThemeKit.AMBER)
	arena.add_theme_color_override("font_hover_color", ThemeKit.AMBER)
	arena.add_theme_stylebox_override("normal", ThemeKit.button_style(ThemeKit.AMBER_SOFT, 26, Color("#f2d59c")))
	arena.add_theme_stylebox_override("hover", ThemeKit.button_style(Color("#fff7e7"), 26, Color("#e7bd64")))
	arena.add_theme_stylebox_override("pressed", ThemeKit.button_style(Color("#ffebc4"), 26, ThemeKit.AMBER))
	status.text = I18n.t("react_ready")
	round_label.text = "%02d / %02d" % [completed_rounds + 1, ROUNDS]
	var delay := 0.75 + rng.randf_range(0.35, 1.25)
	await get_tree().create_timer(delay).timeout
	if token != round_token:
		return
	waiting_for_go = false
	can_tap = true
	go_started_at = Time.get_ticks_msec()
	arena.text = I18n.t("react_go")
	arena.add_theme_color_override("font_color", Color.WHITE)
	arena.add_theme_color_override("font_hover_color", Color.WHITE)
	arena.add_theme_stylebox_override("normal", ThemeKit.button_style(ThemeKit.BLUE, 26, ThemeKit.BLUE_DARK))
	arena.add_theme_stylebox_override("hover", ThemeKit.button_style(ThemeKit.BLUE_DARK, 26, ThemeKit.BLUE_DARK))
	arena.add_theme_stylebox_override("pressed", ThemeKit.button_style(ThemeKit.BLUE_DARK, 26, ThemeKit.BLUE_DARK))
	status.text = I18n.t("react_go")

func _arena_pressed() -> void:
	if waiting_for_go:
		AudioDirector.bad()
		round_token += 1
		waiting_for_go = false
		can_tap = false
		completed_rounds += 1
		total_ms += 700
		status.text = I18n.t("react_false")
		if completed_rounds >= ROUNDS:
			_finish()
		else:
			await get_tree().create_timer(0.55).timeout
			_start_round()
		return
	if not can_tap:
		return
	AudioDirector.good()
	can_tap = false
	round_token += 1
	var reaction_ms := maxi(1, Time.get_ticks_msec() - go_started_at)
	completed_rounds += 1
	total_ms += reaction_ms
	status.text = str(reaction_ms) + " " + I18n.t("react_ms")
	if completed_rounds >= ROUNDS:
		_finish()
	else:
		await get_tree().create_timer(0.55).timeout
		_start_round()

func _finish() -> void:
	var average := int(round(float(total_ms) / float(ROUNDS)))
	var score := clampi(1100 - average, 100, 1000)
	finished.emit({"score": score, "detail": str(average) + " " + I18n.t("react_ms")})

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
