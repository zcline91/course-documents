from pathlib import Path


def compress_directories(item, parent_dir=Path()):
    """Returns a list of endpoint paths based on a nested dict/list/string
    with parent_dir as the root directory"""
    paths = []
    if isinstance(item, str):
        paths.append(parent_dir / item)
    elif isinstance(item, list):
        for d in item:
            if any([isinstance(d, t) for t in (str, dict)]):
                paths.extend(compress_directories(d, parent_dir))
            else:
                raise TypeError('Nested lists are not valid directory structures')
    elif isinstance(item, dict):
        for a, d in item.items():
            new_parent = parent_dir / a
            if any([isinstance(d, t) for t in (str, list, dict)]):
                paths.extend(compress_directories(d, new_parent))
            else:
                raise TypeError('Only lists, dicts, and strs can be passed to compress_directories')
    else:
        raise TypeError('Only lists, dicts, and strs can be passed to compress_directories')
    return paths

def create_directories(item, parent_dir=''):
    """Creates subdirectories of parent_dir based on a nested dict/list/string"""
    for dir in compress_directories(item, parent_dir=parent_dir):
        try:
            Path.mkdir(dir, parents=True)
        except FileExistsError as e:
            print(f"{e} already exists and will not be replaced")
