import json
import os
import copy
import re


def depth(x):
    # Returns the depth of a nested dict
    if isinstance(x, dict) and x != {}:
        return 1 + max(depth(x[a]) for a in x)
    elif isinstance(x, list) and x != []:
        return 1 + max(depth(a) for a in x)
    else:
        return 0

def combine_nested_dicts(d1, d2):
    """For two nested dicts with common depths, this will create
    a new combined nested dict with the same depths."""
    assert depth(d1) == depth(d2)
    d3 = copy.deepcopy(d1)
    for k, v in d2.items():
        if isinstance(v, list):
            d3.setdefault(k, []).extend(d2[k])
        elif isinstance(v, dict):
            if k in d3:
                d3[k]= combine_nested_dicts(d3[k], d2[k])
            else:
                d3[k] = v
    return d3

def compress_directories(nested_dict):
    # Returns a list of endpoint paths based on a nested_dict
    paths = []
    for dirname, subdirs in nested_dict.items():
        if isinstance(subdirs, list):
            paths.extend([os.path.join(dirname, str(subdir)) for subdir in subdirs])
        elif isinstance(subdirs, dict):
            paths.extend([os.path.join(dirname, subdir) for subdir in compress_directories(subdirs)])
    return paths

def create_directories(nested_dict, root="."):
    # Creates subdirectories of root based on nested_dict
    for d in compress_directories(nested_dict):
        dir = os.path.join(root, d)
        if not os.path.exists(dir):
            os.makedirs(dir)
        else:
            print(f"{dir} already exists and will not be replaced")



with open('course_info.json', 'r', encoding='utf-8') as file:
    course_info = json.load(file)


def create_homework_files():
    for source, details in course_info["homework"]["sources"].items():
        problem_list = [assignment[source] for assignment in course_info["homework"]["assignments"].values() if source in assignment]
        problems = problem_list[0]
        for d in problem_list[1:]:
            problems = combine_nested_dicts(problems, d)
        for path in compress_directories(problems):
            path = os.path.join(source, path)
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                print(f"{path} already exists and will not be overwritten")
            for f in details["standard-tex-files"]:
                filepath = os.path.join(path, f"{f}.tex")
                if not os.path.exists(filepath):
                    with open(filepath, 'w') as file:
                        pass
                else:
                    print(f"{filepath} already exists and will not be overwritten")

def create_assignment(hw_assignment_name):
    try:
        problem_dict = course_info["homework"]["assignments"][hw_assignment_name]
    except KeyError:
        print(f"{hw_assignment_name} is not a valid assignment name.")
    command_string, problem_string = "", ""
    for source, problems in problem_dict.items():
        # Add a command to the tex preamble for this problem type
        command = course_info["homework"]["sources"][source]["latex-commands"]["assignment"]
        macro = command["macro"]
        dirnames = re.findall("N[0-9]", macro)
        num_args = len(dirnames) + 1 #PATH will also be an arg
        for index, string in enumerate(dirnames):
            macro = macro.replace(string, f"#{index + 1}")
        macro = macro.replace("PATH", f"#{num_args}")
        command_string += (f"\\newcommand{{\\{command['name']}}}[{num_args}]"
                f"{{\\item {macro}}}\n")
        # Add problems to the list
        for problem_path in compress_directories(problems):
            path_components = problem_path.split(os.sep)
            arguments = [path_components[int(name[1:])-1] for name in dirnames]
            arguments.append(f"../../{source}/" + "/".join(path_components))
            problem_string += ('\n    ' + f"\\{command['name']}"
                    + ''.join(f"{{{arg}}}" for arg in arguments))
    template_path = os.path.join("homework", "assignment_template.tex")
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()
    contents = (template.replace("[[TITLE]]", hw_assignment_name)
        .replace("[[COMMANDS]]", command_string)
        .replace("[[PROBLEMS]]", problem_string)
        .replace("[[COURSENUMBER]]", course_info["course_number"])
        .replace("[[COURSENAME]]", course_info["course_name"])
        .replace("[[SEMESTER]]", course_info["semester"])
        .replace("[[INSTRUCTOR]]", course_info["instructor"]))
    assignment_path = os.path.join("homework", hw_assignment_name)
    if not os.path.exists(assignment_path):
        os.makedirs(assignment_path)
    with open(
        os.path.join(assignment_path, 'assignment.tex'),
        'w', encoding="utf-8"
    ) as file:
        file.write(contents)

def create_solutions(hw_assignment_name):
    try:
        problem_dict = course_info["homework"]["assignments"][hw_assignment_name]
    except KeyError:
        print(f"{hw_assignment_name} is not a valid assignment name.")
    command_string, solution_string = "", ""
    for source, problems in problem_dict.items():
        # Add a command to the tex preamble for this problem type
        command = course_info["homework"]["sources"][source]["latex-commands"]["solution"]
        macro = command["macro"]
        dirnames = re.findall("N[0-9]", macro)
        num_args = len(dirnames) + 1 #PATH will also be an arg
        for index, string in enumerate(dirnames):
            macro = macro.replace(string, f"#{index + 1}")
        macro = macro.replace("PATH", f"#{num_args}")
        command_string += (f"\\newcommand{{\\{command['name']}}}[{num_args}]"
                f"{{\\item {macro}}}\n")
        # Add solutions to the list
        for problem_path in compress_directories(problems):
            path_components = problem_path.split(os.sep)
            arguments = [path_components[int(name[1:])-1] for name in dirnames]
            arguments.append(f"../../{source}/" + "/".join(path_components))
            solution_string += ('\n    ' + f"\\{command['name']}"
                    + ''.join(f"{{{arg}}}" for arg in arguments))
    template_path = os.path.join("homework", "solutions_template.tex")
    with open(template_path, "r", encoding="utf-8") as file:
        template = file.read()
    contents = (template.replace("[[TITLE]]", f"{hw_assignment_name} Solutions")
        .replace("[[COMMANDS]]", command_string)
        .replace("[[SOLUTIONS]]", solution_string)
        .replace("[[COURSENUMBER]]", course_info["course_number"])
        .replace("[[COURSENAME]]", course_info["course_name"])
        .replace("[[SEMESTER]]", course_info["semester"])
        .replace("[[INSTRUCTOR]]", course_info["instructor"]))
    assignment_path = os.path.join("homework", hw_assignment_name)
    if not os.path.exists(assignment_path):
        os.makedirs(assignment_path)
    with open(
        os.path.join(assignment_path, 'solution.tex'),
        'w', encoding="utf-8"
    ) as file:
        file.write(contents)

create_solutions("Assignment 1")