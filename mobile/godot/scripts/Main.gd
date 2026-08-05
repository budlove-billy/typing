extends Control

const BG := ThemeKit.BACKGROUND
const INK := ThemeKit.INK
const MUTED := ThemeKit.MUTED
const SUBTLE := ThemeKit.SUBTLE
const BLUE := ThemeKit.BLUE
const TEAL := ThemeKit.TEAL
const GameIconControl = preload("res://scripts/GameIcon.gd")

var body: VBoxContainer
var scroll: ScrollContainer
var header_title: Label
var header_tagline: Label
var header_back: Button
var header_avatar: MallowAvatar
var nav_panel: PanelContainer
var nav_buttons: Dictionary = {}
var nav_labels: Dictionary = {}
var nav_icons: Dictionary = {}
var current_screen := "home"
var current_game_id := ""
var current_game: Control
var drag_scrolling := false
var drag_moved := false
var selected_category := "memory"
var assessment_flow: AssessmentFlow

func _ready() -> void:
	_build_shell()
	I18n.language_changed.connect(_refresh_screen)
	if SaveStore.has_assessment():
		show_home()
	else:
		show_assessment()

func _build_shell() -> void:
	var background := AmbientBackdrop.new()
	background.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	background.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(background)

	var margin := MarginContainer.new()
	margin.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	margin.add_theme_constant_override("margin_left", 16)
	margin.add_theme_constant_override("margin_right", 16)
	margin.add_theme_constant_override("margin_top", 10)
	margin.add_theme_constant_override("margin_bottom", 10)
	add_child(margin)

	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 10)
	root.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	root.size_flags_vertical = Control.SIZE_EXPAND_FILL
	margin.add_child(root)

	var header := PanelContainer.new()
	header.custom_minimum_size = Vector2(0, 64)
	header.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 20, 10, true))
	root.add_child(header)

	var header_row := HBoxContainer.new()
	header_row.alignment = BoxContainer.ALIGNMENT_CENTER
	header_row.add_theme_constant_override("separation", 10)
	header.add_child(header_row)

	header_back = _button("<", Color.WHITE, 42)
	header_back.custom_minimum_size = Vector2(42, 42)
	header_back.add_theme_font_size_override("font_size", 21)
	header_back.pressed.connect(_go_back)
	header_back.visible = false
	header_row.add_child(header_back)

	header_avatar = MallowAvatar.new()
	header_avatar.custom_minimum_size = Vector2(42, 42)
	header_row.add_child(header_avatar)

	var title_box := VBoxContainer.new()
	title_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	title_box.alignment = BoxContainer.ALIGNMENT_CENTER
	title_box.add_theme_constant_override("separation", 0)
	header_row.add_child(title_box)

	header_title = _label(I18n.t("brand"), 20, INK)
	title_box.add_child(header_title)
	header_tagline = _label(I18n.t("tagline"), 11, MUTED)
	title_box.add_child(header_tagline)

	scroll = ScrollContainer.new()
	scroll.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.size_flags_vertical = Control.SIZE_EXPAND_FILL
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	root.add_child(scroll)
	scroll.gui_input.connect(_on_scroll_gui_input)

	body = VBoxContainer.new()
	body.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_theme_constant_override("separation", 12)
	scroll.add_child(body)

	nav_panel = PanelContainer.new()
	nav_panel.custom_minimum_size = Vector2(0, 72)
	nav_panel.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 24, 6, true))
	root.add_child(nav_panel)

	var nav := HBoxContainer.new()
	nav.add_theme_constant_override("separation", 5)
	nav_panel.add_child(nav)
	for id in ["home", "games", "records"]:
		var nav_button := _button("", Color.WHITE, 58)
		nav_button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		nav_button.pressed.connect(_navigate.bind(id))
		nav.add_child(nav_button)
		nav_buttons[id] = nav_button

		var nav_stack := HBoxContainer.new()
		nav_stack.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
		nav_stack.alignment = BoxContainer.ALIGNMENT_CENTER
		nav_stack.add_theme_constant_override("separation", 6)
		nav_stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
		nav_button.add_child(nav_stack)

		var nav_icon := GameIconControl.new().configure("nav_" + id, MUTED, 27, false)
		nav_icon.size_flags_vertical = Control.SIZE_SHRINK_CENTER
		nav_stack.add_child(nav_icon)
		nav_icons[id] = nav_icon
		var nav_label := _label(I18n.t(id), 12, MUTED, HORIZONTAL_ALIGNMENT_CENTER)
		nav_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
		nav_stack.add_child(nav_label)
		nav_labels[id] = nav_label

