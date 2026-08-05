class_name GameCatalog
extends RefCounted

const GAMES := [
	{"id": "flash", "name_key": "flash_name", "desc_key": "flash_desc", "axis": "기억", "color": "#ff7096"},
	{"id": "bubble", "name_key": "bubble_name", "desc_key": "bubble_desc", "axis": "계산", "color": "#4f7cff"},
	{"id": "trace", "name_key": "trace_name", "desc_key": "trace_desc", "axis": "협응", "color": "#22a77a"}
]

static func all() -> Array:
	return GAMES.duplicate(true)

static func get_game(game_id: String) -> Dictionary:
	for game in GAMES:
		if game["id"] == game_id:
			return game
	return {}
