#!/usr/bin/env python3

import json
import argparse
from pathlib import Path

import yaml

from util import compress_directories, create_directories


__location__ = Path.cwd().joinpath(Path(__file__).parent).resolve()
__root__ = __location__.parent # Set parent directory as root
CONFIG = yaml.safe_load((__location__ / 'config.yaml')
                        .read_text(encoding='utf-8'))


class FiletypeError(Exception):
    pass


def _dirstr_to_dict(dirstr):
    """convert a directory string, e.g. '12/1/1' into a dict of the form
    {"12": {"1": "1"}}"""
    head_tail = dirstr.split('/', 1)
    assert len(head_tail) <= 2
    if len(head_tail) == 1 or head_tail[1] == '':
        return head_tail[0]
    else:
        return {head_tail[0]: _dirstr_to_dict(head_tail[1])}


def create_probs(source, item):
    """Creates problem files in the problems/<source> directory for 
    specified item, which could be a Path, a string, or a nested dict 
    of strings and lists, intepreted as the desired heirarchy directory
    structure for the problems in the source directory. Which files are 
    created for each problem is determined by the argument 
    'standard_tex_files' in the config.yaml file for the problem source,
    and which level of the directory structure to consider the problems
    at is determined by 'directory_levels' argument."""
    source_conf = CONFIG['problem_sources'][source]
    comp_dirs = compress_directories(item)
    create_directories(comp_dirs, 
        parent_dir=(__root__ / "problems" / source))
    file_dirs = set()
    for dir in comp_dirs:
        d = dir
        while len(d.parts) >= source_conf['directory_levels']:
            file_dirs.add(d)
            d = d.parent
    for dir in file_dirs:
        for filename in source_conf['standard_tex_files']:
            path = (__root__ / "problems" / source / dir / f"{filename}.tex")
            if not path.exists():
                path.write_text("(NOT WRITTEN)")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', choices=CONFIG['problem_sources'].keys(),
        help="the problem source to add problems for")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--problem', 
                       help="a single problem path in the source")
    group.add_argument('-s', '--string', 
                       help="json string of problems in directory structure")
    group.add_argument('-f', '--file', 
                       help=("yaml or json file of problems in directory "
                             "structure"))
    args = parser.parse_args()

    if args.problem is not None:
        create_probs(args.source, _dirstr_to_dict(args.problem))
    if args.string is not None:
        create_probs(args.source, json.loads(args.string))
    if args.file is not None:
        path = Path(args.file)
        text_contents = path.read_text(encoding='utf-8')
        if path.suffix == ".json":
            contents = json.loads(text_contents)
        elif path.suffix == '.yaml':
            contents = yaml.safe_load(text_contents)
        else:
            raise FiletypeError(f"{path} is not a .json or .yaml file")
        create_probs(args.source, contents)


if __name__ == '__main__':
    main()
