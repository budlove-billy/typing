class_name GameIcon
extends Control

var icon_key := "flash"
var tint := ThemeKit.BLUE
var icon_size := 48
var draw_surface := true

func configure(next_key: String, next_tint: Color, next_size: int = 48, next_surface: bool = true) -> GameIcon:
	icon_key = next_key
	tint = next_tint
	icon_size = next_size
	draw_surface = next_surface
	custom_minimum_size = Vector2(icon_size, icon_size)
	size = Vector2(icon_size, icon_size)
	queue_redraw()
	return self

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	queue_redraw()

func _draw() -> void:
	if draw_surface:
		var shadow := ThemeKit.box(Color(0.08, 0.12, 0.22, 0.09), 17)
		draw_style_box(shadow, Rect2(0, 2, icon_size, icon_size))
		var outer := ThemeKit.box(tint.lightened(0.43), 17, tint.lightened(0.18), 1, false)
		draw_style_box(outer, Rect2(0, 0, icon_size, icon_size))
		draw_circle(Vector2(icon_size * 0.34, icon_size * 0.28), icon_size * 0.20, Color(1, 1, 1, 0.22))

	var scale_factor := float(icon_size) / 48.0
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(scale_factor, scale_factor))
	var ink := tint.darkened(0.22) if draw_surface else tint
	var soft := tint.lightened(0.13) if draw_surface else tint.lightened(0.18)
	match icon_key:
		"flash", "cat_speed": _draw_bolt(ink)
		"count": _draw_people(ink)
		"nback": _draw_letter_stack("N", ink)
		"cards": _draw_cards(ink)
		"rev", "rotate": _draw_loop_arrow(ink)
		"stroop": _draw_palette(ink, soft)
		"switch": _draw_switch(ink)
		"flank", "cat_focus": _draw_target(ink)
		"trail": _draw_nodes(ink)
		"react": _draw_timer(ink)
		"chop": _draw_tower(ink, soft)
		"run": _draw_runner(ink)
		"whack": _draw_hammer(ink)
		"catch": _draw_basket(ink)
		"trace": _draw_pencil(ink)
		"melody": _draw_note(ink)
		"rhythm": _draw_drum(ink)
		"pitch", "cat_sound": _draw_headphones(ink)
		"spot": _draw_rainbow(ink, soft)
		"odd": _draw_magnifier(ink)
		"diff", "cat_sight": _draw_eyes(ink)
		"slide", "cat_space": _draw_cube(ink)
		"fit": _draw_blocks(ink)
		"math", "cat_calculation": _draw_divide(ink)
		"bubble": _draw_bubbles(ink)
		"merge": _draw_lollipop(ink)
		"guess", "nav_records": _draw_chart(ink)
		"iq", "cat_memory": _draw_brain(ink)
		"sudoku": _draw_grid(ink)
		"sort": _draw_tubes(ink)
		"nono": _draw_pixels(ink)
		"anagram", "cat_language": _draw_letters(ink)
		"wordsearch": _draw_word_search(ink)
		"moamoa", "cat_logic": _draw_puzzle(ink)
		"cat_daily": _draw_calendar(ink)
		"queens": _draw_crown(ink)
		"tango": _draw_sun_moon(ink)
		"braintype", "cat_test": _draw_crystal(ink)
		"cat_coordination": _draw_joystick(ink)
		"nav_home": _draw_house(ink)
		"nav_games": _draw_game_grid(ink)
		_: _draw_sparkle(ink)

func _draw_bolt(color: Color) -> void:
	draw_colored_polygon(PackedVector2Array([Vector2(27, 8), Vector2(15, 25), Vector2(23, 25), Vector2(19, 40), Vector2(34, 20), Vector2(26, 20)]), color)

func _draw_people(color: Color) -> void:
	draw_circle(Vector2(19, 18), 5, color)
	draw_circle(Vector2(30, 20), 4, color)
	draw_arc(Vector2(19, 34), 10, PI, TAU, 18, color, 4, true)
	draw_arc(Vector2(31, 34), 8, PI, TAU, 16, color, 3, true)

