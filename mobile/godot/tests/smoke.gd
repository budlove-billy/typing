extends SceneTree

const GAME_SCRIPTS := [
	"res://games/FlashGame.gd",
	"res://games/BubbleGame.gd",
	"res://games/TraceGame.gd",
	"res://games/ReactGame.gd",
	"res://scripts/AssessmentFlow.gd"
]

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
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
