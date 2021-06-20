from pathlib import Path
from typing import List

from python_architecture_linter.domain_objects.file import File


class ProjectFileScanner:
    def get_files_in_project(self, path: str) -> List[File]:
        paths = Path(path).glob("**/*.py")
        return [File(path) for path in paths]