func _refresh_screen() -> void:
	header_tagline.text = I18n.t("tagline")
	match current_screen:
		"home": show_home()
		"games": show_games()
		"records": show_records()
		"settings": show_settings()
		"assessment": show_assessment()
		"assessment_result": show_assessment_result(SaveStore.assessment_scores())

func _navigate(screen_name: String) -> void:
	AudioDirector.tap()
	match screen_name:
		"home": show_home()
		"games": show_games()
		"records": show_records()

func _go_back() -> void:
	AudioDirector.tap()
	if current_game:
		current_game.queue_free()
		current_game = null
	show_games()

func _set_chrome(screen_name: String, title: String, in_game: bool = false) -> void:
	current_screen = screen_name
	header_title.text = title
	header_back.visible = in_game
	header_avatar.visible = not in_game
	nav_panel.visible = not in_game
	for id in nav_buttons:
		var button: Button = nav_buttons[id]
		var nav_id := str(id)
		var selected: bool = nav_id == screen_name
		var fill := BLUE if selected else Color.WHITE
		var ink := Color.WHITE if selected else MUTED
		button.add_theme_stylebox_override("normal", ThemeKit.button_style(fill, 18))
		button.add_theme_stylebox_override("hover", ThemeKit.button_style(BLUE.lightened(0.08) if selected else Color("#f5f7fc"), 18))
		button.add_theme_stylebox_override("pressed", ThemeKit.button_style(BLUE.darkened(0.08) if selected else ThemeKit.BLUE_SOFT, 18))
		var nav_label: Label = nav_labels[nav_id]
		nav_label.text = I18n.t(nav_id)
		nav_label.add_theme_color_override("font_color", ink)
		var nav_icon: GameIcon = nav_icons[nav_id]
		nav_icon.configure("nav_" + nav_id, ink, 27, false)

func _clear_body() -> void:
	for child in body.get_children():
		body.remove_child(child)
		child.queue_free()
	scroll.scroll_vertical = 0

func _on_scroll_gui_input(event: InputEvent) -> void:
	if event is InputEventScreenDrag:
		scroll.scroll_vertical = maxi(0, scroll.scroll_vertical - int(event.relative.y))
		get_viewport().set_input_as_handled()

