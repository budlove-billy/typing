class_name MallowAvatar
extends Control

var mood := "idle":
	set(value):
		mood = value
		queue_redraw()

var backdrop_color := Color.TRANSPARENT:
	set(value):
		backdrop_color = value
		queue_redraw()

func _ready() -> void:
	if custom_minimum_size == Vector2.ZERO:
		custom_minimum_size = Vector2(72, 72)
	mouse_filter = Control.MOUSE_FILTER_IGNORE

func _draw() -> void:
	var extent := minf(size.x, size.y)
	var pad := extent * 0.10
	var body_rect := Rect2(
		Vector2((size.x - extent) * 0.5 + pad, (size.y - extent) * 0.5 + pad * 1.15),
		Vector2(extent - pad * 2.0, extent - pad * 2.25)
	)
	var radius := maxi(8, int(extent * 0.22))
	draw_style_box(ThemeKit.box(Color("#ffd5b2"), radius), body_rect)

	var center := body_rect.get_center()
	var body_radius := body_rect.size.x * 0.5
	draw_circle(center + Vector2(-body_radius * 0.27, -body_radius * 0.28), body_radius * 0.33, Color(1, 0.91, 0.82, 0.72))
	if backdrop_color.a > 0.01:
		var bite_radius := extent * 0.075
		var bite_origin := body_rect.position + Vector2(body_rect.size.x * 0.93, body_rect.size.y * 0.13)
		draw_circle(bite_origin + Vector2(0, -bite_radius * 0.8), bite_radius, backdrop_color)
		draw_circle(bite_origin + Vector2(bite_radius * 0.65, bite_radius * 0.45), bite_radius, backdrop_color)
		draw_circle(bite_origin + Vector2(-bite_radius * 0.28, bite_radius * 0.72), bite_radius, backdrop_color)

	var eye_y := -body_radius * 0.08
	var eye_gap := body_radius * 0.38
	var eye_radius := maxf(1.8, extent * 0.035)
	if mood == "miss":
		draw_line(center + Vector2(-eye_gap - eye_radius, eye_y - eye_radius), center + Vector2(-eye_gap + eye_radius, eye_y + eye_radius), Color("#46506a"), maxf(1.5, extent * 0.032))
		draw_line(center + Vector2(eye_gap - eye_radius, eye_y + eye_radius), center + Vector2(eye_gap + eye_radius, eye_y - eye_radius), Color("#46506a"), maxf(1.5, extent * 0.032))
	else:
		draw_circle(center + Vector2(-eye_gap, eye_y), eye_radius, Color("#46506a"))
		draw_circle(center + Vector2(eye_gap, eye_y), eye_radius, Color("#46506a"))
	draw_circle(center + Vector2(-body_radius * 0.62, body_radius * 0.23), extent * 0.038, Color(0.95, 0.43, 0.52, 0.38))
	draw_circle(center + Vector2(body_radius * 0.62, body_radius * 0.23), extent * 0.038, Color(0.95, 0.43, 0.52, 0.38))
	if mood == "win" or mood == "good":
		draw_arc(center + Vector2(0, body_radius * 0.13), body_radius * 0.24, 0.15, PI - 0.15, 12, Color("#df6d79"), maxf(1.5, extent * 0.032))
	elif mood == "miss":
		draw_arc(center + Vector2(0, body_radius * 0.34), body_radius * 0.18, PI + 0.2, TAU - 0.2, 12, Color("#df6d79"), maxf(1.5, extent * 0.032))
	else:
		draw_line(center + Vector2(-body_radius * 0.14, body_radius * 0.23), center + Vector2(body_radius * 0.14, body_radius * 0.23), Color("#df6d79"), maxf(1.5, extent * 0.032))
