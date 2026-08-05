extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const PAIRS := 4
const ROUNDS := 3
const SYMBOLS := ["●", "▲", "■", "◆"]

var grid: GridContainer
var status: Label
var round_label: Label
var cards: Array[int] = []
var buttons: Array[Button] = []
var selected: Array[int] = []
var matched: Array[int] = []
var round_index := 0
var pairs_found := 0
var locked := false
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.randomize()
    _build()
    _new_board()

func _build() -> void:
    var root := VBoxContainer.new()
    root.add_theme_constant_override("separation", 12)
    root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(root)
    var intro := PanelContainer.new()
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.PINK_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("MEMORY  |  MATCH PAIRS", 10, ThemeKit.PINK))
    intro_box.add_child(GameTools.label(I18n.t("cards_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("cards_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 03", ThemeKit.BLUE_SOFT, ThemeKit.BLUE)
    row.add_child(round_label)
    grid = GridContainer.new()
    grid.columns = 4
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 9)
    grid.add_theme_constant_override("v_separation", 9)
    root.add_child(grid)
    root.add_child(GameTools.label("TAP TWO CARDS  •  FIND THE PAIRS", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_board() -> void:
    cards.clear()
    for value in range(PAIRS):
        cards.append(value)
        cards.append(value)
    cards.shuffle()
    buttons.clear()
    selected.clear()
    matched.clear()
    locked = false
    for child in grid.get_children():
        child.queue_free()
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("cards_round_ready")
    for index in range(cards.size()):
        var card: Button = GameTools.button("?", ThemeKit.BLUE_SOFT, ThemeKit.BLUE_DARK, 74, ThemeKit.BLUE)
        card.add_theme_font_size_override("font_size", 28)
        card.pressed.connect(_card_pressed.bind(index, card))
        grid.add_child(card)
        buttons.append(card)

func _card_pressed(index: int, card: Button) -> void:
    if locked or index in matched or index in selected:
        return
    GameTools.animate_press(card)
    card.text = SYMBOLS[cards[index]]
    card.add_theme_stylebox_override("normal", ThemeKit.button_style(ThemeKit.PINK_SOFT, 20, ThemeKit.PINK))
    selected.append(index)
    AudioDirector.tap()
    if selected.size() < 2:
        return
    locked = true
    var first := selected[0]
    var second := selected[1]
    if cards[first] == cards[second]:
        matched.append(first)
        matched.append(second)
        pairs_found += 1
        AudioDirector.good()
        status.text = I18n.t("cards_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
        selected.clear()
        locked = false
        if matched.size() >= cards.size():
            await get_tree().create_timer(0.45).timeout
            round_index += 1
            if round_index >= ROUNDS:
                _finish()
            else:
                _new_board()
    else:
        AudioDirector.bad()
        status.text = I18n.t("cards_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
        await get_tree().create_timer(0.55).timeout
        for value in selected:
            buttons[value].text = "?"
            buttons[value].add_theme_stylebox_override("normal", ThemeKit.button_style(ThemeKit.BLUE_SOFT, 20, ThemeKit.BLUE))
        selected.clear()
        locked = false

func _finish() -> void:
    var score := clampi(int(round(float(pairs_found) / float(PAIRS * ROUNDS) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d %s" % [pairs_found, PAIRS * ROUNDS, I18n.t("cards_pairs") ]})
