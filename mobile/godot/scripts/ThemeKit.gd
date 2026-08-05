class_name ThemeKit
extends RefCounted

const INK := Color("#172033")
const MUTED := Color("#68748c")
const SUBTLE := Color("#97a1b4")
const BORDER := Color("#e5e9f2")
const SURFACE := Color("#ffffff")
const BACKGROUND := Color("#f6f7fb")
const BLUE := Color("#4c6fff")
const BLUE_DARK := Color("#3553c7")
const BLUE_SOFT := Color("#edf1ff")
const TEAL := Color("#1f9d78")
const TEAL_SOFT := Color("#e3f6ef")
const PINK := Color("#f06f91")
const PINK_SOFT := Color("#ffebf0")
const AMBER := Color("#c9841d")
const AMBER_SOFT := Color("#fff2d9")

static func box(fill: Color, radius: int = 18, border: Color = Color.TRANSPARENT, border_width: int = 0, shadow: bool = false) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	style.anti_aliasing = true
	style.anti_aliasing_size = 1.0
	if border_width > 0:
		style.border_color = border
		style.border_width_left = border_width
		style.border_width_top = border_width
		style.border_width_right = border_width
		style.border_width_bottom = border_width
	if shadow:
		style.shadow_color = Color(0.08, 0.12, 0.22, 0.075)
		style.shadow_size = 7
		style.shadow_offset = Vector2(0, 2)
	return style

static func button_style(fill: Color, radius: int = 14, border: Color = Color.TRANSPARENT) -> StyleBoxFlat:
	var style := box(fill, radius, border, 1 if border != Color.TRANSPARENT else 0, false)
	style.content_margin_left = 14
	style.content_margin_right = 14
	style.content_margin_top = 10
	style.content_margin_bottom = 10
	return style

static func panel_style(fill: Color = SURFACE, radius: int = 20, padding: int = 16, shadow: bool = true) -> StyleBoxFlat:
	var style := box(fill, radius, BORDER, 1, shadow)
	style.content_margin_left = padding
	style.content_margin_right = padding
	style.content_margin_top = padding
	style.content_margin_bottom = padding
	return style

static func soft_panel(fill: Color, radius: int = 20, padding: int = 16) -> StyleBoxFlat:
	var style := box(fill, radius)
	style.content_margin_left = padding
	style.content_margin_right = padding
	style.content_margin_top = padding
	style.content_margin_bottom = padding
	return style
