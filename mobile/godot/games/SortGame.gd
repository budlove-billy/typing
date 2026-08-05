extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const COLORS := [ThemeKit.PINK, ThemeKit.BLUE, ThemeKit.TEAL]
const DOTS := ["●", "●", "●"]

var tubes_box: HBoxContainer
var status: Label
var move_label: Label
var tubes: Array[Array] = []
var tube_buttons: Array[Button] = []
var selected := -1
var moves := 0
var locked := false

func _ready() -> void:
    _build()
    _new_game()

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
    intro_box.add_child(GameTools.label("LOGIC  |  SORT", 10, ThemeKit.TEAL))
    intro_box.add_child(GameTools.label(I18n.t("sort_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("sort_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    move_label = GameTools.pill("0", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(move_label)
    tubes_box = HBoxContainer.new()
    tubes_box.alignment = BoxContainer.ALIGNMENT_CENTER
    tubes_box.add_theme_constant_override("separation", 8)
    tubes_box.size_flags_vertical = Control.SIZE_EXPAND_FILL
    root.add_child(tubes_box)
    root.add_child(GameTools.label(I18n.t("sort_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_game() -> void:
    tubes = [[0, 1, 2], [1, 2, 0], [2, 0, 1], [], []]
    selected = -1
    moves = 0
    locked = false
    _render()

func _render() -> void:
    for child in tubes_box.get_children():
        child.queue_free()
    tube_buttons.clear()
    for index in range(tubes.size()):
        var text_value := ""
        for value_index in range(tubes[index].size() - 1, -1, -1):
            text_value += "●\n"
        if text_value.is_empty():
            text_value = "·"
        var fill := Color("#f0f3f8")
        var ink := ThemeKit.SUBTLE
        if not tubes[index].is_empty():
            ink = COLORS[int(tubes[index][-1])]
        var button: Button = GameTools.button(text_value, fill, ink, 240, ink)
        button.custom_minimum_size = Vector2(64, 240)
        button.add_theme_font_size_override("font_size", 28)
        button.pressed.connect(_tube_pressed.bind(index, button))
        tubes_box.add_child(button)
        tube_buttons.append(button)
    move_label.text = str(moves)

func _tube_pressed(index: int, button: Button) -> void:
    if locked:
        return
    if selected == -1:
        if tubes[index].is_empty():
            return
        selected = index
        GameTools.animate_press(button)
        status.text = I18n.t("sort_target")
        status.add_theme_color_override("font_color", ThemeKit.BLUE)
        return
    if selected == index:
        selected = -1
        status.text = I18n.t("sort_round_ready")
        return
    var source: Array = tubes[selected]
    var target: Array = tubes[index]
    if target.size() >= 4 or (not target.is_empty() and target[-1] != source[-1]):
        AudioDirector.bad()
        status.text = I18n.t("sort_wrong")
        status.add_theme_color_override("font_color", ThemeKit.PINK)
        selected = -1
        return
    target.append(source.pop_back())
    tubes[selected] = source
    tubes[index] = target
    selected = -1
    moves += 1
    AudioDirector.tap()
    _render()
    if _is_solved() or moves >= 28:
        locked = true
        if _is_solved():
            AudioDirector.good()
            status.text = I18n.t("sort_good")
        else:
            status.text = I18n.t("sort_done")
        await get_tree().create_timer(0.4).timeout
        _finish()
    else:
        status.text = I18n.t("sort_round_ready")

func _is_solved() -> bool:
    for tube in tubes:
        if tube.is_empty():
            continue
        if tube.size() != 4:
            return false
        for value in tube:
            if value != tube[0]:
                return false
    return true

func _finish() -> void:
    var score := 100 if not _is_solved() else clampi(1000 - moves * 18, 100, 1000)
    finished.emit({"score": score, "detail": "%d moves" % moves})
