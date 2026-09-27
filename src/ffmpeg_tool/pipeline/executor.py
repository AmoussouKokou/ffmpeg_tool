from __future__ import annotations

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from ..core import FFmpegRunner
from ..models import OperationResult
from ..core.exceptions import PipelineError
from .pipeline import Pipeline


class PipelineExecutor:

    def __init__(
        self,
        runner: FFmpegRunner | None = None,
        max_workers: int = 1,
    ):
        self.runner = runner or FFmpegRunner()

        if max_workers < 1:
            raise ValueError(
                "max_workers must be >= 1."
            )

        self.max_workers = max_workers

    def run(
        self,
        pipeline: Pipeline,
    ) -> dict[int, OperationResult]:

        pipeline.validate()

        completed: set[int] = set()
        running: set[int] = set()

        results: dict[int, OperationResult] = {}

        while len(completed) < len(pipeline.nodes):

            ready_nodes = pipeline.get_ready_nodes(
                completed=completed,
                running=running,
            )

            if not ready_nodes:
                raise PipelineError(
                    "No executable operation remains. "
                    "The pipeline may contain a dependency problem."
                )

            # On ne lance pas plus de max_workers opérations.
            batch = ready_nodes[:self.max_workers]

            running.update(
                node.id
                for node in batch
            )

            with ThreadPoolExecutor(
                max_workers=len(batch)
            ) as executor:

                futures = {
                    executor.submit(
                        node.operation.execute,
                        self.runner,
                    ): node
                    for node in batch
                }

                for future in as_completed(futures):

                    node = futures[future]

                    try:
                        result = future.result()

                    except Exception as exc:
                        raise PipelineError(
                            f"Operation {node.id} "
                            f"({node.operation.__class__.__name__}) "
                            f"failed."
                        ) from exc

                    results[node.id] = result

                    running.remove(node.id)
                    completed.add(node.id)

        return results