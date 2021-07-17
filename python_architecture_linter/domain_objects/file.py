from pathlib import Path


class File:
    def __init__(self, path: Path, project_root: Path):
        self._path = path
        self._project_root = project_root

    def get_path(self) -> Path:
        return self._path

    def get_project_root(self) -> Path:
        return self._project_root

    def get_contents(self) -> str:
        return self._path.read_text()
