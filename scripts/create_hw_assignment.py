import os
import sys
import json

assignment_name = sys.argv[1]
if len(sys.argv) > 2:
    assignment_path = sys.argv[2]

with open('setup.json', 'r', encoding='utf-8') as file:
    setup = json.load(file)
with open('hw_assignments.json', 'r', encoding='utf-8') as file:
    hw_assignments = json.load(file)

try:
    problem_dict = hw_assignments[assignment_name]
except KeyError:
    print(f"{assignment_name} is not a valid assignment name. Aborting")

problem_string = ""
for source in problem_dict:
    




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