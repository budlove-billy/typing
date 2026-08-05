extends Control

const BG := Color("#f4f7fb")
const INK := Color("#182235")
const MUTED := Color("#66738f")
const BLUE := Color("#4f7cff")
const TEAL := Color("#22a77a")

var body: VBoxContainer
var scroll: ScrollContainer
var header_title: Label
var header_back: Button
var header_avatar: MallowAvatar
var nav_panel: PanelContainer
var nav_buttons: Dictionary = {}
var current_screen := "home"
var current_game_id := ""
var current_game: Control

func _ready() -> void:
	_build_shell()
	I18n.language_changed.connect(_refresh_screen)
	show_home()

func _build_shell() -> void:
	var background := ColorRect.new()
	background.color = BG
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 18)
	margin.add_theme_constant_override("margin_right", 18)
	margin.add_theme_constant_override("margin_top", 12)
	margin.add_theme_constant_override("margin_bottom", 12)
	add_child(margin)

	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 10)
	root.size_flags_vertical = Control.SIZE_EXPAND_FILL
	margin.add_child(root)

	var header := PanelContainer.new()
	header.custom_minimum_size = Vector2(0, 66)
	header.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color("#ffffff"), 18))
	root.add_child(header)
	var header_row := HBoxContainer.new()
	header_row.add_theme_constant_override("separation", 10)
	header.add_child(header_row)

	header_back = _button("‹", Color("#ffffff"), 48)
	header_back.custom_minimum_size = Vector2(48, 48)
	header_back.add_theme_font_size_override("font_size", 30)
	header_back.pressed.connect(_go_back)
	header_back.visible = false
	header_row.add_child(header_back)

	header_avatar = MallowAvatar.new()
	header_avatar.custom_minimum_size = Vector2(48, 48)
	header_row.add_child(header_avatar)

	var title_box := VBoxContainer.new()
	title_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_box.add_theme_constant_override("separation", 1)
	header_row.add_child(title_box)
	header_title = _label(I18n.t("brand"), 21, INK)
	title_box.add_child(header_title)
	var tagline := _label(I18n.t("tagline"), 11, MUTED)
	tagline.name = "Tagline"
	title_box.add_child(tagline)

	scroll = ScrollContainer.new()
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root.add_child(scroll)
	body = VBoxContainer.new()
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 14)
	scroll.add_child(body)

	nav_panel = PanelContainer.new()
	nav_panel.custom_minimum_size = Vector2(0, 72)
	nav_panel.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color("#ffffff"), 20))
	root.add_child(nav_panel)
	var nav := HBoxContainer.new()
	nav.add_theme_constant_override("separation", 8)
	nav_panel.add_child(nav)
	for item in [{"id": "home", "icon": "⌂", "key": "home"}, {"id": "games", "icon": "✦", "key": "games"}, {"id": "records", "icon": "◈", "key": "records"}]:
		var nav_button := _button("", Color("#ffffff"), 54)
		nav_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		nav_button.add_theme_font_size_override("font_size", 13)
		nav_button.pressed.connect(_navigate.bind(item["id"]))
		nav.add_child(nav_button)
		nav_buttons[item["id"]] = nav_button

func _refresh_screen() -> void:
	if current_screen == "home":
		show_home()
	elif current_screen == "games":
		show_games()
	elif current_screen == "records":
		show_records()
	elif current_screen == "settings":
		show_settings()

func _navigate(screen: String) -> void:
	AudioDirector.tap()
	match screen:
		"home": show_home()
		"games": show_games()
		"records": show_records()

func _go_back() -> void:
	AudioDirector.tap()
	if current_game:
		current_game.queue_free()
		current_game = null
	show_games()

func _set_chrome(screen: String, title: String, in_game: bool = false) -> void:
	current_screen = screen
	header_title.text = title
	header_back.visible = in_game
	header_avatar.visible = not in_game
	nav_panel.visible = not in_game
	for id in nav_buttons:
		var button: Button = nav_buttons[id]
		button.text = _nav_text(id, id == screen)
		button.add_theme_stylebox_override("normal", ThemeKit.button_style(Color("#e9efff") if id == screen else Color("#ffffff"), 14))
		button.add_theme_color_override("font_color", BLUE if id == screen else MUTED)

