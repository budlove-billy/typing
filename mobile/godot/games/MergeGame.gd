extends Control

signal finished(result: Dictionary)

const GameTools = preload("res://scripts/GameTools.gd")
const SIZE := 4
const MAX_MOVES := 24

var grid: GridContainer
var status: Label
var move_label: Label
var board: Array[int] = []
var score := 0
var moves := 0
var locked := false
var rng := RandomNumberGenerator.new()

func _ready() -> void:
    rng.randomize()
    _build()
    _new_game()

func _build() -> void:
    var root := VBoxContainer.new()
    root.add_theme_constant_override("separation", 12)
    root.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
    add_child(root)
    var intro := PanelContainer.new()
    intro.add_theme_stylebox_override("panel", ThemeKit.soft_panel(ThemeKit.AMBER_SOFT, 18, 14))
    root.add_child(intro)
    var intro_box := VBoxContainer.new()
    intro_box.add_theme_constant_override("separation", 4)
    intro.add_child(intro_box)
    intro_box.add_child(GameTools.label("CALCULATION  |  MERGE", 10, ThemeKit.AMBER))
    intro_box.add_child(GameTools.label(I18n.t("merge_ready"), 15, ThemeKit.INK, HORIZONTAL_ALIGNMENT_LEFT, true))
    var row := HBoxContainer.new()
    root.add_child(row)
    status = GameTools.label(I18n.t("merge_round_ready"), 13, ThemeKit.MUTED, HORIZONTAL_ALIGNMENT_LEFT, true)
    status.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    row.add_child(status)
    move_label = GameTools.pill("0 / 24", ThemeKit.AMBER_SOFT, ThemeKit.AMBER)
    row.add_child(move_label)
    grid = GridContainer.new()
    grid.columns = SIZE
    grid.size_flags_vertical = Control.SIZE_EXPAND_FILL
    grid.add_theme_constant_override("h_separation", 8)
    grid.add_theme_constant_override("v_separation", 8)
    root.add_child(grid)
    var directions := HBoxContainer.new()
    directions.add_theme_constant_override("separation", 8)
    root.add_child(directions)
    for item in [["←", 0], ["↑", 2], ["↓", 3], ["→", 1]]:
        var button: Button = GameTools.button(str(item[0]), ThemeKit.BLUE_SOFT, ThemeKit.BLUE, 58, ThemeKit.BLUE)
        button.add_theme_font_size_override("font_size", 22)
        button.pressed.connect(_move.bind(int(item[1]), button))
        directions.add_child(button)
    root.add_child(GameTools.label(I18n.t("merge_hint"), 10, ThemeKit.SUBTLE, HORIZONTAL_ALIGNMENT_CENTER))

func _new_game() -> void:
    board.clear()
    board.resize(SIZE * SIZE)
    for i in range(board.size()):
        board[i] = 0
    score = 0
    moves = 0
    locked = false
    _add_tile()
    _add_tile()
    _render()

func _add_tile() -> void:
    var empty: Array[int] = []
    for index in range(board.size()):
        if board[index] == 0:
            empty.append(index)
    if empty.is_empty():
        return
    var index: int = empty[rng.randi_range(0, empty.size() - 1)]
    board[index] = 4 if rng.randf() < 0.12 else 2

func _render() -> void:
    for child in grid.get_children():
        child.queue_free()
    for value in board:
        var fill := ThemeKit.BLUE_SOFT if value == 0 else ThemeKit.AMBER_SOFT
        var ink := ThemeKit.SUBTLE if value == 0 else ThemeKit.AMBER
        var button: Button = GameTools.button("" if value == 0 else str(value), fill, ink, 70, ThemeKit.AMBER)
        button.add_theme_font_size_override("font_size", 22 if value < 100 else 18)
        button.disabled = true
        grid.add_child(button)
    move_label.text = "%d / %d" % [moves, MAX_MOVES]

func _move(direction: int, button: Button) -> void:
    if locked or moves >= MAX_MOVES:
        return
    GameTools.animate_press(button)
    var changed := false
    if direction == 0 or direction == 1:
        for row in range(SIZE):
            var line: Array[int] = []
            for col in range(SIZE):
                var index := row * SIZE + (col if direction == 0 else SIZE - 1 - col)
                line.append(board[index])
            var shifted := _slide_line(line)
            for col in range(SIZE):
                var target_col := col if direction == 0 else SIZE - 1 - col
                var target_index := row * SIZE + target_col
                if board[target_index] != shifted[col]:
                    changed = true
                board[target_index] = shifted[col]
    else:
        for col in range(SIZE):
            var line: Array[int] = []
            for row in range(SIZE):
                var index := (row if direction == 2 else SIZE - 1 - row) * SIZE + col
                line.append(board[index])
            var shifted := _slide_line(line)
            for row in range(SIZE):
                var target_row := row if direction == 2 else SIZE - 1 - row
                var target_index := target_row * SIZE + col
                if board[target_index] != shifted[row]:
                    changed = true
                board[target_index] = shifted[row]
    if not changed:
        status.text = I18n.t("merge_no_move")
        return
    moves += 1
    _add_tile()
    AudioDirector.tap()
    _render()
    status.text = I18n.t("merge_round_ready")
    if _max_tile() >= 128 or moves >= MAX_MOVES:
        locked = true
        await get_tree().create_timer(0.35).timeout
        _finish()

func _slide_line(line: Array[int]) -> Array[int]:
    var compact: Array[int] = []
    for value in line:
        if value != 0:
            compact.append(value)
    var result: Array[int] = []
    var index := 0
    while index < compact.size():
        if index + 1 < compact.size() and compact[index] == compact[index + 1]:
            var merged := compact[index] * 2
            result.append(merged)
            score += merged
            index += 2
        else:
            result.append(compact[index])
            index += 1
    while result.size() < SIZE:
        result.append(0)
    return result

func _max_tile() -> int:
    var highest := 0
    for value in board:
        highest = maxi(highest, value)
    return highest

func _finish() -> void:
    var normalized := clampf(float(score) / 1800.0, 0.0, 1.0)
    var score_value := clampi(int(round(normalized * 1000.0)), 100, 1000)
    finished.emit({"score": score_value, "detail": "%d · tile %d" % [score, _max_tile()]})
