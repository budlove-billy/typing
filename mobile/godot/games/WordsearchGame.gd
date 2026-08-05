extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const KO_WORDS := ["말랑", "기억", "집중", "퍼즐", "도형"]
const EN_WORDS := ["MALLOW", "FOCUS", "SHAPE", "SOUND", "LOGIC"]
const SIZE := 6
const ROUNDS := 5

var grid: GridContainer
var status: Label
var round_label: Label
var letters: Array[String] = []
var target_word := ""
var target_start := -1
var target_end := -1
var first_pick := -1
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.TEAL_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("LANGUAGE  |  WORD SEARCH", 10, ThemeKit.TEAL))
    intro_box.add_child(GameTools.label(I18n.t("wordsearch_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("wordsearch_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 05", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(round_label)
    grid = GridContainer.new()
    grid.columns = SIZE
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 5)
    grid.add_theme_constant_override("v_separation", 5)
    root.add_child(grid)
    root.add_child(GameTools.label(I18n.t("wordsearch_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_round() -> void:
    locked = false
    first_pick = -1
    var words: Array = EN_WORDS if I18n.language == "en" else KO_WORDS
    target_word = str(words[rng.randi_range(0, words.size() - 1)])
    letters.clear()
    letters.resize(SIZE * SIZE)
    for index in range(letters.size()):
        letters[index] = _random_letter()
    var row := rng.randi_range(0, SIZE - 1)
    var col := rng.randi_range(0, SIZE - target_word.length())
    target_start = row * SIZE + col
    target_end = target_start + target_word.length() - 1
    for offset in range(target_word.length()):
        letters[target_start + offset] = target_word[offset]
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("wordsearch_round_ready") + "  " + target_word
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    _render()

func _random_letter() -> String:
    if I18n.language == "en":
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[rng.randi_range(0, 25)]
    return "가나다라마바사아자차카타파하고노도로모보소오조"[rng.randi_range(0, 21)]

func _render() -> void:
    for child in grid.get_children():
        child.queue_free()
    for index in range(letters.size()):
        var button: Button = GameTools.button(letters[index], ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 55, ThemeKit.TEAL)
        button.custom_minimum_size = Vector2(48, 48)
        button.add_theme_font_size_override("font_size", 19)
        button.pressed.connect(_cell_pressed.bind(index, button))
        grid.add_child(button)

func _cell_pressed(index: int, cell: Button) -> void:
    if locked:
        return
    GameTools.animate_press(cell)
    if first_pick == -1:
        first_pick = index
        status.text = I18n.t("wordsearch_choose_end")
        status.add_theme_color_override("font_color", ThemeKit.BLUE)
        return
    locked = true
    var correct := first_pick == target_start and index == target_end
    if correct:
        correct_count += 1
        AudioDirector.good()
        status.text = I18n.t("wordsearch_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
    else:
        AudioDirector.bad()
        status.text = I18n.t("wordsearch_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
    await get_tree().create_timer(0.4).timeout
    round_index += 1
    if round_index >= ROUNDS:
        _finish()
    else:
        _new_round()

func _finish() -> void:
    var score := clampi(int(round(float(correct_count) / float(ROUNDS) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct_count, ROUNDS]})