func _nav_text(id: String, selected: bool) -> String:
	var icon: String = str({"home": "⌂", "games": "✦", "records": "◈"}.get(id, "•"))
	var name := I18n.t(id)
	return ("● " if selected else "") + icon + "  " + name

func _clear_body() -> void:
	for child in body.get_children():
		child.queue_free()
	body = body
	scroll.scroll_vertical = 0

func show_home() -> void:
	_set_chrome("home", I18n.t("brand"))
	_clear_body()
	var hero := PanelContainer.new()
	hero.custom_minimum_size = Vector2(0, 155)
	hero.add_theme_stylebox_override("panel", ThemeKit.box(Color("#4f7cff"), 24, Color.TRANSPARENT, 0, true))
	body.add_child(hero)
	var hero_row := HBoxContainer.new()
	hero.add_child(hero_row)
	var hero_text := VBoxContainer.new()
	hero_row.add_theme_constant_override("separation", 5)
	hero_row.add_child(hero_text)
	var greeting := _label(I18n.t("home_greeting"), 23, Color.WHITE)
	greeting.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	hero_text.add_child(greeting)
	var sub := _label(I18n.t("home_sub"), 13, Color(1, 1, 1, 0.82))
	hero_text.add_child(sub)
	var streak := _label("✦  1 " + I18n.t("streak"), 13, Color.WHITE)
	streak.add_theme_stylebox_override("normal", ThemeKit.box(Color(1, 1, 1, 0.16), 20))
	hero_text.add_child(streak)
	var avatar := MallowAvatar.new()
	avatar.mood = "good"
	avatar.custom_minimum_size = Vector2(105, 105)
	hero_row.add_child(avatar)

	var mission_head := _section_heading(I18n.t("mission"), str(SaveStore.mission_count()) + "/3")
	body.add_child(mission_head)
	var mission := PanelContainer.new()
	mission.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color("#ffffff"), 18))
	body.add_child(mission)
	var mission_box := VBoxContainer.new()
	mission_box.add_theme_constant_override("separation", 8)
	mission.add_child(mission_box)
	var mission_label := _label(I18n.t("mission_progress") + "  ·  " + str(SaveStore.mission_count()) + "/3", 13, MUTED)
	mission_box.add_child(mission_label)
	var progress := ProgressBar.new()
	progress.max_value = 3
	progress.value = SaveStore.mission_count()
	progress.show_percentage = false
	progress.custom_minimum_size = Vector2(0, 9)
	progress.add_theme_stylebox_override("background", ThemeKit.box(Color("#edf1f7"), 6))
	progress.add_theme_stylebox_override("fill", ThemeKit.box(Color("#22a77a"), 6))
	mission_box.add_child(progress)

	body.add_child(_section_heading(I18n.t("today_games"), "3"))
	var games_row := HBoxContainer.new()
	games_row.add_theme_constant_override("separation", 9)
	body.add_child(games_row)
	for game in GameCatalog.all():
		games_row.add_child(_game_tile(game))

	var browse := _button(I18n.t("browse_games") + "  →", Color("#ffffff"), 54)
	browse.add_theme_color_override("font_color", BLUE)
	browse.pressed.connect(show_games)
	body.add_child(browse)

func show_games() -> void:
	_set_chrome("games", I18n.t("games"))
	_clear_body()
	body.add_child(_label(I18n.t("today_games"), 23, INK))
	body.add_child(_label(I18n.t("home_sub"), 13, MUTED))
	for game in GameCatalog.all():
		body.add_child(_large_game_card(game))
	var settings := _button("⚙  " + I18n.t("settings"), Color("#ffffff"), 52)
	settings.add_theme_color_override("font_color", MUTED)
	settings.pressed.connect(show_settings)
	body.add_child(settings)

