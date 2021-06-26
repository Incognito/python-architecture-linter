from functools import cache
from pathlib import Path


class File:
    def __init__(self, path: Path):
        self._path = path

    def get_path(self) -> Path:
        return self._path

    def get_contents(self) -> str:
        return self._path.read_text()
