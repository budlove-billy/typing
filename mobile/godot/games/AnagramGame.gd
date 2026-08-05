extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const KO_WORDS := ["말랑", "기억", "집중", "퍼즐", "계산", "도형", "소리", "속도"]
const EN_WORDS := ["MALLOW", "MEMORY", "FOCUS", "PUZZLE", "SHAPE", "SOUND", "SPEED", "LOGIC"]
const ROUNDS := 8

var status: Label
var round_label: Label
var answer_label: Label
var letters_box: HBoxContainer
var current_word := ""
var answer := ""
var round_index := 0
var correct_count := 0
var locked := false
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.randomize()
    _build()
    _new_round()

func _build() -> void:
    var root := VBoxContainer.new()
    root.add_theme_constant_override("separation", 12)
    root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(root)
    var intro := PanelContainer.new()
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.BLUE_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("LANGUAGE  |  ANAGRAM", 10, ThemeKit.BLUE))
    intro_box.add_child(GameTools.label(I18n.t("anagram_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("anagram_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 08", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    var answer_card := PanelContainer.new()
    answer_card.custom_minimum_size = Vector2(0, 160)
    answer_card.add_theme_stylebox_override("panel", ThemeKit.panel_style(Color.WHITE, 26, 16, true))
    root.add_child(answer_card)
    answer_label = GameTools.label("", 28, ThemeKit.BLUE_DARK, HORIZONTAL_ALIGNMENT_CENTER)
    answer_label.name = "AnswerLabel"
    answer_label.size_flags_vertical = Control.SIZE_EXPAND_FILL
    answer_card.add_child(answer_label)
    letters_box = HBoxContainer.new()
    letters_box.alignment = BoxContainer.ALIGNMENT_CENTER
    letters_box.add_theme_constant_override("separation", 8)
    root.add_child(letters_box)
    root.add_child(GameTools.label(I18n.t("anagram_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    var words: Array = EN_WORDS if I18n.language == "en" else KO_WORDS
    current_word = str(words[rng.randi_range(0, words.size() - 1)])
    var letters: Array[String] = []
    for letter in current_word:
        letters.append(letter)
    letters.shuffle()
    answer = ""
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("anagram_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    answer_label.text = ""
    for child in letters_box.get_children():
        child.queue_free()
    for index in range(letters.size()):
        var tile: Button = GameTools.button(letters[index], ThemeKit.BLUE_SOFT, ThemeKit.BLUE_DARK, 72, ThemeKit.BLUE)
        tile.custom_minimum_size = Vector2(58, 72)
        tile.add_theme_font_size_override("font_size", 23)
        tile.pressed.connect(_letter_pressed.bind(letters[index], tile))
        letters_box.add_child(tile)

func _letter_pressed(letter: String, tile: Button) -> void:
    if locked:
        return
    GameTools.animate_press(tile)
    tile.disabled = true
    answer += letter
    AudioDirector.tap()
    answer_label.text = answer
    if answer.length() < current_word.length():
        return
    locked = true
    if answer == current_word:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("anagram_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("anagram_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.42).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct_count, ROUNDS]})
