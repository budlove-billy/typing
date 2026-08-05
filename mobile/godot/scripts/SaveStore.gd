extends Node

const SAVE_PATH := "user://mallow_save_v1.json"
const SCHEMA_VERSION := 1

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
			"lastSeen": ""
		},
		"records": {},
		"mission": {"date": "", "completed": []}
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
