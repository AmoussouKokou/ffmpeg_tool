from dataclasses import dataclass

from ffmpeg_tool.models import OperationResult
from ffmpeg_tool.operations.base import Operation
from ffmpeg_tool.pipeline import (
    Pipeline,
    PipelineExecutor,
)


@dataclass
class FakeOperation(Operation):

    output_path: str

    @property
    def output(self) -> str:
        return self.output_path

    def build_args(self) -> list[str]:
        return []


def test_pipeline_dependencies():

    pipeline = Pipeline()

    first = pipeline.add(
        FakeOperation("first.mp3")
    )

    second = pipeline.add(
        FakeOperation("second.mp3"),
        depends_on=[first],
    )

    assert second.dependencies == {first.id}


def test_pipeline_validation():

    pipeline = Pipeline()

    first = pipeline.add(
        FakeOperation("first.mp3")
    )

    pipeline.add(
        FakeOperation("second.mp3"),
        depends_on=[first],
    )

    pipeline.validate()