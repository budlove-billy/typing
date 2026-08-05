class_name ThemeKit
extends RefCounted

const INK := Color("#182235")
const MUTED := Color("#66738f")
const BORDER := Color("#e2e8f2")
const SURFACE := Color("#ffffff")
const BACKGROUND := Color("#f4f7fb")
const BLUE := Color("#4f7cff")
const BLUE_SOFT := Color("#e9efff")
const TEAL := Color("#22a77a")
const TEAL_SOFT := Color("#ddf5eb")
const PINK := Color("#ff7096")
const PINK_SOFT := Color("#ffe5ed")
const AMBER := Color("#d49324")
const AMBER_SOFT := Color("#fff1d4")

static func box(fill: Color, radius: int = 18, border: Color = Color.TRANSPARENT, border_width: int = 0, shadow: bool = false) -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = fill
	style.corner_radius_top_left = radius
	style.corner_radius_top_right = radius
	style.corner_radius_bottom_left = radius
	style.corner_radius_bottom_right = radius
	if border_width > 0:
		style.border_color = border
		style.border_width_left = border_width
		style.border_width_top = border_width
		style.border_width_right = border_width
		style.border_width_bottom = border_width
	if shadow:
		style.shadow_color = Color(0.09, 0.13, 0.22, 0.10)
		style.shadow_size = 8
		style.shadow_offset = Vector2(0, 3)
	return style

static func button_style(fill: Color, radius: int = 14, border: Color = Color.TRANSPARENT) -> StyleBoxFlat:
	return box(fill, radius, border, 1 if border != Color.TRANSPARENT else 0, false)

static func panel_style(fill: Color = SURFACE, radius: int = 20) -> StyleBoxFlat:
	return box(fill, radius, BORDER, 1, true)
