extends Control

signal finished(result: Dictionary)

var status: Label
var stage: TraceStage

func _ready() -> void:
	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 14)
	root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	add_child(root)
	root.add_child(_label(I18n.t("trace_ready"), 16, Color("#66738f"), HORIZONTAL_ALIGNMENT_CENTER))
	status = _label(I18n.t("tap_start"), 14, Color("#22a77a"), HORIZONTAL_ALIGNMENT_CENTER)
	root.add_child(status)
	stage = TraceStage.new()
	stage.custom_minimum_size = Vector2(0, 430)
	stage.size_flags_vertical = Control.SIZE_EXPAND_FILL
	stage.finished.connect(_stage_finished)
	root.add_child(stage)
	root.add_child(_label("Touch  ·  follow the soft line", 12, Color("#98a3b8"), HORIZONTAL_ALIGNMENT_CENTER))

func _stage_finished(success: bool, accuracy: int) -> void:
	if not success:
		AudioDirector.bad()
		status.text = I18n.t("trace_short")
		return
	AudioDirector.good()
	status.text = I18n.t("trace_good")
	finished.emit({"score": accuracy, "detail": str(accuracy) + "% accuracy"})

func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = align
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
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
		draw_style_box(ThemeKit.box(Color("#f8fbff"), 22, Color("#dbe5f2"), 1, false), Rect2(Vector2.ZERO, size))
		if path.size() > 1:
			draw_polyline(path, Color("#c9d5ec"), 18.0, true)
			draw_polyline(path, Color("#ffffff"), 8.0, true)
		if trail.size() > 1:
			draw_polyline(trail, Color("#22a77a"), 13.0, true)
		if not path.is_empty():
			draw_circle(path[0], 21.0, Color("#22a77a"))
			draw_circle(path[0], 9.0, Color.WHITE)
			draw_circle(path[path.size() - 1], 24.0, Color("#4f7cff"))
			draw_circle(path[path.size() - 1], 10.0, Color.WHITE)