func _draw_letter_stack(text: String, color: Color) -> void:
	draw_rect(Rect2(12, 11, 24, 27), Color(color.r, color.g, color.b, 0.13), true)
	draw_rect(Rect2(12, 11, 24, 27), color, false, 2, true)
	_draw_text(text, 13, 32, 22, color)

func _draw_cards(color: Color) -> void:
	draw_rect(Rect2(10, 13, 19, 25), color, false, 3, true)
	draw_rect(Rect2(20, 9, 19, 26), color, false, 3, true)
	draw_circle(Vector2(30, 21), 3, color)

func _draw_loop_arrow(color: Color) -> void:
	draw_arc(Vector2(24, 25), 12, -2.7, 1.1, 22, color, 3, true)
	draw_colored_polygon(PackedVector2Array([Vector2(11, 18), Vector2(11, 29), Vector2(19, 24)]), color)

func _draw_palette(color: Color, accent: Color) -> void:
	draw_circle(Vector2(23, 24), 14, Color(color.r, color.g, color.b, 0.12))
	draw_arc(Vector2(23, 24), 14, 0, TAU, 24, color, 2.5, true)
	for point in [Vector2(18, 18), Vector2(27, 17), Vector2(16, 27)]:
		draw_circle(point, 2.4, accent)
	draw_circle(Vector2(29, 28), 4.5, ThemeKit.BACKGROUND)

func _draw_switch(color: Color) -> void:
	draw_line(Vector2(11, 17), Vector2(34, 17), color, 3, true)
	draw_colored_polygon(PackedVector2Array([Vector2(34, 12), Vector2(41, 17), Vector2(34, 22)]), color)
	draw_line(Vector2(37, 31), Vector2(14, 31), color, 3, true)
	draw_colored_polygon(PackedVector2Array([Vector2(14, 26), Vector2(7, 31), Vector2(14, 36)]), color)

func _draw_target(color: Color) -> void:
	for radius in [14.0, 9.0, 4.0]:
		draw_arc(Vector2(24, 24), radius, 0, TAU, 28, color, 2.3, true)
	draw_line(Vector2(24, 8), Vector2(24, 15), color, 2, true)
	draw_line(Vector2(33, 24), Vector2(40, 24), color, 2, true)

func _draw_nodes(color: Color) -> void:
	var points := PackedVector2Array([Vector2(13, 32), Vector2(22, 17), Vector2(35, 29)])
	draw_polyline(points, color, 3, true)
	for point in points:
		draw_circle(point, 4, color)
		draw_circle(point, 1.7, ThemeKit.BACKGROUND)

func _draw_timer(color: Color) -> void:
	draw_arc(Vector2(24, 26), 13, 0, TAU, 28, color, 3, true)
	draw_line(Vector2(24, 13), Vector2(24, 8), color, 3, true)
	draw_line(Vector2(19, 8), Vector2(29, 8), color, 3, true)
	draw_line(Vector2(24, 26), Vector2(31, 20), color, 3, true)
	draw_circle(Vector2(24, 26), 2, color)

func _draw_tower(color: Color, accent: Color) -> void:
	for i in range(3):
		draw_circle(Vector2(24, 12 + i * 11), 5, accent if i == 1 else color)
	draw_line(Vector2(24, 7), Vector2(24, 40), color, 2, true)

func _draw_runner(color: Color) -> void:
	draw_circle(Vector2(28, 12), 4, color)
	draw_line(Vector2(25, 18), Vector2(20, 28), color, 4, true)
	draw_line(Vector2(21, 22), Vector2(33, 24), color, 3, true)
	draw_line(Vector2(20, 28), Vector2(31, 37), color, 4, true)
	draw_line(Vector2(20, 28), Vector2(11, 37), color, 4, true)

func _draw_hammer(color: Color) -> void:
	draw_colored_polygon(PackedVector2Array([Vector2(16, 35), Vector2(21, 39), Vector2(34, 22), Vector2(29, 18)]), color)
	draw_colored_polygon(PackedVector2Array([Vector2(17, 10), Vector2(24, 7), Vector2(37, 18), Vector2(30, 24)]), color)

