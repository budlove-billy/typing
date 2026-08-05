class_name GameCatalog
extends RefCounted

const GAMES := [
	{"id": "flash", "name_key": "flash_name", "desc_key": "flash_desc", "axis_key": "memory", "axis": "기억", "color": "#f06f91"},
	{"id": "bubble", "name_key": "bubble_name", "desc_key": "bubble_desc", "axis_key": "calculation", "axis": "계산", "color": "#4c6fff"},
	{"id": "trace", "name_key": "trace_name", "desc_key": "trace_desc", "axis_key": "coordination", "axis": "협응", "color": "#1f9d78"},
	{"id": "react", "name_key": "react_name", "desc_key": "react_desc", "axis_key": "focus", "axis": "집중", "color": "#d99327"},
	{"id": "switch", "name_key": "switch_name", "desc_key": "switch_desc", "axis_key": "focus", "axis": "집중", "color": "#1f9d78"}
]

static func all() -> Array:
	return GAMES.duplicate(true)

static func daily() -> Array:
	return GAMES.slice(0, 3).duplicate(true)

static func get_game(game_id: String) -> Dictionary:
	for game in GAMES:
		if game["id"] == game_id:
			return game
	return {}
