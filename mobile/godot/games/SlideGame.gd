extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const SIZE := 3
const ROUNDS := 3

var grid: GridContainer
var status: Label
var round_label: Label
var board: Array[int] = []
var buttons: Array[Button] = []
var blank := 8
var round_index := 0
var moves := 0
var completed := 0
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
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.TEAL_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("SPACE  |  SLIDE", 10, ThemeKit.TEAL))
    intro_box.add_child(GameTools.label(I18n.t("slide_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("slide_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    round_label = GameTools.pill("01 / 03", ThemeKit.TEAL_SOFT, ThemeKit.TEAL)
    row.add_child(round_label)
    grid = GridContainer.new()
    grid.columns = SIZE
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 8)
    grid.add_theme_constant_override("v_separation", 8)
    root.add_child(grid)
    root.add_child(GameTools.label("TAP A TILE NEXT TO THE EMPTY SPACE", 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_board() -> void:
    board.clear()
    for value in range(8):
        board.append(value + 1)
    board.append(0)
    blank = 8
    for shuffle_step in range(28 + round_index * 8):
        var neighbors := _neighbors(blank)
        var pick: int = neighbors[rng.randi_range(0, neighbors.size() - 1)]
        board[blank] = board[pick]
        board[pick] = 0
        blank = pick
    moves = 0
    locked = false
    round_label.text = "%02d / %02d" % [round_index + 1, ROUNDS]
    status.text = I18n.t("slide_round_ready")
    status.add_theme_color_override("font_color", ThemeKit.MUTED)
    _render_board()

func _render_board() -> void:
    buttons.clear()
    for child in grid.get_children():
        child.queue_free()
    for index in range(board.size()):
        var value := board[index]
        var button: Button = GameTools.button("" if value == 0 else str(value), Color("#edf6f2") if value == 0 else ThemeKit.TEAL_SOFT, ThemeKit.TEAL, 76, ThemeKit.TEAL)
        button.add_theme_font_size_override("font_size", 26)
        button.pressed.connect(_tile_pressed.bind(index, button))
        grid.add_child(button)
        buttons.append(button)

func _neighbors(index: int) -> Array[int]:
    var out: Array[int] = []
    var row := index / SIZE
    var col := index % SIZE
    if row > 0: out.append(index - SIZE)
    if row < SIZE - 1: out.append(index + SIZE)
    if col > 0: out.append(index - 1)
    if col < SIZE - 1: out.append(index + 1)
    return out

func _tile_pressed(index: int, button: Button) -> void:
    if locked or index not in _neighbors(blank):
        return
    GameTools.animate_press(button)
    board[blank] = board[index]
    board[index] = 0
    blank = index
    moves += 1
    AudioDirector.tap()
    _render_board()
    if _is_solved():
        locked = true
        completed += 1
        AudioDirector.good()
        status.text = I18n.t("slide_good")
        status.add_theme_color_override("font_color", ThemeKit.TEAL)
        await get_tree().create_timer(0.45).timeout
        round_index += 1
        if round_index >= ROUNDS:
            _finish()
        else:
            _new_board()

func _is_solved() -> bool:
    for i in range(8):
        if board[i] != i + 1:
            return false
    return board[8] == 0

func _finish() -> void:
    var move_bonus := clampf(1.0 - float(moves - ROUNDS * 28) / 150.0, 0.0, 1.0)
    var score := clampi(int(round(float(completed) / float(ROUNDS) * 780.0 + move_bonus * 220.0)), 100, 1000)
    finished.emit({"score": score, "detail": "%d/%d · %d moves" % [completed, ROUNDS, moves]})
