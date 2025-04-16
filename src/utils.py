from os import path, walk


def files_to_upload(root: str) -> dict[str, str] | None:
    result = {}

    for p, _, files in walk(root):
        for name in files:
            file_path = path.join(p, name)
            relative_path = file_path.replace(root + "/", "")
            result.update({file_path: relative_path})

    if not result:
        return None

    return result
