import json
import os


#Change this tuple based on which files you would like 
#to be created by default for each book problem.
STANDARD_FILES=("statement.tex", "solution.tex")


with open('all_problems.json', 'r', encoding='utf-8') as file:
    problem_dict = json.load(file)

for chapter, problems in problem_dict.items():
    for problem in problems:
        path = os.path.join(chapter, str(problem))
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            print(f"{path} already exists and will not be overwritten")
        for f in (STANDARD_FILES):
            filepath = os.path.join(path, f)
            if not os.path.exists(filepath):
                with open(filepath, 'w') as file:
                    pass
            else:
                print(f"{filepath} already exists and will not be overwritten")
