extends Node

const SAVE_PATH := "user://mallow_save_v1.json"
const SCHEMA_VERSION := 3

const GAME_AXIS := {
	"flash": "memory",
	"react": "focus",
	"bubble": "calculation",
	"trace": "coordination",
	"switch": "focus",
	"count": "memory",
	"nback": "memory",
	"cards": "memory",
	"stroop": "focus",
	"trail": "focus",
	"flank": "focus",
	"rev": "memory",
	"chop": "focus",
	"whack": "coordination",
	"spot": "sight",
	"catch": "coordination",
	"diff": "sight",
	"odd": "sight",
	"rotate": "space",
	"slide": "space",
	"melody": "sound",
	"rhythm": "sound",
	"pitch": "sound",
	"math": "calculation",
	"guess": "calculation",
	"merge": "calculation",
	"sort": "logic",
	"nono": "logic",
	"run": "speed",
	"fit": "space",
	"iq": "logic",
	"sudoku": "logic",
	"anagram": "language",
	"wordsearch": "language",
	"braintype": "logic",
	"moamoa": "language",
	"queens": "logic",
	"tango": "logic"
}

const GAME_AXES := {
	"nback": ["memory", "focus"],
	"moamoa": ["language", "logic"],
	"braintype": ["logic", "language"],
	"queens": ["logic", "space"],
	"tango": ["logic", "focus"]
}

const GAME_CAP := {
	"flash": 1000.0,
	"react": 1000.0,
	"bubble": 650.0,
	"trace": 1000.0,
	"switch": 1000.0,
	"count": 1000.0,
	"nback": 1000.0,
	"cards": 1000.0,
	"stroop": 1000.0,
	"trail": 1000.0,
	"flank": 1000.0,
	"rev": 1000.0,
	"chop": 1000.0,
	"whack": 1000.0,
	"spot": 1000.0,
	"catch": 1000.0,
	"diff": 1000.0,
	"odd": 1000.0,
	"rotate": 1000.0,
	"slide": 1000.0,
	"melody": 1000.0,
	"rhythm": 1000.0,
	"pitch": 1000.0,
	"math": 1000.0,
	"guess": 1000.0,
	"merge": 1000.0,
	"sort": 1000.0,
	"nono": 1000.0,
	"run": 1000.0,
	"fit": 1000.0,
	"iq": 1000.0,
	"sudoku": 1000.0,
	"anagram": 1000.0,
	"wordsearch": 1000.0,
	"braintype": 1000.0,
	"moamoa": 1000.0,
	"queens": 1000.0,
	"tango": 1000.0
}

var data: Dictionary = {}

func _ready() -> void:
	_load()

func _defaults() -> Dictionary:
	return {
		"schemaVersion": SCHEMA_VERSION,
		"profile": {
			"language": "ko",
			"sound": true,
			"music": false,
			"haptics": true,
			"streak": 1,
			"lastSeen": "",
			"skillScores": _default_skill_scores()
		},
		"records": {},
		"mission": {"date": "", "completed": []},
		"assessment": {
			"completed": false,
			"source": "pending",
			"completedAt": "",
			"scores": _default_skill_scores()
		}
	}

func _default_skill_scores() -> Dictionary:
	return {
		"memory": 50,
		"focus": 50,
		"calculation": 50,
		"coordination": 50,
		"speed": 50,
		"space": 50,
		"logic": 50,
		"language": 50,
		"sound": 50,
		"sight": 50
	}

func _load() -> void:
	data = _defaults()
	if not FileAccess.file_exists(SAVE_PATH):
		_save()
		return
	var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		return
	var parsed = JSON.parse_string(file.get_as_text())
	if parsed is Dictionary:
		data = _merge_defaults(parsed)

func _merge_defaults(incoming: Dictionary) -> Dictionary:
	var merged := _defaults()
	for key in incoming:
		merged[key] = incoming[key]
	if not merged.get("profile", {}) is Dictionary:
		merged["profile"] = _defaults()["profile"]
	else:
		var profile: Dictionary = _defaults()["profile"]
		for key in merged["profile"]:
			profile[key] = merged["profile"][key]
		merged["profile"] = profile
	if not merged.get("records", {}) is Dictionary:
		merged["records"] = {}
	var default_profile: Dictionary = _defaults()["profile"]
	if not merged["profile"].get("skillScores", {}) is Dictionary:
		merged["profile"]["skillScores"] = _default_skill_scores()
	else:
		var profile_scores: Dictionary = _default_skill_scores()
		for key in merged["profile"]["skillScores"]:
			profile_scores[key] = int(clampi(int(merged["profile"]["skillScores"][key]), 0, 100))
		merged["profile"]["skillScores"] = profile_scores
	if not merged.get("assessment", {}) is Dictionary:
		merged["assessment"] = _defaults()["assessment"]
	else:
		var assessment: Dictionary = _defaults()["assessment"]
		for key in merged["assessment"]:
			assessment[key] = merged["assessment"][key]
		if not assessment.get("scores", {}) is Dictionary:
			assessment["scores"] = _default_skill_scores()
		merged["assessment"] = assessment
	merged["schemaVersion"] = SCHEMA_VERSION
	return merged

