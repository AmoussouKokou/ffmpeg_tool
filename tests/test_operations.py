from ffmpeg_tool.operations import (
    ConvertAudio,
    CutAudio,
    CutVideo,
    ImageAudioToVideo,
)


def test_audio_cut_command(tmp_path):

    input_file = tmp_path / "input.mp3"
    output_file = tmp_path / "output.mp3"

    input_file.touch()

    operation = CutAudio(
        input=str(input_file),
        output_path=str(output_file),
        start="00:05:00",
        end="00:10:00",
    )

    args = operation.build_args()

    assert "-ss" in args
    assert "-t" in args
    assert str(input_file) in args
    assert str(output_file) in args


def test_video_cut_command(tmp_path):

    input_file = tmp_path / "input.mp4"
    output_file = tmp_path / "output.mp4"

    input_file.touch()

    operation = CutVideo(
        input=str(input_file),
        output_path=str(output_file),
        start=10,
        end=20,
    )

    args = operation.build_args()

    assert "-ss" in args
    assert "-t" in args


def test_audio_conversion(tmp_path):

    input_file = tmp_path / "input.wav"
    output_file = tmp_path / "output.mp3"

    input_file.touch()

    operation = ConvertAudio(
        input=str(input_file),
        output_path=str(output_file),
        codec="libmp3lame",
        quality=0,
    )

    args = operation.build_args()

    assert "libmp3lame" in args
    assert "0" in args


def test_image_audio_video(tmp_path):

    image = tmp_path / "image.jpg"
    audio = tmp_path / "audio.mp3"
    output = tmp_path / "video.mp4"

    image.touch()
    audio.touch()

    operation = ImageAudioToVideo(
        image=str(image),
        audio=str(audio),
        output_path=str(output),
    )

    args = operation.build_args()

    assert "-loop" in args
    assert str(image) in args
    assert str(audio) in args
    assert str(output) in args