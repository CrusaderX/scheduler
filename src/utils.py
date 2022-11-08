from os import path, walk, getcwd
from types import SimpleNamespace
from typing import Dict


def dict_to_simplenamespace(d: dict) -> SimpleNamespace:
    ns = SimpleNamespace()
    [
        setattr(
            ns,
            k,
            dict_to_simplenamespace(v)
            if isinstance(v, dict)
            else [dict_to_simplenamespace(e) for e in v]
            if isinstance(v, list)
            else v,
        )
        for k, v in d.items()
    ]
    return ns


def files_to_upload(root: str) -> Dict[str, str]:
    f = {}

    for p, subdirs, files in walk(root):
        for name in files:
            file_path = path.join(p, name)
            relative_path = file_path.replace(root + "/", "")
            f.update({file_path: relative_path})
    return f