func _draw_basket(color: Color) -> void:
	draw_colored_polygon(PackedVector2Array([Vector2(11, 22), Vector2(37, 22), Vector2(33, 37), Vector2(15, 37)]), Color(color.r, color.g, color.b, 0.16))
	draw_polyline(PackedVector2Array([Vector2(11, 22), Vector2(15, 37), Vector2(33, 37), Vector2(37, 22)]), color, 3, true)
	draw_arc(Vector2(24, 24), 10, PI, TAU, 16, color, 2.5, true)

func _draw_pencil(color: Color) -> void:
	draw_colored_polygon(PackedVector2Array([Vector2(12, 33), Vector2(17, 38), Vector2(37, 18), Vector2(32, 13)]), color)
	draw_colored_polygon(PackedVector2Array([Vector2(10, 40), Vector2(12, 33), Vector2(17, 38)]), color)
	draw_line(Vector2(30, 15), Vector2(35, 20), ThemeKit.BACKGROUND, 2, true)

func _draw_note(color: Color) -> void:
	draw_line(Vector2(29, 10), Vector2(29, 32), color, 4, true)
	draw_line(Vector2(29, 11), Vector2(38, 14), color, 4, true)
	draw_circle(Vector2(23, 34), 6, color)

func _draw_drum(color: Color) -> void:
	draw_arc(Vector2(24, 20), 13, 0, TAU, 24, color, 3, true)
	draw_line(Vector2(11, 20), Vector2(14, 35), color, 3, true)
	draw_line(Vector2(37, 20), Vector2(34, 35), color, 3, true)
	draw_line(Vector2(14, 35), Vector2(34, 35), color, 3, true)
	draw_line(Vector2(13, 11), Vector2(34, 4), color, 2, true)

func _draw_headphones(color: Color) -> void:
	draw_arc(Vector2(24, 25), 14, PI, TAU, 24, color, 3.5, true)
	draw_rect(Rect2(8, 24, 6, 13), color, true)
	draw_rect(Rect2(34, 24, 6, 13), color, true)

func _draw_rainbow(color: Color, accent: Color) -> void:
	for i in range(3):
		draw_arc(Vector2(24, 34), 14 - i * 4, PI, TAU, 20, color if i != 1 else accent, 3, true)

func _draw_magnifier(color: Color) -> void:
	draw_arc(Vector2(21, 21), 10, 0, TAU, 24, color, 3, true)
	draw_line(Vector2(28, 29), Vector2(38, 39), color, 4, true)
	draw_colored_polygon(PackedVector2Array([Vector2(18, 17), Vector2(24, 19), Vector2(20, 25)]), color)

func _draw_eyes(color: Color) -> void:
	for x in [16.0, 32.0]:
		draw_arc(Vector2(x, 24), 9, -0.85, 0.85, 14, color, 2.5, true)
		draw_arc(Vector2(x, 24), 9, PI - 0.85, PI + 0.85, 14, color, 2.5, true)
		draw_circle(Vector2(x, 24), 2.5, color)

func _draw_cube(color: Color) -> void:
	var top := PackedVector2Array([Vector2(24, 9), Vector2(38, 17), Vector2(24, 25), Vector2(10, 17)])
	draw_polyline(PackedVector2Array([top[0], top[1], top[2], top[3], top[0]]), color, 2.5, true)
	draw_polyline(PackedVector2Array([Vector2(10, 17), Vector2(10, 32), Vector2(24, 40), Vector2(38, 32), Vector2(38, 17)]), color, 2.5, true)
	draw_line(Vector2(24, 25), Vector2(24, 40), color, 2.5, true)

func _draw_blocks(color: Color) -> void:
	for rect in [Rect2(9, 24, 10, 10), Rect2(19, 14, 10, 10), Rect2(19, 24, 10, 10), Rect2(29, 24, 10, 10)]:
		draw_rect(rect, color, false, 2.5, true)

func _draw_divide(color: Color) -> void:
	draw_circle(Vector2(24, 13), 3, color)
	draw_line(Vector2(12, 24), Vector2(36, 24), color, 3.5, true)
	draw_circle(Vector2(24, 35), 3, color)

