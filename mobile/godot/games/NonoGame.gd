extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const SIZE := 5
const SOLUTION := [
    [1, 1, 0, 0, 1],
    [0, 1, 1, 1, 0],
    [1, 1, 1, 0, 0],
    [0, 0, 1, 1, 1],
    [1, 0, 0, 1, 1]
]
const ROW_HINTS := ["2 · 1", "3", "3", "3", "1 · 2"]
const COL_HINTS := ["1 · 1 · 1", "3", "3", "1 · 1", "1 · 2"]

var grid: GridContainer
var status: Label
var filled: Array[int] = []
var taps := 0
var locked := false

func _ready() -> void:
    _build()
    _new_game()

func _build() -> void:
    var root := VBoxContainer.new()
    root.add_theme_constant_override("separation", 10)
    root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(root)
    var intro := PanelContainer.new()
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.PINK_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("LOGIC  |  NONOGRAM", 10, ThemeKit.PINK))
    intro_box.add_child(GameTools.label(I18n.t("nono_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    status = GameTools.label(I18n.t("nono_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_CENTER, true)
    root.add_child(status)
    var column_hints := HBoxContainer.new()
    column_hints.alignment = BoxContainer.ALIGNMENT_CENTER
    column_hints.add_theme_constant_override("separation", 6)
    column_hints.add_child(GameTools.label("     ", 11, ThemeKit.SUBTLE))
    for hint in COL_HINTS:
        var label := GameTools.label(hint, 10, ThemeKit.BLUE, HORIZONTAL_ALIGNMENT_CENTER, true)
        label.custom_minimum_size = Vector2(48, 44)
        column_hints.add_child(label)
    root.add_child(column_hints)
    var board_row := HBoxContainer.new()
    board_row.alignment = BoxContainer.ALIGNMENT_CENTER
    board_row.add_theme_constant_override("separation", 6)
    var row_hints := VBoxContainer.new()
    row_hints.add_theme_constant_override("separation", 5)
    for hint in ROW_HINTS:
        var label := GameTools.label(hint, 10, ThemeKit.BLUE, HORIZONTAL_ALIGNMENT_RIGHT)
        label.custom_minimum_size = Vector2(48, 52)
        row_hints.add_child(label)
    board_row.add_child(row_hints)
    grid = GridContainer.new()
    grid.columns = SIZE
    grid.add_theme_constant_override("h_separation", 5)
    grid.add_theme_constant_override("v_separation", 5)
    board_row.add_child(grid)
    root.add_child(board_row)
    root.add_child(GameTools.label(I18n.t("nono_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_game() -> void:
    locked = false
    taps = 0
    filled.clear()
    filled.resize(SIZE * SIZE)
    for i in range(filled.size()):
        filled[i] = 0
    status.text = I18n.t("nono_round_ready")
    _render()

func _render() -> void:
    for child in grid.get_children():
        child.queue_free()
    for index in range(filled.size()):
        var state := filled[index]
        var text_value := "" if state == 0 else ("■" if state == 1 else "×")
        var fill := ThemeKit.PINK_SOFT if state == 1 else Color("#f3f5f8")
        var ink := ThemeKit.PINK if state == 1 else ThemeKit.SUBTLE
        var cell: Button = GameTools.button(text_value, fill, ink, 56, ThemeKit.PINK)
        cell.custom_minimum_size = Vector2(52, 52)
        cell.add_theme_font_size_override("font_size", 22)
        cell.pressed.connect(_cell_pressed.bind(index, cell))
        grid.add_child(cell)

func _cell_pressed(index: int, cell: Button) -> void:
    if locked:
        return
    filled[index] = (filled[index] + 1) % 3
    taps += 1
    GameTools.animate_press(cell)
    AudioDirector.tap()
    _render()
    if _is_solved():
        locked = true
        AudioDirector.good()
        status.text = I18n.t("nono_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
        await get_tree().create_timer(0.45).timeout
        _finish()
    elif taps >= 50:
        locked = true
        status.text = I18n.t("nono_done")
        await get_tree().create_timer(0.35).timeout
        _finish()

func _is_solved() -> bool:
    for row in range(SIZE):
        for col in range(SIZE):
            var index := row * SIZE + col
            if int(SOLUTION[row][col]) == 1 and filled[index] != 1:
                return false
            if int(SOLUTION[row][col]) == 0 and filled[index] == 1:
                return false
    return true

func _finish() -> void:
    var correct := 0
    for row in range(SIZE):
        for col in range(SIZE):
            var index := row * SIZE + col
            if (int(SOLUTION[row][col]) == 1 and filled[index] == 1) or (int(SOLUTION[row][col]) == 0 and filled[index] != 1):
                correct += 1
    var score := clampi(int(round(float(correct) / float(SIZE * SIZE) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct, SIZE * SIZE]})
