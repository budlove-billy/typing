class_name GameCatalog
extends RefCounted

const GAMES := [
	{"id": "flash", "name_key": "flash_name", "desc_key": "flash_desc", "axis_key": "memory", "axis": "기억", "color": "#f06f91"},
	{"id": "count", "name_key": "count_name", "desc_key": "count_desc", "axis_key": "memory", "axis": "기억", "color": "#f06f91"},
	{"id": "nback", "name_key": "nback_name", "desc_key": "nback_desc", "axis_key": "memory", "axis": "기억", "color": "#9b63d7"},
	{"id": "cards", "name_key": "cards_name", "desc_key": "cards_desc", "axis_key": "memory", "axis": "기억", "color": "#f06f91"},
	{"id": "stroop", "name_key": "stroop_name", "desc_key": "stroop_desc", "axis_key": "focus", "axis": "집중", "color": "#d99327"},
	{"id": "switch", "name_key": "switch_name", "desc_key": "switch_desc", "axis_key": "focus", "axis": "집중", "color": "#1f9d78"},
	{"id": "trail", "name_key": "trail_name", "desc_key": "trail_desc", "axis_key": "focus", "axis": "집중", "color": "#4c6fff"},
	{"id": "react", "name_key": "react_name", "desc_key": "react_desc", "axis_key": "focus", "axis": "집중", "color": "#d99327"},
	{"id": "chop", "name_key": "chop_name", "desc_key": "chop_desc", "axis_key": "focus", "axis": "집중", "color": "#c9841d"},
	{"id": "run", "name_key": "run_name", "desc_key": "run_desc", "axis_key": "speed", "axis": "속도", "color": "#4c6fff"},
	{"id": "whack", "name_key": "whack_name", "desc_key": "whack_desc", "axis_key": "coordination", "axis": "협응", "color": "#1f9d78"},
	{"id": "melody", "name_key": "melody_name", "desc_key": "melody_desc", "axis_key": "sound", "axis": "청각", "color": "#4c6fff"},
	{"id": "spot", "name_key": "spot_name", "desc_key": "spot_desc", "axis_key": "sight", "axis": "관찰", "color": "#4c6fff"},
	{"id": "odd", "name_key": "odd_name", "desc_key": "odd_desc", "axis_key": "sight", "axis": "관찰", "color": "#f06f91"},
	{"id": "rotate", "name_key": "rotate_name", "desc_key": "rotate_desc", "axis_key": "space", "axis": "공간", "color": "#1f9d78"},
	{"id": "slide", "name_key": "slide_name", "desc_key": "slide_desc", "axis_key": "space", "axis": "공간", "color": "#1f9d78"},
	{"id": "math", "name_key": "math_name", "desc_key": "math_desc", "axis_key": "calculation", "axis": "계산", "color": "#4c6fff"},
	{"id": "bubble", "name_key": "bubble_name", "desc_key": "bubble_desc", "axis_key": "calculation", "axis": "계산", "color": "#4c6fff"},
	{"id": "merge", "name_key": "merge_name", "desc_key": "merge_desc", "axis_key": "calculation", "axis": "계산", "color": "#c9841d"},
	{"id": "iq", "name_key": "iq_name", "desc_key": "iq_desc", "axis_key": "logic", "axis": "논리", "color": "#9b63d7"},
	{"id": "sudoku", "name_key": "sudoku_name", "desc_key": "sudoku_desc", "axis_key": "logic", "axis": "논리", "color": "#9b63d7"},
	{"id": "sort", "name_key": "sort_name", "desc_key": "sort_desc", "axis_key": "logic", "axis": "논리", "color": "#1f9d78"},
	{"id": "flank", "name_key": "flank_name", "desc_key": "flank_desc", "axis_key": "focus", "axis": "집중", "color": "#d99327"},
	{"id": "rev", "name_key": "rev_name", "desc_key": "rev_desc", "axis_key": "memory", "axis": "기억", "color": "#9b63d7"},
	{"id": "rhythm", "name_key": "rhythm_name", "desc_key": "rhythm_desc", "axis_key": "sound", "axis": "청각", "color": "#c9841d"},
	{"id": "catch", "name_key": "catch_name", "desc_key": "catch_desc", "axis_key": "coordination", "axis": "협응", "color": "#1f9d78"},
	{"id": "fit", "name_key": "fit_name", "desc_key": "fit_desc", "axis_key": "space", "axis": "공간", "color": "#1f9d78"},
	{"id": "guess", "name_key": "guess_name", "desc_key": "guess_desc", "axis_key": "calculation", "axis": "계산", "color": "#c9841d"},
	{"id": "nono", "name_key": "nono_name", "desc_key": "nono_desc", "axis_key": "logic", "axis": "논리", "color": "#f06f91"},
	{"id": "anagram", "name_key": "anagram_name", "desc_key": "anagram_desc", "axis_key": "language", "axis": "언어", "color": "#c9841d"},
	{"id": "wordsearch", "name_key": "wordsearch_name", "desc_key": "wordsearch_desc", "axis_key": "language", "axis": "언어", "color": "#1f9d78"},
	{"id": "diff", "name_key": "diff_name", "desc_key": "diff_desc", "axis_key": "sight", "axis": "관찰", "color": "#4c6fff"},
	{"id": "pitch", "name_key": "pitch_name", "desc_key": "pitch_desc", "axis_key": "sound", "axis": "청각", "color": "#4c6fff"},
	{"id": "trace", "name_key": "trace_name", "desc_key": "trace_desc", "axis_key": "coordination", "axis": "협응", "color": "#1f9d78"},
	{"id": "braintype", "name_key": "braintype_name", "desc_key": "braintype_desc", "axis_key": "logic", "axis": "논리", "color": "#f06f91"},
	{"id": "moamoa", "name_key": "moamoa_name", "desc_key": "moamoa_desc", "axis_key": "language", "axis": "언어", "color": "#c9841d"},
	{"id": "queens", "name_key": "queens_name", "desc_key": "queens_desc", "axis_key": "logic", "axis": "논리", "color": "#f06f91"},
	{"id": "tango", "name_key": "tango_name", "desc_key": "tango_desc", "axis_key": "logic", "axis": "논리", "color": "#4c6fff"}
]

