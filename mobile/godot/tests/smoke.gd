extends SceneTree

const GAME_SCRIPTS := [
	"res://games/FlashGame.gd",
	"res://games/BubbleGame.gd",
	"res://games/TraceGame.gd",
	"res://games/ReactGame.gd",
	"res://games/SwitchGame.gd",
	"res://games/CountGame.gd",
	"res://games/NbackGame.gd",
	"res://games/CardsGame.gd",
	"res://games/StroopGame.gd",
	"res://games/TrailGame.gd",
	"res://games/FlankGame.gd",
	"res://games/RevGame.gd",
	"res://games/ChopGame.gd",
	"res://games/WhackGame.gd",
	"res://games/SpotGame.gd",
	"res://games/CatchGame.gd",
	"res://games/DiffGame.gd",
	"res://games/OddGame.gd",
	"res://games/RotateGame.gd",
	"res://games/SlideGame.gd",
	"res://games/MelodyGame.gd",
	"res://games/RhythmGame.gd",
	"res://games/PitchGame.gd",
	"res://games/MathGame.gd",
	"res://games/GuessGame.gd",
	"res://games/MergeGame.gd",
	"res://games/SortGame.gd",
	"res://games/NonoGame.gd",
	"res://games/RunGame.gd",
	"res://games/FitGame.gd",
	"res://games/IQGame.gd",
	"res://games/SudokuGame.gd",
	"res://games/AnagramGame.gd",
	"res://games/WordsearchGame.gd",
	"res://games/BraintypeGame.gd",
	"res://games/MoamoaGame.gd",
	"res://games/QueensGame.gd",
	"res://games/TangoGame.gd",
	"res://scripts/AssessmentFlow.gd"
]

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	var catalog = GameCatalog.all()
	if catalog.size() != 38:
		push_error("Expected 38 catalog games, got " + str(catalog.size()))
		quit(1)
		return
	for game in catalog:
		var catalog_script_path := GameCatalog.script_path(str(game["id"]))
		if load(catalog_script_path) == null:
			push_error("Catalog script missing: " + catalog_script_path)
			quit(1)
			return
	print("SMOKE PASS: GameCatalog 38/38 script mappings")
	for script_path in GAME_SCRIPTS:
		var script = load(script_path)
		if script == null:
			push_error("Could not load " + script_path)
			quit(1)
			return
		var game = script.new()
		root.add_child(game)
		await process_frame
		if not is_instance_valid(game):
			push_error("Game instance was freed: " + script_path)
			quit(1)
			return
		game.queue_free()
		await process_frame
		print("SMOKE PASS: " + script_path)
	quit(0)
