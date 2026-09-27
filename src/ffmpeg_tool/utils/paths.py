from pathlib import Path


def ensure_input_exists(path: str | Path) -> Path:
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Input file does not exist: {path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Input path is not a file: {path}"
        )

    return path


def ensure_output_parent(
    path: str | Path,
) -> Path:

    path = Path(path)

    if path.parent != Path("."):
        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    return path