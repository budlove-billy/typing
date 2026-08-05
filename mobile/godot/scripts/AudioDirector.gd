extends Node

var enabled := true
var music_enabled := false
var _player: AudioStreamPlayer
var _playback
const MIX_RATE := 44100.0

func _ready() -> void:
	enabled = bool(SaveStore.get_setting("sound", true))
	music_enabled = bool(SaveStore.get_setting("music", false))
	_create_generator()

func _create_generator() -> void:
	_player = AudioStreamPlayer.new()
	var stream := AudioStreamGenerator.new()
	stream.mix_rate = MIX_RATE
	stream.buffer_length = 0.35
	_player.stream = stream
	add_child(_player)
	_player.play()
	_playback = _player.get_stream_playback()

func set_enabled(value: bool) -> void:
	enabled = value
	SaveStore.set_setting("sound", value)

func set_music_enabled(value: bool) -> void:
	music_enabled = value
	SaveStore.set_setting("music", value)

func _tone(frequency: float, duration: float, volume: float = 0.12, offset: float = 0.0) -> void:
	if not enabled or _playback == null:
		return
	var frames := maxi(1, int(MIX_RATE * duration))
	for i in range(frames):
		var time := float(i) / MIX_RATE
		var envelope := 1.0 - (float(i) / float(frames))
		var sample := sin(TAU * frequency * (time + offset)) * volume * envelope
		_playback.push_frame(Vector2(sample, sample))

func tap() -> void:
	_tone(1380.0, 0.035, 0.045)

func good() -> void:
	_tone(740.0, 0.08, 0.11)
	_tone(988.0, 0.11, 0.10, 0.06)
	_haptic(14)

func bad() -> void:
	_tone(220.0, 0.14, 0.08)
	_haptic(35)

func win() -> void:
	_tone(523.0, 0.10, 0.10)
	_tone(659.0, 0.10, 0.10, 0.08)
	_tone(784.0, 0.20, 0.11, 0.16)
	_haptic(28)

func _haptic(duration_ms: int) -> void:
	if bool(SaveStore.get_setting("haptics", true)) and Input.has_method("vibrate_handheld"):
		Input.vibrate_handheld(duration_ms)