func _draw_bubbles(color: Color) -> void:
	for bubble in [[17.0, 28.0, 8.0], [29.0, 19.0, 7.0], [33.0, 32.0, 4.5]]:
		draw_arc(Vector2(bubble[0], bubble[1]), bubble[2], 0, TAU, 20, color, 2.5, true)

func _draw_lollipop(color: Color) -> void:
	draw_arc(Vector2(23, 19), 10, 0, TAU, 24, color, 3, true)
	draw_arc(Vector2(23, 19), 5, -0.3, 4.5, 18, color, 2, true)
	draw_line(Vector2(29, 27), Vector2(37, 39), color, 3, true)

func _draw_chart(color: Color) -> void:
	for item in [[10.0, 29.0, 7.0], [20.0, 22.0, 14.0], [30.0, 14.0, 22.0]]:
		draw_rect(Rect2(item[0], item[1], 7, item[2]), color, true)

func _draw_brain(color: Color) -> void:
	for point in [Vector2(17, 17), Vector2(25, 14), Vector2(32, 19), Vector2(17, 28), Vector2(28, 29)]:
		draw_circle(point, 7, Color(color.r, color.g, color.b, 0.16))
	draw_arc(Vector2(24, 23), 14, 0, TAU, 30, color, 2.5, true)
	draw_line(Vector2(24, 11), Vector2(24, 36), color, 2, true)

func _draw_grid(color: Color) -> void:
	draw_rect(Rect2(10, 10, 28, 28), color, false, 2.5, true)
	for offset in [19.0, 29.0]:
		draw_line(Vector2(offset, 10), Vector2(offset, 38), color, 1.7, true)
		draw_line(Vector2(10, offset), Vector2(38, offset), color, 1.7, true)
	_draw_text("4", 19, 29, 12, color)

func _draw_tubes(color: Color) -> void:
	for x in [15.0, 28.0]:
		draw_line(Vector2(x, 10), Vector2(x, 31), color, 3, true)
		draw_arc(Vector2(x + 4, 31), 4, 0, PI, 12, color, 3, true)
		draw_line(Vector2(x + 8, 31), Vector2(x + 8, 10), color, 3, true)
		draw_line(Vector2(x - 2, 10), Vector2(x + 10, 10), color, 3, true)

func _draw_pixels(color: Color) -> void:
	for y in range(3):
		for x in range(3):
			if (x + y) % 2 == 0 or (x == 1 and y == 1):
				draw_rect(Rect2(13 + x * 8, 13 + y * 8, 6, 6), color, true)
	draw_rect(Rect2(10, 10, 28, 28), color, false, 2, true)

func _draw_letters(color: Color) -> void:
	_draw_text("A", 8, 31, 18, color)
	_draw_text("B", 23, 36, 14, color)
	draw_rect(Rect2(8, 11, 16, 22), color, false, 2, true)
	draw_rect(Rect2(24, 18, 15, 20), color, false, 2, true)

func _draw_word_search(color: Color) -> void:
	_draw_text("A", 10, 31, 18, color)
	draw_arc(Vector2(28, 24), 9, 0, TAU, 20, color, 2.5, true)
	draw_line(Vector2(34, 31), Vector2(40, 38), color, 3, true)

func _draw_puzzle(color: Color) -> void:
	draw_rect(Rect2(11, 12, 26, 25), color, false, 3, true)
	draw_circle(Vector2(24, 12), 4, ThemeKit.BACKGROUND)
	draw_arc(Vector2(24, 12), 4, 0, PI, 12, color, 2.5, true)
	draw_circle(Vector2(37, 25), 4, Color(color.r, color.g, color.b, 0.18))
	draw_arc(Vector2(37, 25), 4, -PI / 2.0, PI / 2.0, 12, color, 2.5, true)