func show_home() -> void:
	_set_chrome("home", I18n.t("brand"))
	_clear_body()

	var hero := PanelContainer.new()
	hero.custom_minimum_size = Vector2(0, 164)
	hero.add_theme_stylebox_override("panel", ThemeKit.soft_panel(BLUE, 24, 18))
	body.add_child(hero)

	var hero_row := HBoxContainer.new()
	hero_row.alignment = BoxContainer.ALIGNMENT_CENTER
	hero_row.add_theme_constant_override("separation", 8)
	hero.add_child(hero_row)

	var hero_text := VBoxContainer.new()
	hero_text.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	hero_text.alignment = BoxContainer.ALIGNMENT_CENTER
	hero_text.add_theme_constant_override("separation", 6)
	hero_row.add_child(hero_text)

	var routine_badge := _pill(I18n.t("for_you") + "  |  3 min", Color(1, 1, 1, 0.16), Color.WHITE, 11)
	routine_badge.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	hero_text.add_child(routine_badge)

	var greeting := _label(I18n.t("home_greeting"), 23, Color.WHITE, HORIZONTAL_ALIGNMENT_LEFT, true)
	greeting.custom_minimum_size = Vector2(178, 0)
	hero_text.add_child(greeting)

	var sub := _label(I18n.t("home_sub"), 12, Color(1, 1, 1, 0.80), HORIZONTAL_ALIGNMENT_LEFT, true)
	hero_text.add_child(sub)

	var streak := _pill("1 " + I18n.t("streak"), Color(0.09, 0.14, 0.34, 0.16), Color.WHITE, 11)
	streak.size_flags_horizontal = Control.SIZE_SHRINK_BEGIN
	hero_text.add_child(streak)

	var avatar := MallowAvatar.new()
	avatar.mood = "good"
	avatar.custom_minimum_size = Vector2(94, 94)
	avatar.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	avatar.size_flags_vertical = Control.SIZE_SHRINK_CENTER
	hero_row.add_child(avatar)
	if SaveStore.assessment_was_skipped():
		var skipped_hint := _pill(I18n.t("assessment_skipped_hint"), ThemeKit.AMBER_SOFT, ThemeKit.AMBER, 11)
		skipped_hint.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		body.add_child(skipped_hint)

	body.add_child(_section_heading(I18n.t("mission"), str(SaveStore.mission_count()) + "/3"))
	var mission := PanelContainer.new()
	mission.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 18, 14, false))
	body.add_child(mission)

	var mission_row := HBoxContainer.new()
	mission_row.alignment = BoxContainer.ALIGNMENT_CENTER
	mission_row.add_theme_constant_override("separation", 12)
	mission.add_child(mission_row)

	var mission_text := VBoxContainer.new()
	mission_text.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	mission_text.add_theme_constant_override("separation", 8)
	mission_row.add_child(mission_text)
	mission_text.add_child(_label(I18n.t("mission_progress"), 14, INK))

	var progress := ProgressBar.new()
	progress.max_value = 3
	progress.value = SaveStore.mission_count()
	progress.show_percentage = false
	progress.custom_minimum_size = Vector2(0, 8)
	progress.add_theme_stylebox_override("background", ThemeKit.box(Color("#edf0f6"), 5))
	progress.add_theme_stylebox_override("fill", ThemeKit.box(TEAL, 5))
	mission_text.add_child(progress)
	mission_row.add_child(_pill(str(SaveStore.mission_count()) + " / 3", ThemeKit.TEAL_SOFT, TEAL, 12))

	body.add_child(_section_heading(I18n.t("for_you"), "3"))
	body.add_child(_label(I18n.t("for_you_desc"), 12, MUTED, HORIZONTAL_ALIGNMENT_LEFT, true))
	var recommendations := RecommendationEngine.recommended(3)
	for i in range(recommendations.size()):
		body.add_child(_recommended_card(recommendations[i], i + 1))

	var browse := _button(I18n.t("browse_games") + "  >", Color.WHITE, 52)
	browse.add_theme_color_override("font_color", BLUE)
	browse.add_theme_color_override("font_hover_color", ThemeKit.BLUE_DARK)
	browse.pressed.connect(show_games)
	body.add_child(browse)

func show_games() -> void:
	_set_chrome("games", I18n.t("games"))
	_render_games_body(false)

func _render_games_body(preserve_scroll: bool) -> void:
	var previous_scroll := scroll.scroll_vertical
	_clear_body()
	body.add_child(_eyebrow("PLAY MALLOW"))
	body.add_child(_section_heading(I18n.t("all_games"), str(GameCatalog.all().size())))
	body.add_child(_label(I18n.t("category_hint"), 13, MUTED, HORIZONTAL_ALIGNMENT_LEFT, true))

	var category_panel := PanelContainer.new()
	category_panel.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 22, 10, true))
	body.add_child(category_panel)
	var category_grid := GridContainer.new()
	category_grid.columns = 4
	category_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	category_grid.add_theme_constant_override("h_separation", 6)
	category_grid.add_theme_constant_override("v_separation", 6)
	category_panel.add_child(category_grid)
	for category in GameCatalog.categories():
		category_grid.add_child(_category_tile(category))

	var active_category := _selected_category_data()
	if not active_category.is_empty():
		body.add_child(_selected_category_header(active_category))
		var game_grid := GridContainer.new()
		game_grid.columns = 3
		game_grid.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		game_grid.add_theme_constant_override("h_separation", 8)
		game_grid.add_theme_constant_override("v_separation", 8)
		for game in GameCatalog.games_for_category(selected_category):
			game_grid.add_child(_game_icon_tile(game))
		body.add_child(game_grid)
	var settings := _button(I18n.t("settings"), Color.WHITE, 52)
	settings.add_theme_color_override("font_color", MUTED)
	settings.pressed.connect(show_settings)
	body.add_child(settings)
	if preserve_scroll:
		scroll.call_deferred("set", "scroll_vertical", previous_scroll)

