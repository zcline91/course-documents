import sys
import json
import re

from pathlib import Path
from util import compress_directories, create_directories


class AssignmentNameError(Exception):
    pass


__location__ = Path.cwd().joinpath(Path(__file__).parent).resolve()
__root__ = __location__.parent # Set parent directory as root
config = json.loads((__location__ / 'config.json').read_text(encoding='utf-8'))
hw_assignments = json.loads((__location__ / 'hw_assignments.json').read_text(encoding='utf-8'))

hw_as_config = config['document_types']['homework-assignment']

assignment_name = sys.argv[1]
filename = re.sub("[^0-9a-zA-z]+", "-", assignment_name).lower()
pathstr = hw_as_config['default_path'].replace('@title@', filename)
docdepth = len(pathstr.split('/'))

try:
    problem_dict = hw_assignments[assignment_name]
except KeyError:
    raise AssignmentNameError(f"{assignment_name} is not a known assignment name")

prob_str = ""
for source, probs in problem_dict.items():
    s_config = config['problem_sources'][source]
    depth = s_config['directory_levels']
    comp_dirs = compress_directories(probs)
    create_directories(comp_dirs, parent_dir=(__root__ / "problems" / source))
    top_dirs = []
    top_dirs_duplicated = [Path().joinpath(*d.parts[0:depth]) for d in comp_dirs]
    [top_dirs.append(d) for d in top_dirs_duplicated if d not in top_dirs] # Use this method rather than sets to maintain order
    file_dirs = list(set(comp_dirs).union(set(top_dirs)))
    for dir in file_dirs:
        for filename in s_config['standard_tex_files']:
            path = (__root__ / "problems" / source / dir / f"{filename}.tex")
            if not path.exists():
                path.write_text("(FILL)")
    for dir in sorted(top_dirs):
        parts_str = ','.join(
            (d.parts[depth] for d in comp_dirs if (d.parts[0:depth] == dir.parts and len(d.parts) > depth))
        )
        if parts_str != '':
            parts_str = "[" + parts_str + "]"
        prob_str += (
            f"  \{source}problem" + parts_str + ''.join(f"{{{d}}}" for d in dir.parts) + '\n'
        )


contents = (__root__ / 'templates' / 'homework-assignment.tex').read_text(encoding='utf-8')
contents = (contents.replace("TITLE", assignment_name)
    .replace("INCLUDES", '\n'.join(["\input{" + "../" * docdepth + f"includes/{x}.tex}}" for x in hw_as_config['includes']]))
    .replace("PROBLEMS", prob_str))
path = (__root__ / "documents" / pathstr)
path.parent.mkdir(parents=True)
path.write_text(contents, encoding='utf-8')
