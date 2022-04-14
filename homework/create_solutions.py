import sys
import os
import json


with open('assignments.json', 'r', encoding='utf-8') as file:
    assignment_dict = json.load(file)
with open(os.path.join('..', 'course_info.json'), 'r', encoding='utf-8') as file:
    course_info = json.load(file)

def create_solutions(hw_assignment_name):
    assert hw_assignment_name in assignment_dict
    problem_dict = assignment_dict[hw_assignment_name]
    solution_string = '\n    '.join([
        f"\\booksolution{{{chnum}}}{{{prnum}}}" 
        for chnum, prlist in problem_dict['book-problems'].items()
        for prnum in prlist
    ])
    solution_string += '\n    ' + (
        '\n    '.join([
            f"\\extrahwsolution{{{chnum}}}{{{prname}}}"
            for chnum, prlist in problem_dict['extra-hw-problems'].items()
            for prname in prlist
        ])
    )
    with open('solutions_template.tex', 'r', encoding='utf-8') as file:
        template = file.read()
    contents = (template.replace("[[TITLE]]", f"{hw_assignment_name} Solutions")
        .replace("[[SOLUTIONS]]", solution_string)
        .replace("[[COURSENUMBER]]", course_info["course_number"])
        .replace("[[COURSENAME]]", course_info["course_name"])
        .replace("[[SEMESTER]]", course_info["semester"])
        .replace("[[INSTRUCTOR]]", course_info["instructor"]))
    if not os.path.exists(hw_assignment_name):
        os.makedirs(hw_assignment_name)
    with open(
        os.path.join(hw_assignment_name, 'solutions.tex'), 
        'w', encoding='utf-8'
        ) as file:
        file.write(contents)

if len(sys.argv) == 2:
    hw_assignment_name = sys.argv[1]
    create_solutions(hw_assignment_name)
elif len(sys.argv) == 1:
    for hw_assignment_name in assignment_dict:
        create_solutions(hw_assignment_name)
else:
    print("Nothing happened. Please either submit no arguments, "
    "or the name of one of the homework assignments in assignment.json")