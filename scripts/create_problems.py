#!/usr/bin/env python3

import json
import argparse

from pathlib import Path
from util import compress_directories, create_directories

def create_probs(source, item):
    source_conf = config['problem_sources'][source]
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

__location__ = Path.cwd().joinpath(Path(__file__).parent).resolve()
__root__ = __location__.parent # Set parent directory as root
config = json.loads((__location__ / 'config.json').read_text(encoding='utf-8'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('source', choices=config['problem_sources'].keys(),
        help="the problem source to add problems for")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-s', '--string', help="json string of problems in directory structure")
    group.add_argument('-f', '--file', help="json file of problems in directory structure")
    args = parser.parse_args()

    if args.string is not None:
        create_probs(args.source, json.loads(args.string))
    if args.file is not None:
        create_probs(args.source, 
            json.loads(Path(args.f).read_text(encoding='utf-8'))
        )