func show_records() -> void:
	_set_chrome("records", I18n.t("records"))
	_clear_body()
	var summary := PanelContainer.new()
	summary.add_theme_stylebox_override("panel", ThemeKit.box(Color("#e9efff"), 20))
	body.add_child(summary)
	var summary_row := HBoxContainer.new()
	summary.add_child(summary_row)
	summary_row.add_child(_stat(I18n.t("plays"), str(SaveStore.total_plays())))
	summary_row.add_child(_stat(I18n.t("mission"), str(SaveStore.mission_count()) + "/3"))
	for game in GameCatalog.all():
		var card := PanelContainer.new()
		card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color("#ffffff"), 18))
		body.add_child(card)
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 12)
		card.add_child(row)
		var dot := Label.new()
		dot.text = "●"
		dot.add_theme_color_override("font_color", Color(game["color"]))
		dot.add_theme_font_size_override("font_size", 24)
		row.add_child(dot)
		var name_box := VBoxContainer.new()
		name_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		name_box.add_child(_label(I18n.t(game["name_key"]), 16, INK))
		name_box.add_child(_label(game["axis"], 12, MUTED))
		row.add_child(name_box)
		row.add_child(_label(str(SaveStore.get_best(game["id"])) + " " + I18n.t("score"), 16, BLUE, HORIZONTAL_ALIGNMENT_RIGHT))

func show_settings() -> void:
	_set_chrome("settings", I18n.t("settings"))
	_clear_body()
	body.add_child(_label(I18n.t("settings"), 23, INK))
	body.add_child(_label(I18n.t("settings_hint"), 13, MUTED))
	for setting in [{"key": "sound", "label": "sound"}, {"key": "music", "label": "music"}, {"key": "haptics", "label": "haptics"}]:
		var toggle := CheckButton.new()
		toggle.text = I18n.t(setting["label"])
		toggle.button_pressed = bool(SaveStore.get_setting(setting["key"], true))
		toggle.custom_minimum_size = Vector2(0, 56)
		toggle.add_theme_font_size_override("font_size", 15)
		toggle.toggled.connect(_setting_changed.bind(setting["key"]))
		body.add_child(toggle)
	var lang_button := _button(I18n.t("language") + ":  " + (I18n.t("korean") if I18n.language == "ko" else I18n.t("english")), Color("#ffffff"), 56)
	lang_button.add_theme_color_override("font_color", BLUE)
	lang_button.pressed.connect(_toggle_language)
	body.add_child(lang_button)

func _setting_changed(value: bool, key: String) -> void:
	AudioDirector.tap()
	SaveStore.set_setting(key, value)
	if key == "sound":
		AudioDirector.set_enabled(value)
	elif key == "music":
		AudioDirector.set_music_enabled(value)

func _toggle_language() -> void:
	AudioDirector.tap()
	I18n.set_language("en" if I18n.language == "ko" else "ko")

func _launch_game(game_id: String) -> void:
	AudioDirector.tap()
	current_game_id = game_id
	current_screen = "game"
	header_title.text = I18n.t(GameCatalog.get_game(game_id)["name_key"])
	header_back.visible = true
	header_avatar.visible = false
	nav_panel.visible = false
	_clear_body()
	var game_script = load("res://games/" + game_id.capitalize() + "Game.gd")
	current_game = game_script.new()
	current_game.size_flags_vertical = Control.SIZE_EXPAND_FILL
	current_game.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	current_game.finished.connect(_on_game_finished.bind(game_id))
	body.add_child(current_game)

func _on_game_finished(result: Dictionary, game_id: String) -> void:
	var score := int(result.get("score", 0))
	var is_new := SaveStore.record_result(game_id, score)
	SaveStore.mark_completed(game_id)
	AudioDirector.win()
	if current_game:
		current_game.queue_free()
		current_game = null
	_show_result(game_id, score, is_new, str(result.get("detail", "")))

