from pathlib import Path

# IMPORTANT: This path MUST be updated if the file is moved
PROJECT_ROOT = Path(__file__).parent.parent


def project_path(path: Path | str) -> Path:
    if (isinstance(path, Path) and path.anchor != '') or (isinstance(path, str) and path.startswith('/')):
        raise ValueError(f"Input path ({path}) cannot be an absolute path.")

    if isinstance(path, str):
        path = Path(path)
    return PROJECT_ROOT / path
