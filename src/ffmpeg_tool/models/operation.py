from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class OperationResult:
    operation_name: str
    output: str
    command: list[str]
    duration: float
    return_code: int
    metadata: dict = field(default_factory=dict)