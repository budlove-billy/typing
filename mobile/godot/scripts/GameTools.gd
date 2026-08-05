class_name GameTools
extends RefCounted

static func label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT, wrap: bool = false) -> Label:
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

static func pill(text_value: String, fill: Color, color: Color, font_size: int = 12) -> Label:
	var label := label(text_value, font_size, color, HORIZONTAL_ALIGNMENT_CENTER)
	var style := ThemeKit.box(fill, 18)
	style.content_margin_left = 10
	style.content_margin_right = 10
	style.content_margin_top = 6
	style.content_margin_bottom = 6
	label.add_theme_stylebox_override("normal", style)
	return label

static func button(text_value: String, fill: Color, ink: Color, min_height: int = 64, pressed_color: Color = Color.TRANSPARENT) -> Button:
	var button := Button.new()
	button.text = text_value
	button.custom_minimum_size = Vector2(0, min_height)
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.add_theme_font_size_override("font_size", 17)
	button.add_theme_color_override("font_color", ink)
	button.add_theme_color_override("font_hover_color", ink)
	button.add_theme_color_override("font_pressed_color", Color.WHITE if pressed_color != Color.TRANSPARENT else ink)
	var down := pressed_color if pressed_color != Color.TRANSPARENT else fill.darkened(0.08)
	button.add_theme_stylebox_override("normal", ThemeKit.button_style(fill, 20, Color(fill, 0.74)))
	button.add_theme_stylebox_override("hover", ThemeKit.button_style(fill.lightened(0.12), 20, ink))
	button.add_theme_stylebox_override("pressed", ThemeKit.button_style(down, 20, down))
	button.add_theme_stylebox_override("focus", ThemeKit.button_style(fill, 20, ink))
	return button

static func animate_press(control: Control) -> void:
	control.pivot_offset = control.size * 0.5
	var tween := control.create_tween()
	tween.tween_property(control, "scale", Vector2(0.95, 0.95), 0.07).set_trans(Tween.TRANS_SINE)
	tween.tween_property(control, "scale", Vector2(1.03, 1.03), 0.10).set_trans(Tween.TRANS_BACK)
	tween.tween_property(control, "scale", Vector2.ONE, 0.16).set_trans(Tween.TRANS_SINE)
