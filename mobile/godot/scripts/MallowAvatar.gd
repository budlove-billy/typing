class_name MallowAvatar
extends Control

var mood := "idle":
	set(value):
		mood = value
		queue_redraw()

func _ready() -> void:
	custom_minimum_size = Vector2(88, 88)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _draw() -> void:
	var center := Vector2(size.x * 0.5, size.y * 0.54)
	var body_radius := minf(size.x, size.y) * 0.36
	var body_color := Color("#ffd3a8")
	draw_circle(center, body_radius, body_color)
	draw_circle(center + Vector2(-body_radius * 0.08, -body_radius * 0.12), body_radius * 0.86, Color("#ffe2c4"))
	var eye_y := center.y - body_radius * 0.12
	var eye_gap := body_radius * 0.38
	if mood == "miss":
		draw_line(center + Vector2(-eye_gap - 4, eye_y - 3), center + Vector2(-eye_gap + 4, eye_y + 3), Color("#4b4c63"), 3.0)
		draw_line(center + Vector2(eye_gap - 4, eye_y + 3), center + Vector2(eye_gap + 4, eye_y - 3), Color("#4b4c63"), 3.0)
	else:
		draw_circle(center + Vector2(-eye_gap, eye_y), 3.2, Color("#4b4c63"))
		draw_circle(center + Vector2(eye_gap, eye_y), 3.2, Color("#4b4c63"))
	if mood == "win" or mood == "good":
		draw_arc(center + Vector2(0, body_radius * 0.16), body_radius * 0.24, 0.15, PI - 0.15, 12, Color("#e8787d"), 3.0)
	elif mood == "miss":
		draw_arc(center + Vector2(0, body_radius * 0.34), body_radius * 0.18, PI + 0.2, TAU - 0.2, 12, Color("#e8787d"), 3.0)
	else:
		draw_line(center + Vector2(-body_radius * 0.14, body_radius * 0.25), center + Vector2(body_radius * 0.14, body_radius * 0.25), Color("#e8787d"), 3.0)
	# Mallow's small leaf-like top detail.
	var top := center + Vector2(0, -body_radius * 0.92)
	draw_colored_polygon(PackedVector2Array([top + Vector2(-10, 4), top + Vector2(0, -12), top + Vector2(10, 4)]), Color("#ff9f72"))
