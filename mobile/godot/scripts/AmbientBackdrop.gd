class_name AmbientBackdrop
extends Control

var time := 0.0

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	set_process(true)

func _process(delta: float) -> void:
	time += delta
	queue_redraw()

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), ThemeKit.BACKGROUND)
	var drift := sin(time * 0.18) * 16.0
	draw_circle(Vector2(size.x * 0.08 + drift, size.y * 0.12), size.x * 0.34, Color(0.30, 0.44, 1.0, 0.035))
	draw_circle(Vector2(size.x * 0.94 - drift * 0.6, size.y * 0.52), size.x * 0.28, Color(0.12, 0.62, 0.47, 0.028))
	draw_circle(Vector2(size.x * 0.45, size.y * 0.96 + sin(time * 0.22) * 10.0), size.x * 0.30, Color(0.95, 0.42, 0.57, 0.022))
	for i in range(7):
		var phase := time * (0.25 + float(i) * 0.018) + float(i) * 1.7
		var x := fposmod(float(i) * 73.0 + sin(phase) * 18.0, maxf(size.x, 1.0))
		var y := fposmod(float(i) * 119.0 - time * (2.0 + float(i) * 0.4), maxf(size.y, 1.0))
		var alpha := 0.07 + sin(phase * 1.7) * 0.025
		draw_circle(Vector2(x, y), 2.0 + float(i % 2), Color(0.30, 0.44, 1.0, alpha))
