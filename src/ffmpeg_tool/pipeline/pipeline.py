from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from ..operations.base import Operation


@dataclass
class PipelineNode:
    id: int
    operation: Operation
    dependencies: set[int] = field(
        default_factory=set
    )


class Pipeline:
    """
    Represents a directed acyclic graph of FFmpeg operations.
    """

    def __init__(self):
        self._nodes: dict[int, PipelineNode] = {}
        self._next_id = 0

    def add(
        self,
        operation: Operation,
        *,
        depends_on: Iterable[int | PipelineNode] | None = None,
    ) -> PipelineNode:

        node_id = self._next_id
        self._next_id += 1

        dependencies: set[int] = set()

        if depends_on:
            for dependency in depends_on:
                if isinstance(dependency, PipelineNode):
                    dependencies.add(dependency.id)
                else:
                    dependencies.add(dependency)

        node = PipelineNode(
            id=node_id,
            operation=operation,
            dependencies=dependencies,
        )

        self._nodes[node_id] = node

        return node

    @property
    def nodes(self) -> list[PipelineNode]:
        return list(self._nodes.values())

    def get_ready_nodes(
        self,
        completed: set[int],
        running: set[int],
    ) -> list[PipelineNode]:

        ready = []

        for node in self._nodes.values():

            if node.id in completed:
                continue

            if node.id in running:
                continue

            if node.dependencies.issubset(completed):
                ready.append(node)

        return ready

    def validate(self) -> None:
        """
        Detect invalid dependencies and cycles.
        """

        for node in self._nodes.values():

            for dependency in node.dependencies:

                if dependency not in self._nodes:
                    raise ValueError(
                        f"Unknown dependency: {dependency}"
                    )

        # Cycle detection
        visited = set()
        visiting = set()

        def visit(node_id: int):

            if node_id in visiting:
                raise ValueError(
                    "Pipeline contains a cycle."
                )

            if node_id in visited:
                return

            visiting.add(node_id)

            node = self._nodes[node_id]

            for dependency in node.dependencies:
                visit(dependency)

            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in self._nodes:
            visit(node_id)