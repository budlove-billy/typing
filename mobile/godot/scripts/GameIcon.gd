class_name GameIcon
extends Control

var tint := ThemeKit.BLUE
var symbol := "✦"
var icon_size := 48
var symbol_label: Label

func configure(next_symbol: String, next_tint: Color, next_size: int = 48) -> GameIcon:
	symbol = next_symbol
	tint = next_tint
	icon_size = next_size
	custom_minimum_size = Vector2(icon_size, icon_size)
	size = Vector2(icon_size, icon_size)
	queue_redraw()
	return self

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	symbol_label = Label.new()
	symbol_label.text = symbol
	symbol_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	symbol_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	symbol_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	symbol_label.add_theme_font_size_override("font_size", maxi(18, int(icon_size * 0.43)))
	symbol_label.add_theme_color_override("font_color", tint.darkened(0.2))
	symbol_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(symbol_label)

func _draw() -> void:
	var outer := ThemeKit.box(tint.lightened(0.46), 17, tint.lightened(0.18), 1, false)
	draw_style_box(outer, Rect2(Vector2.ZERO, Vector2(icon_size, icon_size)))
	draw_circle(Vector2(icon_size * 0.5, icon_size * 0.48), icon_size * 0.29, Color(tint.r, tint.g, tint.b, 0.13))
