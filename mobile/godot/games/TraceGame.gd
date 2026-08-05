extends Control

signal finished(result: Dictionary)

var status: Label
var stage: TraceStage

func _ready() -> void:
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
	intro_box.add_child(_label("COORDINATION  |  TRACE", 10, ThemeKit.TEAL, HORIZONTAL_ALIGNMENT_LEFT))
	intro_box.add_child(_label(I18n.t("trace_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))

	status = _pill(I18n.t("tap_start"), ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
	status.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	root.add_child(status)

	stage = TraceStage.new()
	stage.custom_minimum_size = Vector2(0, 470)
	stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stage.finished.connect(_stage_finished)
	root.add_child(stage)
	root.add_child(_label("PRESS START  |  FOLLOW THE PATH", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _stage_finished(success: bool, accuracy: int) -> void:
	if not success:
		AudioDirector.bad()
		status.text = I18n.t("trace_short")
		return
	AudioDirector.good()
	status.text = I18n.t("trace_good")
	finished.emit({"score": accuracy, "detail": str(accuracy) + "% accuracy"})

func _pill(text_value: String, fill: Color, color: Color) -> Label:
	var label := _label(text_value, 12, color, HORIZONTAL_ALIGNMENT_CENTER)
	var style := ThemeKit.box(fill, 18)
	style.content_margin_left = 12
	style.content_margin_right = 12
	style.content_margin_top = 6
	style.content_margin_bottom = 6
	label.add_theme_stylebox_override("normal", style)
	return label

func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment, wrap: bool = false) -> Label:
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

class TraceStage extends Control:
	signal finished(success: bool, accuracy: int)

	var path := PackedVector2Array()
	var trail := PackedVector2Array()
	var current_index := 0
	var drawing := false
	var completed := false

	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_STOP
		call_deferred("_make_path")

	func _notification(what: int) -> void:
		if what == NOTIFICATION_RESIZED and size.x > 20 and size.y > 20 and path.is_empty():
			_make_path()

	func _make_path() -> void:
		if size.x <= 20 or size.y <= 20:
			return
		path = PackedVector2Array([
			Vector2(size.x * 0.16, size.y * 0.78),
			Vector2(size.x * 0.22, size.y * 0.42),
			Vector2(size.x * 0.42, size.y * 0.20),
			Vector2(size.x * 0.70, size.y * 0.28),
			Vector2(size.x * 0.84, size.y * 0.58),
			Vector2(size.x * 0.72, size.y * 0.82)
		])
		queue_redraw()

	func _gui_input(event: InputEvent) -> void:
		if event is InputEventScreenTouch:
			if event.pressed:
				_begin(event.position)
			else:
				_end()
			accept_event()
		elif event is InputEventScreenDrag:
			_move(event.position)
			accept_event()
		elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
			if event.pressed:
				_begin(event.position)
			else:
				_end()
			accept_event()
		elif event is InputEventMouseMotion and drawing and event.button_mask & MOUSE_BUTTON_MASK_LEFT:
			_move(event.position)
			accept_event()

	func _begin(position: Vector2) -> void:
		if path.is_empty():
			_make_path()
		if path.is_empty() or position.distance_to(path[0]) > 48.0:
			return
		drawing = true
		completed = false
		current_index = 0
		trail = PackedVector2Array([position])
		queue_redraw()

	func _move(position: Vector2) -> void:
		if not drawing or path.is_empty():
			return
		trail.append(position)
		var nearest := _nearest_path_index(position)
		if nearest >= current_index:
			current_index = mini(path.size() - 1, nearest + 1)
		queue_redraw()
		if current_index >= path.size() - 1 and position.distance_to(path[path.size() - 1]) < 48.0:
			_end()

	func _end() -> void:
		if not drawing:
			return
		drawing = false
		var ratio := float(current_index) / float(maxi(1, path.size() - 1))
		if ratio >= 0.95:
			completed = true
			finished.emit(true, 820 + int(ratio * 180.0))
		else:
			finished.emit(false, int(ratio * 100.0))
		queue_redraw()

	func _nearest_path_index(position: Vector2) -> int:
		var best := 0
		var best_distance := INF
		for i in range(path.size()):
			var distance := position.distance_to(path[i])
			if distance < best_distance:
				best_distance = distance
				best = i
		return best if best_distance < 68.0 else current_index

	func _draw() -> void:
		draw_style_box(ThemeKit.box(Color("#f8fafc"), 22, Color("#dde4ef"), 1, false), Rect2(Vector2.ZERO, size))
		if path.size() > 1:
			draw_polyline(path, Color("#d3daea"), 20.0, true)
			draw_polyline(path, Color.WHITE, 10.0, true)
			for point in path:
				draw_circle(point, 4.0, Color("#c3ccdf"))
		if trail.size() > 1:
			draw_polyline(trail, ThemeKit.TEAL, 13.0, true)
		if not path.is_empty():
			draw_circle(path[0], 24.0, Color(0.12, 0.62, 0.47, 0.16))
			draw_circle(path[0], 17.0, ThemeKit.TEAL)
			draw_circle(path[0], 7.0, Color.WHITE)
			draw_circle(path[path.size() - 1], 27.0, Color(0.30, 0.44, 1.0, 0.16))
			draw_circle(path[path.size() - 1], 19.0, ThemeKit.BLUE)
			draw_circle(path[path.size() - 1], 8.0, Color.WHITE)