func _select_category(category_id: String) -> void:
	AudioDirector.tap()
	selected_category = category_id
	_render_games_body(false)

func show_records() -> void:
	_set_chrome("records", I18n.t("records"))
	_clear_body()
	body.add_child(_eyebrow("MY MALLOW"))
	body.add_child(_label(I18n.t("records"), 24, INK))

	var summary := PanelContainer.new()
	summary.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 20, 18))
	body.add_child(summary)
	var summary_row := HBoxContainer.new()
	summary_row.add_theme_constant_override("separation", 8)
	summary.add_child(summary_row)
	summary_row.add_child(_stat(I18n.t("plays"), str(SaveStore.total_plays())))
	summary_row.add_child(_stat(I18n.t("mission"), str(SaveStore.mission_count()) + "/3"))

	body.add_child(_skills_panel())
	body.add_child(_section_heading(I18n.t("best"), str(GameCatalog.all().size())))
	var games := GameCatalog.all()
	for i in range(games.size()):
		var game: Dictionary = games[i]
		var card := PanelContainer.new()
		card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 18, 14, false))
		body.add_child(card)

		var row := HBoxContainer.new()
		row.alignment = BoxContainer.ALIGNMENT_CENTER
		row.add_theme_constant_override("separation", 12)
		card.add_child(row)
		row.add_child(_number_badge(i + 1, Color(game["color"])))

		var name_box := VBoxContainer.new()
		name_box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		name_box.add_theme_constant_override("separation", 2)
		name_box.add_child(_label(I18n.t(game["name_key"]), 16, INK))
		name_box.add_child(_label(str(game["axis"]), 11, MUTED))
		row.add_child(name_box)

		var score_box := VBoxContainer.new()
		score_box.add_theme_constant_override("separation", 1)
		score_box.add_child(_label(str(SaveStore.get_best(game["id"])), 20, BLUE, HORIZONTAL_ALIGNMENT_RIGHT))
		score_box.add_child(_label(I18n.t("score"), 10, SUBTLE, HORIZONTAL_ALIGNMENT_RIGHT))
		row.add_child(score_box)

func show_settings() -> void:
	_set_chrome("settings", I18n.t("settings"))
	_clear_body()
	body.add_child(_eyebrow("PLAY FEEL"))
	body.add_child(_label(I18n.t("settings"), 24, INK))
	body.add_child(_label(I18n.t("settings_hint"), 13, MUTED, HORIZONTAL_ALIGNMENT_LEFT, true))
	for setting in [
		{"key": "sound", "label": "sound"},
		{"key": "music", "label": "music"},
		{"key": "haptics", "label": "haptics"}
	]:
		body.add_child(_setting_row(str(setting["key"]), str(setting["label"])))
	var lang_button := _button(I18n.t("language") + "    " + (I18n.t("korean") if I18n.language == "ko" else I18n.t("english")), Color.WHITE, 56)
	lang_button.alignment = HORIZONTAL_ALIGNMENT_LEFT
	lang_button.add_theme_color_override("font_color", BLUE)
	lang_button.pressed.connect(_toggle_language)
	body.add_child(lang_button)
	var retake := _button(I18n.t("assessment_retake"), ThemeKit.BLUE_SOFT, 54)
	retake.add_theme_color_override("font_color", BLUE)
	retake.add_theme_color_override("font_hover_color", ThemeKit.BLUE_DARK)
	retake.pressed.connect(_restart_assessment)
	body.add_child(retake)

