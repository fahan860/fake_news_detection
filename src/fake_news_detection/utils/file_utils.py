from pathlib import Path


def resolve_with_legacy(primary_path: Path, legacy_path: Path) -> Path | None:
    if primary_path.exists():
        return primary_path
    if legacy_path.exists():
        return legacy_path
    return None
