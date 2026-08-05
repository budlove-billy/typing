class_name MallowAvatar
extends Control

var mood := "idle":
	set(value):
		mood = value
		queue_redraw()

func _ready() -> void:
	if custom_minimum_size == Vector2.ZERO:
		custom_minimum_size = Vector2(72, 72)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _draw() -> void:
	var extent := minf(size.x, size.y)
	if extent <= 2.0:
		return
	var center := Vector2(size.x * 0.5, size.y * 0.54)
	var radius_x := extent * 0.37
	var radius_y := extent * 0.34
	var blob := PackedVector2Array()
	for i in range(32):
		var angle := TAU * float(i) / 32.0
		var wobble := 1.0 + 0.045 * sin(angle * 3.0 + 0.6)
		var point := center + Vector2(cos(angle) * radius_x * wobble, sin(angle) * radius_y * wobble)
		blob.append(point)
	var outline := blob.duplicate()
	outline.append(blob[0])

	# A soft ground shadow keeps the character anchored without adding a head cutout.
	draw_slime_ellipse(center + Vector2(0, radius_y * 1.08), radius_x * 0.64, extent * 0.055, Color(0.10, 0.24, 0.28, 0.12))
	draw_colored_polygon(blob, Color("#9ce6c8"))
	draw_polyline(outline, Color("#5bc19d"), maxf(1.4, extent * 0.025), true)

	# Slime bumps and a glossy highlight make the silhouette feel soft and alive.
	draw_circle(center + Vector2(-radius_x * 0.26, -radius_y * 0.86), radius_x * 0.18, Color("#9ce6c8"))
	draw_circle(center + Vector2(radius_x * 0.08, -radius_y * 0.98), radius_x * 0.14, Color("#a8ebd1"))
	draw_circle(center + Vector2(-radius_x * 0.30, -radius_y * 0.35), radius_x * 0.28, Color(0.88, 1.0, 0.95, 0.72))

	var eye_offset_y := -radius_y * 0.08
	var eye_gap := radius_x * 0.38
	var eye_radius := maxf(1.8, extent * 0.035)
	var ink := Color("#2f5060")
	if mood == "miss":
		draw_line(center + Vector2(-eye_gap - eye_radius, eye_offset_y - eye_radius), center + Vector2(-eye_gap + eye_radius, eye_offset_y + eye_radius), ink, maxf(1.5, extent * 0.032))
		draw_line(center + Vector2(eye_gap - eye_radius, eye_offset_y + eye_radius), center + Vector2(eye_gap + eye_radius, eye_offset_y - eye_radius), ink, maxf(1.5, extent * 0.032))
	else:
		draw_circle(center + Vector2(-eye_gap, eye_offset_y), eye_radius, ink)
		draw_circle(center + Vector2(eye_gap, eye_offset_y), eye_radius, ink)
		draw_circle(center + Vector2(-eye_gap - eye_radius * 0.3, eye_offset_y - eye_radius * 0.3), eye_radius * 0.32, Color.WHITE)
		draw_circle(center + Vector2(eye_gap - eye_radius * 0.3, eye_offset_y - eye_radius * 0.3), eye_radius * 0.32, Color.WHITE)

	draw_circle(center + Vector2(-radius_x * 0.62, radius_y * 0.25), extent * 0.038, Color(0.95, 0.42, 0.57, 0.40))
	draw_circle(center + Vector2(radius_x * 0.62, radius_y * 0.25), extent * 0.038, Color(0.95, 0.42, 0.57, 0.40))
	if mood == "win" or mood == "good":
		draw_arc(center + Vector2(0, radius_y * 0.15), radius_x * 0.24, 0.15, PI - 0.15, 12, Color("#dd6f82"), maxf(1.5, extent * 0.032))
	elif mood == "miss":
		draw_arc(center + Vector2(0, radius_y * 0.33), radius_x * 0.18, PI + 0.2, TAU - 0.2, 12, Color("#dd6f82"), maxf(1.5, extent * 0.032))
	else:
		draw_line(center + Vector2(-radius_x * 0.14, radius_y * 0.25), center + Vector2(radius_x * 0.14, radius_y * 0.25), Color("#dd6f82"), maxf(1.5, extent * 0.032))

func draw_slime_ellipse(center: Vector2, radius_x: float, radius_y: float, color: Color) -> void:
	var points := PackedVector2Array()
	for i in range(24):
		var angle := TAU * float(i) / 24.0
		points.append(center + Vector2(cos(angle) * radius_x, sin(angle) * radius_y))
	draw_colored_polygon(points, color)