func _setting_row(key: String, label_key: String) -> Control:
	var card := PanelContainer.new()
	card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 18, 14, false))
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 12)
	card.add_child(row)
	var text := _label(I18n.t(label_key), 15, INK)
	text.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(text)
	var toggle := CheckButton.new()
	toggle.text = ""
	toggle.button_pressed = bool(SaveStore.get_setting(key, true))
	toggle.custom_minimum_size = Vector2(54, 44)
	toggle.toggled.connect(_setting_changed.bind(key))
	row.add_child(toggle)
	return card

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

func show_assessment() -> void:
	_set_chrome("assessment", I18n.t("brand"))
	nav_panel.visible = false
	_clear_body()
	assessment_flow = AssessmentFlow.new()
	assessment_flow.completed.connect(_assessment_completed)
	assessment_flow.skipped.connect(_assessment_skipped)
	assessment_flow.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	body.add_child(assessment_flow)

func _assessment_completed(scores: Dictionary) -> void:
	SaveStore.save_assessment(scores, "baseline")
	_show_assessment_result(scores)

func _assessment_skipped() -> void:
	SaveStore.save_assessment({"memory": 50, "focus": 50, "calculation": 50, "coordination": 50}, "skipped")
	show_home()

func _input(event: InputEvent) -> void:
	if current_screen != "home" and current_screen != "games" and current_screen != "records":
		return
	if event is InputEventScreenTouch:
		if event.pressed:
			drag_scrolling = true
			drag_moved = false
		elif not event.pressed:
			if drag_moved:
				get_viewport().set_input_as_handled()
			drag_scrolling = false
	elif event is InputEventScreenDrag and drag_scrolling:
		if abs(event.relative.y) > 1.0:
			drag_moved = true
			scroll.scroll_vertical = maxi(0, scroll.scroll_vertical - int(event.relative.y))
			get_viewport().set_input_as_handled()
	elif event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
		if event.pressed:
			drag_scrolling = true
			drag_moved = false
		elif not event.pressed:
			if drag_moved:
				get_viewport().set_input_as_handled()
			drag_scrolling = false
	elif event is InputEventMouseMotion and drag_scrolling:
		if abs(event.relative.y) > 1.0:
			drag_moved = true
			scroll.scroll_vertical = maxi(0, scroll.scroll_vertical - int(event.relative.y))
			get_viewport().set_input_as_handled()

func show_assessment_result(scores: Dictionary) -> void:
	_show_assessment_result(scores)

func _show_assessment_result(scores: Dictionary) -> void:
	_set_chrome("assessment_result", I18n.t("brand"))
	nav_panel.visible = false
	_clear_body()
	var result_card := PanelContainer.new()
	result_card.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 26, 20))
	body.add_child(result_card)
	var result_box := VBoxContainer.new()
	result_box.alignment = BoxContainer.ALIGNMENT_CENTER
	result_box.add_theme_constant_override("separation", 8)
	result_card.add_child(result_box)
	var avatar := MallowAvatar.new()
	avatar.mood = "win"
	avatar.custom_minimum_size = Vector2(104, 104)
	avatar.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	result_box.add_child(avatar)
	result_box.add_child(_label(I18n.t("assessment_result_title"), 23, INK, HORIZONTAL_ALIGNMENT_CENTER, true))
	result_box.add_child(_label(I18n.t("assessment_result_desc"), 13, MUTED, HORIZONTAL_ALIGNMENT_CENTER, true))

	body.add_child(_skills_panel(scores))
	body.add_child(_section_heading(I18n.t("for_you"), "3"))
	var recommendations := RecommendationEngine.recommended(3)
	for i in range(recommendations.size()):
		body.add_child(_recommended_card(recommendations[i], i + 1))
	if not recommendations.is_empty():
		var start := _button(I18n.t("assessment_result_start") + "  >", BLUE, 58)
		start.add_theme_color_override("font_color", Color.WHITE)
		start.add_theme_color_override("font_hover_color", Color.WHITE)
		start.pressed.connect(_launch_recommended.bind(recommendations[0]))
		body.add_child(start)
	var home := _button(I18n.t("assessment_result_home"), Color.WHITE, 50)
	home.add_theme_color_override("font_color", MUTED)
	home.pressed.connect(show_home)
	body.add_child(home)