func _show_result(game_id: String, score: int, is_new: bool, detail: String) -> void:
	current_screen = "result"
	header_title.text = I18n.t(GameCatalog.get_game(game_id)["name_key"])
	header_back.visible = false
	header_avatar.visible = true
	nav_panel.visible = false
	_clear_body()
	var result_card := PanelContainer.new()
	result_card.add_theme_stylebox_override("panel", ThemeKit.box(Color("#e9efff"), 24, BLUE, 1, true))
	body.add_child(result_card)
	var result_box := VBoxContainer.new()
	result_box.alignment = BoxContainer.ALIGNMENT_CENTER
	result_box.add_theme_constant_override("separation", 10)
	result_card.add_child(result_box)
	var avatar := MallowAvatar.new()
	avatar.mood = "win" if is_new else "good"
	avatar.custom_minimum_size = Vector2(112, 112)
	avatar.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	result_box.add_child(avatar)
	var title := _label(I18n.t("new_record") if is_new else I18n.t("correct"), 20, BLUE, HORIZONTAL_ALIGNMENT_CENTER)
	result_box.add_child(title)
	var score_label := _label(str(score) + " " + I18n.t("score"), 42, INK, HORIZONTAL_ALIGNMENT_CENTER)
	result_box.add_child(score_label)
	result_box.add_child(_label(detail, 13, MUTED, HORIZONTAL_ALIGNMENT_CENTER))
	result_box.add_child(_label(I18n.t("result_detail"), 13, MUTED, HORIZONTAL_ALIGNMENT_CENTER))

	var next := _button(I18n.t("next") + "  →", BLUE, 58)
	next.pressed.connect(_next_game.bind(game_id))
	body.add_child(next)
	var home := _button(I18n.t("go_home"), Color("#ffffff"), 52)
	home.add_theme_color_override("font_color", MUTED)
	home.pressed.connect(show_home)
	body.add_child(home)

func _next_game(game_id: String) -> void:
	var games := GameCatalog.all()
	for i in range(games.size()):
		if games[i]["id"] == game_id:
			_launch_game(games[(i + 1) % games.size()]["id"])
			return

func _game_tile(game: Dictionary) -> Control:
	var button := _button("", Color("#ffffff"), 146)
	button.custom_minimum_size = Vector2(0, 146)
	button.add_theme_stylebox_override("normal", ThemeKit.box(Color("#ffffff"), 18, ThemeKit.BORDER, 1, true))
	button.add_theme_stylebox_override("hover", ThemeKit.box(Color("#f3f6ff"), 18, Color("#b8c8ff"), 1, true))
	button.add_theme_font_size_override("font_size", 13)
	button.text = "●\n" + I18n.t(game["name_key"]) + "\n" + game["axis"]
	button.add_theme_color_override("font_color", Color(game["color"]))
	button.add_theme_color_override("font_hover_color", Color(game["color"]))
	button.pressed.connect(_launch_game.bind(game["id"]))
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	return button

func _large_game_card(game: Dictionary) -> Control:
	var button := _button("", Color("#ffffff"), 88)
	button.add_theme_stylebox_override("normal", ThemeKit.box(Color("#ffffff"), 18, ThemeKit.BORDER, 1, true))
	button.add_theme_stylebox_override("hover", ThemeKit.box(Color("#f3f6ff"), 18, Color("#b8c8ff"), 1, true))
	button.text = "●  " + I18n.t(game["name_key"]) + "    ·    " + game["axis"] + "\n     " + I18n.t(game["desc_key"])
	button.add_theme_color_override("font_color", Color(game["color"]))
	button.pressed.connect(_launch_game.bind(game["id"]))
	return button

func _section_heading(title: String, meta: String) -> Control:
	var row := HBoxContainer.new()
	var left := _label(title, 18, INK)
	left.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(left)
	row.add_child(_label(meta, 13, MUTED, HORIZONTAL_ALIGNMENT_RIGHT))
	return row

func _stat(label_text: String, value: String) -> Control:
	var box := VBoxContainer.new()
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	box.add_theme_constant_override("separation", 2)
	box.add_child(_label(value, 25, BLUE, HORIZONTAL_ALIGNMENT_CENTER))
	box.add_child(_label(label_text, 11, MUTED, HORIZONTAL_ALIGNMENT_CENTER))
	return box

func _label(text_value: String, font_size: int, color: Color, align: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = align
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	return label

func _button(text_value: String, fill: Color, height: int) -> Button:
	var button := Button.new()
	button.text = text_value
	button.custom_minimum_size = Vector2(0, height)
	button.add_theme_font_size_override("font_size", 16)
	button.add_theme_color_override("font_color", INK)
	button.add_theme_color_override("font_hover_color", INK)
	button.add_theme_stylebox_override("normal", ThemeKit.button_style(fill, 16))
	button.add_theme_stylebox_override("hover", ThemeKit.button_style(fill.lightened(0.035), 16))
	button.add_theme_stylebox_override("pressed", ThemeKit.button_style(fill.darkened(0.04), 16))
	button.add_theme_stylebox_override("focus", ThemeKit.button_style(fill, 16, BLUE))
	return button