func _draw_calendar(color: Color) -> void:
	draw_rect(Rect2(10, 13, 28, 25), color, false, 3, true)
	draw_line(Vector2(10, 21), Vector2(38, 21), color, 3, true)
	draw_line(Vector2(17, 9), Vector2(17, 17), color, 3, true)
	draw_line(Vector2(31, 9), Vector2(31, 17), color, 3, true)
	draw_rect(Rect2(17, 26, 5, 5), color, true)
	draw_rect(Rect2(27, 26, 5, 5), color, true)

func _draw_crown(color: Color) -> void:
	draw_colored_polygon(PackedVector2Array([Vector2(10, 16), Vector2(18, 25), Vector2(24, 12), Vector2(31, 25), Vector2(39, 16), Vector2(35, 35), Vector2(14, 35)]), Color(color.r, color.g, color.b, 0.20))
	draw_polyline(PackedVector2Array([Vector2(10, 16), Vector2(18, 25), Vector2(24, 12), Vector2(31, 25), Vector2(39, 16), Vector2(35, 35), Vector2(14, 35), Vector2(10, 16)]), color, 2.5, true)

func _draw_sun_moon(color: Color) -> void:
	draw_circle(Vector2(18, 24), 9, color)
	draw_circle(Vector2(31, 24), 10, Color(color.r, color.g, color.b, 0.16))
	draw_arc(Vector2(31, 24), 10, 0, TAU, 24, color, 2.5, true)
	draw_circle(Vector2(35, 20), 10, ThemeKit.BACKGROUND)

func _draw_crystal(color: Color) -> void:
	draw_circle(Vector2(24, 22), 11, Color(color.r, color.g, color.b, 0.16))
	draw_arc(Vector2(24, 22), 11, 0, TAU, 24, color, 2.5, true)
	_draw_sparkle(color, Vector2(26, 19), 5)
	draw_line(Vector2(15, 36), Vector2(33, 36), color, 3, true)

func _draw_joystick(color: Color) -> void:
	draw_arc(Vector2(24, 29), 13, PI, TAU, 20, color, 3, true)
	draw_line(Vector2(13, 29), Vector2(10, 37), color, 3, true)
	draw_line(Vector2(35, 29), Vector2(38, 37), color, 3, true)
	draw_line(Vector2(24, 25), Vector2(24, 12), color, 3, true)
	draw_circle(Vector2(24, 11), 4, color)

func _draw_house(color: Color) -> void:
	draw_colored_polygon(PackedVector2Array([Vector2(8, 23), Vector2(24, 9), Vector2(40, 23), Vector2(36, 23), Vector2(36, 39), Vector2(12, 39), Vector2(12, 23)]), Color(color.r, color.g, color.b, 0.18))
	draw_polyline(PackedVector2Array([Vector2(8, 23), Vector2(24, 9), Vector2(40, 23)]), color, 3, true)
	draw_polyline(PackedVector2Array([Vector2(12, 22), Vector2(12, 39), Vector2(36, 39), Vector2(36, 22)]), color, 3, true)
	draw_rect(Rect2(21, 28, 7, 11), color, true)

func _draw_game_grid(color: Color) -> void:
	for y in range(2):
		for x in range(2):
			draw_style_box(ThemeKit.box(Color(color.r, color.g, color.b, 0.16), 4, color, 2, false), Rect2(10 + x * 16, 10 + y * 16, 13, 13))

func _draw_sparkle(color: Color, center: Vector2 = Vector2(24, 24), radius: float = 11) -> void:
	var points := PackedVector2Array([
		center + Vector2(0, -radius), center + Vector2(radius * 0.25, -radius * 0.25),
		center + Vector2(radius, 0), center + Vector2(radius * 0.25, radius * 0.25),
		center + Vector2(0, radius), center + Vector2(-radius * 0.25, radius * 0.25),
		center + Vector2(-radius, 0), center + Vector2(-radius * 0.25, -radius * 0.25)
	])
	draw_colored_polygon(points, color)

func _draw_text(text: String, x: float, baseline: float, width: float, color: Color) -> void:
	var size_px := 20 if text.length() == 1 else 12
	draw_string(ThemeDB.fallback_font, Vector2(x, baseline), text, HORIZONTAL_ALIGNMENT_CENTER, width, size_px, color)
