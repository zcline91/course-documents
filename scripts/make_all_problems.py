#!/usr/bin/env python3

import json
import argparse

from pathlib import Path

from util import path_to_dict, descend_directory, latex_escape


class ProblemLevelError(Exception):
    pass


__location__ = Path.cwd().joinpath(Path(__file__).parent).resolve()
__root__ = __location__.parent # Set parent directory as root
config = json.loads((__location__ / 'config.json').read_text(encoding='utf-8'))
problem_dir = (__root__ / 'problems')


if __name__ == '__main__':
    # Create arguments for command line
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', 
        help="directory (relative to 'documents') to write the problems file to")
    parser.add_argument('-f', '--filename', default="all-problems.tex",
        help="filename, the default is 'all-problems.tex'")
    args = parser.parse_args()

    directory = (__root__ / "documents" / args.directory)


    # Create the problem contents portion of the file
    prob_dicts = path_to_dict(problem_dir)
    prob_contents = ""
    for source, prob_dict in prob_dicts.items():
        prob_depth = config["problem_sources"][source]['directory_levels']
        prob_contents += f"\\section{{{latex_escape(source)}}}"
        depth = 0
        printing_files = False
        for prob in descend_directory(prob_dict):
            parts = len(prob.parts)
            if (problem_dir / source / prob).is_dir() and prob.stem != 'img':
                if printing_files:
                    prob_contents += "  " * depth + "\\end{description}\n"
                    printing_files = False
                if parts < prob_depth:
                    # Close all open environments for (sub)problems
                    while depth > 0:
                        if depth == 1:
                            prob_contents += "  " * depth + "\\end{description}\n"
                        else:
                            prob_contents += "  " * depth + "\\end{itemize}\n"
                        depth -= 1
                    # Make the relevant section
                    if parts == 1:
                        prob_contents += f"\\subsection{{{latex_escape(prob.as_posix())}}}\n"
                    elif parts == 2:
                        prob_contents += f"\\subsubsection{{{latex_escape(prob.as_posix())}}}\n"
                    elif parts == 3:
                        prob_contents += f"\\paragraph{{{latex_escape(prob.as_posix())}}}\n"
                    elif parts == 4:
                        prob_contents += f"\\subparagraph{{{latex_escape(prob.as_posix())}}}\n"
                    else:
                        raise ProblemLevelError("too many levels")
                elif parts == prob_depth:
                    if depth == 0:
                        prob_contents += "\\begin{description}\n"
                        depth = 1
                    while depth > 1:
                        depth -= 1
                        prob_contents += "  " * depth + "\\end{itemize}\n"
                    prob_contents += "  " * depth + f"\\item[{latex_escape(prob.as_posix())}]\n"
                else:
                    while parts < prob_depth + depth - 1:
                        depth -= 1
                        prob_contents += "  " * depth + "\\end{itemize}\n"
                    while parts > prob_depth + depth - 1:
                        prob_contents += "  " * depth + "\\begin{itemize}\n"
                        depth += 1
                    prob_contents += "  " * depth + f"\\item[{prob.stem}]\n"
            elif prob.suffix == '.tex':
                if not printing_files:
                    prob_contents += ("  " * depth + "\ \n" + "  " * depth + 
                                     "\\begin{description}\n")
                    printing_files = True
                prob_contents += ("  " * (depth + 1) + 
                    f"\\pitem[{latex_escape(prob.stem)}]" +
                    # f"{{{'/'.join([source] + list(prob.parent.parts))}}}" +
                    f"{{{(source / prob.parent).as_posix()}}}" +
                    f"{{{prob.stem}}}\n")
        if printing_files:
            prob_contents += "  " * depth + "\\end{description}\n"
        while depth > 0:
            if depth == 1:
                prob_contents += "\\end{description}\n"
            else:
                prob_contents += "\\end{itemize}\n"
            depth -= 1

    # Create the contents of the file
    docdepth = len(args.directory.split('/')) + 1
    contents = ((__root__ / 'templates' / 'all-problems.tex')
        .read_text(encoding='utf-8')
        .replace("ROOTDIR", "/".join([".."] * docdepth))
        .replace("CONTENTS", prob_contents))

    # Make any necessary directories and write the file
    directory.mkdir(parents=True, exist_ok=True)
    (directory / args.filename).write_text(contents, encoding='utf-8')
