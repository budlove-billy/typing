extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const SIZE := 4
const SOLUTION := [
    [1, 2, 3, 4],
    [3, 4, 1, 2],
    [2, 1, 4, 3],
    [4, 3, 2, 1]
]
const GIVEN := [0, 2, 5, 7, 8, 10]

var grid: GridContainer
var status: Label
var buttons: Array[Button] = []
var values: Array[int] = []
var taps := 0
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.PINK_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("LOGIC  |  SUDOKU", 10, ThemeKit.PINK))
    intro_box.add_child(GameTools.label(I18n.t("sudoku_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    status = GameTools.label(I18n.t("sudoku_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_CENTER, true)
    root.add_child(status)
    grid = GridContainer.new()
    grid.columns = SIZE
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 7)
    grid.add_theme_constant_override("v_separation", 7)
    root.add_child(grid)
    root.add_child(GameTools.label(I18n.t("sudoku_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_game() -> void:
    locked = false
    taps = 0
    values.clear()
    values.resize(SIZE * SIZE)
    for row in range(SIZE):
        for col in range(SIZE):
            values[row * SIZE + col] = int(SOLUTION[row][col]) if row * SIZE + col in GIVEN else 0
    _render()

func _render() -> void:
    buttons.clear()
    for child in grid.get_children():
        child.queue_free()
    for index in range(values.size()):
        var value := values[index]
        var fixed := index in GIVEN
        var button: Button = GameTools.button("" if value == 0 else str(value), ThemeKit.BLUE_SOFT if fixed else ThemeKit.PINK_SOFT, ThemeKit.BLUE_DARK if fixed else ThemeKit.PINK, 80, ThemeKit.PINK)
        button.add_theme_font_size_override("font_size", 27)
        button.disabled = fixed
        button.pressed.connect(_cell_pressed.bind(index, button))
        grid.add_child(button)
        buttons.append(button)

func _cell_pressed(index: int, cell: Button) -> void:
    if locked:
        return
    values[index] = (values[index] % SIZE) + 1
    taps += 1
    GameTools.animate_press(cell)
    AudioDirector.tap()
    _render()
    if _is_solved():
        locked = true
        AudioDirector.good()
        status.text = I18n.t("sudoku_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
        await get_tree().create_timer(0.45).timeout
        _finish()
    elif taps >= 55:
        locked = true
        status.text = I18n.t("sudoku_done")
        await get_tree().create_timer(0.35).timeout
        _finish()

func _is_solved() -> bool:
    for index in range(values.size()):
        var row := index / SIZE
        var col := index % SIZE
        if values[index] != int(SOLUTION[row][col]):
            return false
    return true

func _finish() -> void:
    var correct := 0
    for index in range(values.size()):
        var row := index / SIZE
        var col := index % SIZE
        if values[index] == int(SOLUTION[row][col]):
            correct += 1
    var score := clampi(int(round(float(correct) / float(SIZE * SIZE) * 1000.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d" % [correct, SIZE * SIZE]})
