from pathlib import Path


def compress_directories(item, parent_dir=Path()):
    """Returns a list of endpoint paths based on a nested dict/list/string/
    pathlib.Path with parent_dir as the root directory"""
    paths = []
    if any([isinstance(item, t) for t in (str, Path)]):
        paths.append(parent_dir / item)
    elif isinstance(item, list):
        for d in item:
            if any([isinstance(d, t) for t in (str, dict, Path)]):
                paths.extend(compress_directories(d, parent_dir))
            else:
                raise TypeError('Nested lists are not valid directory structures')
    elif isinstance(item, dict):
        for a, d in item.items():
            new_parent = parent_dir / a
            if any([isinstance(d, t) for t in (str, list, dict, Path)]):
                paths.extend(compress_directories(d, new_parent))
            else:
                raise TypeError('Only lists, dicts, strs, and Paths can be passed to compress_directories')
    else:
        raise TypeError('Only lists, dicts, strs, and Paths can be passed to compress_directories')
    return paths

def create_directories(item, parent_dir=Path()):
    """Creates subdirectories of parent_dir based on a nested dict/list/string"""
    for dir in compress_directories(item, parent_dir=parent_dir):
        try:
            Path.mkdir(dir, parents=True)
        except FileExistsError as e:
            print(f"{e} already exists and will not be replaced")

def descend_directory(d, parent_dir=Path()):
    """Generator that yields directories descended from a nested dictionary"""
    if isinstance(d, dict):
        for x, y in d.items():
            yield (parent_dir / x)
            yield from descend_directory(y, parent_dir=(parent_dir / x))
    elif isinstance(d, list):
        for x in d:
            yield from descend_directory(x, parent_dir=parent_dir)
    elif any(isinstance(d, t) for t in (str, Path)):
        yield (parent_dir / d)
    else:
        raise TypeError('Only lists, dicts, strs, and Paths can be passed to descend_directory')

def path_to_dict(path):
    """Generate a nested dict/list/str of folder/file names showing the 
    directory structre of path."""
    if any((x.is_file() for x in path.iterdir())):
        dir_files = [x.name for x in path.iterdir() if x.is_file()]
        dir_files.extend(({x.name: path_to_dict(x)} for x in path.iterdir() if x.is_dir()))
        return dir_files
    else:
        return {x.name: path_to_dict(x) for x in path.iterdir()}
