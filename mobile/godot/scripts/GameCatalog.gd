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
	{"id": "memory", "name_key": "category_memory", "icon": "cat_memory", "color": "#f06f91"},
	{"id": "focus", "name_key": "category_focus", "icon": "cat_focus", "color": "#d99327"},
	{"id": "speed", "name_key": "category_speed", "icon": "cat_speed", "color": "#4c6fff"},
	{"id": "coordination", "name_key": "category_coordination", "icon": "cat_coordination", "color": "#1f9d78"},
	{"id": "sound", "name_key": "category_sound", "icon": "cat_sound", "color": "#8d62d7"},
	{"id": "sight", "name_key": "category_sight", "icon": "cat_sight", "color": "#3f82db"},
	{"id": "space", "name_key": "category_space", "icon": "cat_space", "color": "#16a085"},
	{"id": "calculation", "name_key": "category_calculation", "icon": "cat_calculation", "color": "#6f61d9"},
	{"id": "logic", "name_key": "category_logic", "icon": "cat_logic", "color": "#5a6b82"},
	{"id": "language", "name_key": "category_language", "icon": "cat_language", "color": "#c9841d"},
	{"id": "daily", "name_key": "category_daily", "icon": "cat_daily", "color": "#e75f88"},
	{"id": "test", "name_key": "category_test", "icon": "cat_test", "color": "#8d62d7"}
]

const CATEGORY_GAMES := {
	"memory": ["flash", "count", "nback", "cards", "rev"],
	"focus": ["stroop", "switch", "flank"],
	"speed": ["trail", "react", "chop", "run"],
	"coordination": ["whack", "catch", "trace"],
	"sound": ["melody", "rhythm", "pitch"],
	"sight": ["spot", "odd", "diff"],
	"space": ["rotate", "slide", "fit"],
	"calculation": ["math", "bubble", "merge", "guess"],
	"logic": ["iq", "sudoku", "sort", "nono"],
	"language": ["anagram", "wordsearch"],
	"daily": ["moamoa", "queens", "tango"],
	"test": ["braintype"]
}

# Semantic reference from playmallow.com. Native GameIcon renders matching vector pictograms.
const WEB_ICON_REFERENCE := {
	"flash": "⚡", "count": "👥", "nback": "🔡", "cards": "🃏", "rev": "🔁",
	"stroop": "🎨", "switch": "🔀", "flank": "🎯", "trail": "🔗", "react": "⏱️",
	"chop": "🍡", "run": "🏃", "whack": "🔨", "catch": "🧺", "trace": "✏️",
	"melody": "🎵", "rhythm": "🥁", "pitch": "🎧", "spot": "🌈", "odd": "🔎",
	"diff": "👀", "rotate": "🔄", "slide": "🧊", "fit": "🧱", "math": "➗",
	"bubble": "🫧", "merge": "🍭", "guess": "📊", "iq": "🧠", "sudoku": "🔢",
	"sort": "🧪", "nono": "🖼️", "anagram": "🔤", "wordsearch": "🔠",
	"moamoa": "🧩", "queens": "👑", "tango": "🌗", "braintype": "🔮"
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

static func icon_reference_for(game_id: String) -> String:
	return str(WEB_ICON_REFERENCE.get(game_id, "🎮"))

static func script_path(game_id: String) -> String:
	var class_names := {"iq": "IQGame"}
	var script_class := str(class_names.get(game_id, game_id.capitalize() + "Game"))
	return "res://games/" + script_class + ".gd"