func _launch_recommended(item: Dictionary) -> void:
	var game: Dictionary = item.get("game", {})
	if not game.is_empty():
		_launch_game(str(game["id"]))

func _restart_assessment() -> void:
	AudioDirector.tap()
	SaveStore.reset_assessment()
	show_assessment()

func _launch_game(game_id: String) -> void:
	AudioDirector.tap()
	current_game_id = game_id
	current_screen = "game"
	header_title.text = I18n.t(GameCatalog.get_game(game_id)["name_key"])
	header_back.visible = true
	header_avatar.visible = false
	nav_panel.visible = false
	_clear_body()
	var game_script = load(GameCatalog.script_path(game_id))
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
	result_card.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 24, 22))
	body.add_child(result_card)
	var result_box := VBoxContainer.new()
	result_box.alignment = BoxContainer.ALIGNMENT_CENTER
	result_box.add_theme_constant_override("separation", 8)
	result_card.add_child(result_box)

	var avatar := MallowAvatar.new()
	avatar.mood = "win" if is_new else "good"
	avatar.custom_minimum_size = Vector2(104, 104)
	avatar.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	result_box.add_child(avatar)
	result_box.add_child(_label(I18n.t("new_record") if is_new else I18n.t("correct"), 18, BLUE, HORIZONTAL_ALIGNMENT_CENTER, true))
	result_box.add_child(_label(str(score), 44, INK, HORIZONTAL_ALIGNMENT_CENTER))
	result_box.add_child(_label(I18n.t("score"), 11, MUTED, HORIZONTAL_ALIGNMENT_CENTER))
	result_box.add_child(_label(detail, 13, MUTED, HORIZONTAL_ALIGNMENT_CENTER, true))
	result_box.add_child(_label(I18n.t("result_detail"), 12, MUTED, HORIZONTAL_ALIGNMENT_CENTER, true))

	var next := _button(I18n.t("next") + "  >", BLUE, 58)
	next.add_theme_color_override("font_color", Color.WHITE)
	next.add_theme_color_override("font_hover_color", Color.WHITE)
	next.pressed.connect(_next_game.bind(game_id))
	body.add_child(next)
	var home := _button(I18n.t("go_home"), Color.WHITE, 52)
	home.add_theme_color_override("font_color", MUTED)
	home.pressed.connect(show_home)
	body.add_child(home)

func _next_game(game_id: String) -> void:
	var games := GameCatalog.all()
	for i in range(games.size()):
		if games[i]["id"] == game_id:
			_launch_game(games[(i + 1) % games.size()]["id"])
			return

func _recommended_card(item: Dictionary, number: int) -> Control:
	var game: Dictionary = item.get("game", {})
	var color := Color(str(game.get("color", "#4c6fff")))
	var card := PanelContainer.new()
	card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 20, 12, true))
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 10)
	card.add_child(row)
	row.add_child(_number_badge(number, color))
	var info := VBoxContainer.new()
	info.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	info.add_theme_constant_override("separation", 3)
	row.add_child(info)
	info.add_child(_label(I18n.t(str(game.get("name_key", ""))), 16, INK))
	var axis_line := _label(RecommendationEngine.axis_label(str(item.get("axis_key", "memory"))) + "  ·  " + RecommendationEngine.reason_text(item), 11, MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
	info.add_child(axis_line)
	var skill_bar := ProgressBar.new()
	skill_bar.max_value = 100
	skill_bar.value = int(item.get("skill", 50))
	skill_bar.show_percentage = false
	skill_bar.custom_minimum_size = Vector2(0, 7)
	skill_bar.add_theme_stylebox_override("background", ThemeKit.box(Color("#edf0f6"), 8))
	skill_bar.add_theme_stylebox_override("fill", ThemeKit.box(color, 8))
	info.add_child(skill_bar)
	var play := _button(">", color.lightened(0.38), 48)
	play.custom_minimum_size = Vector2(48, 48)
	play.add_theme_font_size_override("font_size", 22)
	play.add_theme_color_override("font_color", color.darkened(0.16))
	play.add_theme_color_override("font_hover_color", color.darkened(0.16))
	play.pressed.connect(_launch_recommended.bind(item))
	row.add_child(play)
	return card

func _skills_panel(scores: Dictionary = {}) -> Control:
	var values := SaveStore.get_skill_scores()
	if not scores.is_empty():
		for key in scores:
			values[key] = int(scores[key])
	var panel := PanelContainer.new()
	panel.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 20, 14, false))
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 9)
	panel.add_child(box)
	box.add_child(_label(I18n.t("skill_now"), 14, INK))
	for axis in ["memory", "focus", "calculation", "coordination", "speed", "space", "logic", "language", "sound", "sight"]:
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 8)
		var name := _label(I18n.t("skill_" + axis), 12, MUTED)
		name.custom_minimum_size = Vector2(86, 0)
		row.add_child(name)
		var bar := ProgressBar.new()
		bar.max_value = 100
		bar.value = int(values.get(axis, 50))
		bar.show_percentage = false
		bar.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		bar.custom_minimum_size = Vector2(0, 8)
		bar.add_theme_stylebox_override("background", ThemeKit.box(Color("#edf0f6"), 8))
		bar.add_theme_stylebox_override("fill", ThemeKit.box(ThemeKit.TEAL, 8))
		row.add_child(bar)
		row.add_child(_label(str(int(values.get(axis, 50))), 12, ThemeKit.TEAL, HORIZONTAL_ALIGNMENT_RIGHT))
		box.add_child(row)
	box.add_child(_label(I18n.t("skill_hint"), 10, SUBTLE, HORIZONTAL_ALIGNMENT_LEFT, true))
	return panel