func _save() -> void:
	var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file:
		file.store_string(JSON.stringify(data))

func get_setting(key: String, fallback = null):
	return data.get("profile", {}).get(key, fallback)

func set_setting(key: String, value) -> void:
	data["profile"][key] = value
	_save()

func has_assessment() -> bool:
	return bool(data.get("assessment", {}).get("completed", false))

func assessment_was_skipped() -> bool:
	return str(data.get("assessment", {}).get("source", "")) == "skipped"

func assessment_scores() -> Dictionary:
	var scores: Dictionary = _default_skill_scores()
	var saved: Variant = data.get("assessment", {}).get("scores", {})
	if saved is Dictionary:
		for key in scores:
			scores[key] = int(clampi(int(saved.get(key, scores[key])), 0, 100))
	return scores

func get_skill_scores() -> Dictionary:
	var scores: Dictionary = _default_skill_scores()
	var saved: Variant = data.get("profile", {}).get("skillScores", {})
	if saved is Dictionary:
		for key in scores:
			scores[key] = int(clampi(int(saved.get(key, scores[key])), 0, 100))
	return scores

func save_assessment(scores: Dictionary, source: String = "baseline") -> void:
	var safe_scores: Dictionary = _default_skill_scores()
	for key in safe_scores:
		safe_scores[key] = int(clampi(int(scores.get(key, 50)), 0, 100))
	data["assessment"] = {
		"completed": true,
		"source": source,
		"completedAt": Time.get_datetime_string_from_system(),
		"scores": safe_scores.duplicate(true)
	}
	data["profile"]["skillScores"] = safe_scores.duplicate(true)
	_save()

func reset_assessment() -> void:
	data["assessment"] = _defaults()["assessment"]
	data["profile"]["skillScores"] = _default_skill_scores()
	_save()

func get_best(game_id: String) -> int:
	return int(data.get("records", {}).get(game_id, {}).get("best", 0))

func get_plays(game_id: String) -> int:
	return int(data.get("records", {}).get(game_id, {}).get("plays", 0))

func record_result(game_id: String, score: int) -> bool:
	var old_best := get_best(game_id)
	var record: Dictionary = data["records"].get(game_id, {"best": 0, "plays": 0, "last": 0})
	record["best"] = maxi(old_best, score)
	record["plays"] = int(record.get("plays", 0)) + 1
	record["last"] = score
	data["records"][game_id] = record
	var axis: String = str(GAME_AXIS.get(game_id, ""))
	var axes: Array = GAME_AXES.get(game_id, [])
	if axes.is_empty() and axis != "":
		axes = [axis]
	if not axes.is_empty():
		var cap: float = float(GAME_CAP.get(game_id, 1000.0))
		var live_score := clampf(float(score) / cap * 100.0, 0.0, 100.0)
		var skill_scores := get_skill_scores()
		for axis_name in axes:
			var previous: float = float(skill_scores.get(axis_name, 50))
			skill_scores[axis_name] = int(round(previous * 0.65 + live_score * 0.35))
		data["profile"]["skillScores"] = skill_scores
	_save()
	return score > old_best

func total_plays() -> int:
	var total := 0
	for record in data.get("records", {}).values():
		total += int(record.get("plays", 0))
	return total

func completed_today(game_id: String) -> bool:
	var today := Time.get_date_string_from_system()
	var mission: Dictionary = data.get("mission", {})
	if mission.get("date", "") != today:
		return false
	return game_id in mission.get("completed", [])

func mark_completed(game_id: String) -> void:
	var today := Time.get_date_string_from_system()
	if data["mission"].get("date", "") != today:
		data["mission"] = {"date": today, "completed": []}
	if game_id not in data["mission"]["completed"]:
		data["mission"]["completed"].append(game_id)
	_save()

func mission_count() -> int:
	var today := Time.get_date_string_from_system()
	if data["mission"].get("date", "") != today:
		return 0
	return data["mission"].get("completed", []).size()
