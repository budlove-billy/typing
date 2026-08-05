class_name RecommendationEngine
extends RefCounted

const AXIS_KEYS := ["memory", "focus", "calculation", "coordination", "speed", "space", "logic", "language", "sound", "sight"]

static func recommended(limit: int = 3) -> Array:
	var skills := SaveStore.get_skill_scores()
	var ranked: Array = []
	for game in GameCatalog.all():
		var axis := str(game.get("axis_key", "memory"))
		var skill := float(skills.get(axis, 50))
		var plays := SaveStore.get_plays(str(game["id"]))
		var weakness := (100.0 - skill) * 0.55
		var discovery := 25.0 if plays == 0 else 0.0
		var freshness := maxf(0.0, 20.0 - float(plays) * 4.0)
		var reason_key := "rec_reason_weak"
		if plays == 0:
			reason_key = "rec_reason_new"
		elif skill >= 70.0:
			reason_key = "rec_reason_balance"
		ranked.append({
			"game": game,
			"skill": int(round(skill)),
			"rank": weakness + discovery + freshness,
			"reason_key": reason_key,
			"axis_key": axis
		})
	ranked.sort_custom(func(a: Dictionary, b: Dictionary) -> bool:
		return float(a["rank"]) > float(b["rank"])
	)
	return ranked.slice(0, mini(limit, ranked.size()))

static func reason_text(item: Dictionary) -> String:
	var game: Dictionary = item.get("game", {})
	var axis_label := I18n.t("axis_" + str(item.get("axis_key", "memory")))
	var reason := I18n.t(str(item.get("reason_key", "rec_reason_weak")))
	return reason.replace("{axis}", axis_label).replace("{score}", str(item.get("skill", 50))).replace("{game}", I18n.t(str(game.get("name_key", ""))))

static func axis_label(axis_key: String) -> String:
	return I18n.t("axis_" + axis_key)