func _category_tile(category: Dictionary) -> Control:
	var category_id := str(category["id"])
	var color := Color(category["color"])
	var selected := selected_category == category_id
	var button := _button("", color.lightened(0.47) if selected else Color("#f7f8fc"), 78)
	button.custom_minimum_size = Vector2(0, 78)
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.add_theme_stylebox_override("normal", ThemeKit.button_style(color.lightened(0.47) if selected else Color("#f7f8fc"), 16, color.lightened(0.16) if selected else Color("#e9edf5")))
	button.add_theme_stylebox_override("hover", ThemeKit.button_style(color.lightened(0.51), 16, color.lightened(0.12)))
	button.add_theme_stylebox_override("pressed", ThemeKit.button_style(color.lightened(0.38), 16, color))
	button.pressed.connect(_select_category.bind(category_id))

	var stack := VBoxContainer.new()
	stack.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	stack.alignment = BoxContainer.ALIGNMENT_CENTER
	stack.add_theme_constant_override("separation", 2)
	stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
	button.add_child(stack)
	var icon := GameIconControl.new().configure(str(category["icon"]), color, 31, false)
	icon.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	stack.add_child(icon)
	var label := _label(I18n.t(str(category["name_key"])), 10, color.darkened(0.20) if selected else INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	label.custom_minimum_size = Vector2(0, 24)
	label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stack.add_child(label)
	return button

func _selected_category_data() -> Dictionary:
	for category in GameCatalog.categories():
		if str(category["id"]) == selected_category:
			return category
	return {}

func _selected_category_header(category: Dictionary) -> Control:
	var color := Color(category["color"])
	var games := GameCatalog.games_for_category(str(category["id"]))
	var panel := PanelContainer.new()
	panel.custom_minimum_size = Vector2(0, 60)
	panel.add_theme_stylebox_override("panel", ThemeKit.soft_panel(color, 19, 10))
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	row.add_theme_constant_override("separation", 10)
	panel.add_child(row)
	row.add_child(GameIconControl.new().configure(str(category["icon"]), color, 38, true))
	var title := _label(I18n.t(str(category["name_key"])), 17, INK)
	title.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(title)
	row.add_child(_pill(I18n.t("category_count") % games.size(), Color(1, 1, 1, 0.72), color.darkened(0.18), 10))
	return panel

func _game_icon_tile(game: Dictionary) -> Control:
	var color := Color(game["color"])
	var button := _button("", Color.WHITE, 110)
	button.custom_minimum_size = Vector2(0, 110)
	button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	button.add_theme_stylebox_override("normal", ThemeKit.button_style(Color.WHITE, 20, Color("#e5e9f2")))
	button.add_theme_stylebox_override("hover", ThemeKit.button_style(color.lightened(0.52), 20, color.lightened(0.20)))
	button.add_theme_stylebox_override("pressed", ThemeKit.button_style(color.lightened(0.42), 20, color))
	button.pressed.connect(_launch_game.bind(game["id"]))

	var stack := VBoxContainer.new()
	stack.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	stack.alignment = BoxContainer.ALIGNMENT_CENTER
	stack.add_theme_constant_override("separation", 5)
	stack.mouse_filter = Control.MOUSE_FILTER_IGNORE
	button.add_child(stack)

	var icon := GameIconControl.new().configure(str(game["id"]), color, 50)
	icon.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
	stack.add_child(icon)
	var name := _label(I18n.t(str(game["name_key"])), 11, INK, HORIZONTAL_ALIGNMENT_CENTER, true)
	name.custom_minimum_size = Vector2(0, 30)
	name.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stack.add_child(name)
	return button

func _section_heading(title: String, meta: String) -> Control:
	var row := HBoxContainer.new()
	row.alignment = BoxContainer.ALIGNMENT_CENTER
	var left := _label(title, 17, INK)
	left.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	row.add_child(left)
	row.add_child(_label(meta, 12, MUTED, HORIZONTAL_ALIGNMENT_RIGHT))
	return row

func _stat(label_text: String, value: String) -> Control:
	var box := VBoxContainer.new()
	box.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	box.add_theme_constant_override("separation", 2)
	box.add_child(_label(value, 28, BLUE, HORIZONTAL_ALIGNMENT_CENTER))
	box.add_child(_label(label_text, 11, MUTED, HORIZONTAL_ALIGNMENT_CENTER))
	return box

func _number_badge(number: int, color: Color) -> Label:
	return _pill("%02d" % number, color.lightened(0.42), color.darkened(0.15), 11)

func _eyebrow(text_value: String) -> Label:
	var label := _label(text_value, 10, BLUE)
	label.add_theme_constant_override("letter_spacing", 1)
	return label

func _pill(text_value: String, fill: Color, color: Color, font_size: int) -> Label:
	var label := _label(text_value, font_size, color, HORIZONTAL_ALIGNMENT_CENTER)
	var style := ThemeKit.box(fill, 20)
	style.content_margin_left = 10
	style.content_margin_right = 10
	style.content_margin_top = 5
	style.content_margin_bottom = 5
	label.add_theme_stylebox_override("normal", style)
	return label

func _label(
	text_value: String,
	font_size: int,
	color: Color,
	align: HorizontalAlignment = HORIZONTAL_ALIGNMENT_LEFT,
	wrap: bool = false
) -> Label:
	var label := Label.new()
	label.text = text_value
	label.add_theme_font_size_override("font_size", font_size)
	label.add_theme_color_override("font_color", color)
	label.horizontal_alignment = align
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	if wrap:
		label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		label.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	else:
		label.autowrap_mode = TextServer.AUTOWRAP_OFF
	return label

func _button(text_value: String, fill: Color, height: int) -> Button:
	var button := Button.new()
	button.text = text_value
	button.custom_minimum_size = Vector2(0, height)
	button.add_theme_font_size_override("font_size", 15)
	button.add_theme_color_override("font_color", INK)
	button.add_theme_color_override("font_hover_color", INK)
	button.add_theme_color_override("font_pressed_color", INK)
	button.add_theme_stylebox_override("normal", ThemeKit.button_style(fill, 16, ThemeKit.BORDER if fill == Color.WHITE else Color.TRANSPARENT))
	button.add_theme_stylebox_override("hover", ThemeKit.button_style(fill.lightened(0.035), 16, ThemeKit.BORDER if fill == Color.WHITE else Color.TRANSPARENT))
	button.add_theme_stylebox_override("pressed", ThemeKit.button_style(fill.darkened(0.04), 16))
	button.add_theme_stylebox_override("focus", ThemeKit.button_style(fill, 16, BLUE))
	button.text_overrun_behavior = TextServer.OVERRUN_TRIM_ELLIPSIS
	return button
