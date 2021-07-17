import os


def file_to_module(project_path: str, target_file: str) -> str:
    project_file_path = target_file.removeprefix(project_path).removeprefix(os.sep)

    path_parts = project_file_path.split(os.sep)

    path_parts[-1] = path_parts[-1].removesuffix(".py")

    if path_parts[-1] == "__init__":
        path_parts.pop()

    return ".".join(path_parts)