const CATEGORIES := [
	{"id": "memory", "name_key": "category_memory", "symbol": "M", "color": "#f06f91"},
	{"id": "focus", "name_key": "category_focus", "symbol": "+", "color": "#d99327"},
	{"id": "speed", "name_key": "category_speed", "symbol": ">", "color": "#4c6fff"},
	{"id": "coordination", "name_key": "category_coordination", "symbol": "o", "color": "#1f9d78"},
	{"id": "sight", "name_key": "category_sight", "symbol": "@", "color": "#4c6fff"},
	{"id": "space", "name_key": "category_space", "symbol": "◇", "color": "#1f9d78"},
	{"id": "sound", "name_key": "category_sound", "symbol": "♪", "color": "#9b63d7"},
	{"id": "calculation", "name_key": "category_calculation", "symbol": "÷", "color": "#4c6fff"},
	{"id": "logic", "name_key": "category_logic", "symbol": "∴", "color": "#1f9d78"},
	{"id": "language", "name_key": "category_language", "symbol": "A", "color": "#c9841d"},
	{"id": "test", "name_key": "category_test", "symbol": "?", "color": "#f06f91"}
]

const CATEGORY_GAMES := {
	"memory": ["flash", "count", "nback", "cards", "rev"],
	"focus": ["stroop", "switch"],
	"speed": ["trail", "react", "chop", "run", "flank"],
	"coordination": ["whack", "catch", "trace"],
	"sight": ["spot", "odd", "diff"],
	"space": ["rotate", "slide", "fit"],
	"sound": ["melody", "rhythm", "pitch"],
	"calculation": ["math", "bubble", "merge", "guess"],
	"logic": ["iq", "sudoku", "sort", "nono", "queens", "tango"],
	"language": ["anagram", "wordsearch", "moamoa"],
	"test": ["braintype"]
}

const GAME_SYMBOLS := {
	"flash": "✦", "count": "◌", "nback": "N", "cards": "▦", "stroop": "A",
	"switch": "↔", "trail": "1", "react": "!", "chop": "/", "run": ">",
	"whack": "●", "melody": "♪", "spot": "◉", "odd": "!", "rotate": "↻",
	"slide": "□", "math": "+", "bubble": "○", "merge": "2", "iq": "?",
	"sudoku": "4", "sort": "≡", "flank": "→", "rev": "↶", "rhythm": "∿",
	"catch": "∪", "fit": "▧", "guess": "≈", "nono": "▤", "anagram": "A",
	"wordsearch": "⌕", "diff": "≠", "pitch": "♫", "trace": "⌁", "braintype": "?",
	"moamoa": "가", "queens": "♛", "tango": "☼"
}

static func all() -> Array:
	return GAMES.duplicate(true)

static func daily() -> Array:
	return [get_game("flash"), get_game("bubble"), get_game("trace")]

static func get_game(game_id: String) -> Dictionary:
	for game in GAMES:
		if game["id"] == game_id:
			return game
	return {}

static func categories() -> Array:
	return CATEGORIES.duplicate(true)

static func games_for_category(category_id: String) -> Array:
	var result: Array = []
	for game_id in CATEGORY_GAMES.get(category_id, []):
		var game := get_game(str(game_id))
		if not game.is_empty():
			result.append(game)
	return result

static func symbol_for(game_id: String) -> String:
	return str(GAME_SYMBOLS.get(game_id, "✦"))

static func script_path(game_id: String) -> String:
	var class_names := {"iq": "IQGame"}
	var script_class := str(class_names.get(game_id, game_id.capitalize() + "Game"))
	return "res://games/" + script_class + ".gd"
