from pathlib import Path


class File:
    def __init__(self, path: Path):
        self._path = path
        self._contents = None

    def get_path(self):

        return self._path

    def get_contents(self):
        if self._contents is None:
            self._contents = self._path.read_text()

        return self._contents


class ProjectFileScanner:
    def get_files_in_project(self, path: str):
        paths = Path(".").glob("**/*.py")
        return [File(path) for path in paths]
