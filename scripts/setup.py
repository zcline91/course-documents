import json
from pathlib import Path


class CourseInitializedError(Exception):
    pass


__location__ = Path.cwd().joinpath(Path(__file__).parent).resolve()
__root__ = __location__.parent # Set parent directory as root
config = json.loads((__location__ / 'config.json').read_text(encoding='utf-8'))

# Check if course has been initialized by checking if course-info.tex exists
path = __root__ / 'includes' / 'course-info.tex'
if path.exists():
    raise CourseInitializedError(
        "The course has already been initialized.")

# Set the course information
contents = f"""% For use in preambles for custom document types
\coursename{{{config['course_name']}}}
\coursenumber{{{config['course_number']}}}
\instructor{{{config['instructor']}}}
\semester{{{config['semester']}}}
"""
path.write_text(contents, encoding='utf-8')

# Add latex commands for each problem_source
#  - problem-and-solution
pas_head = (__location__ / 'init' / 'includes' / 'problem-and-solution.tex').read_text(encoding='utf-8')
pas_commands = (__location__ / 'init' / 'includes' / 'problem-and-solution-commands').read_text(encoding='utf-8')
for docdepth in range(2, 7):
    contents = pas_head
    for source, info in config['problem_sources'].items():
        probdepth = info['directory_levels'] + 1
        endstring = "/#".join(['', *map(str, range(2, probdepth+1))])
        end2string = "/#".join(['', *map(str, range(2, probdepth+2))])
        contents += (pas_commands.replace("SOURCE", source)
            .replace("PROBDEPTH", str(probdepth))
            .replace("DOCDEPTHSTRING", "../" * docdepth)
            .replace("ENDSTRING", endstring).replace("END2STRING", end2string))
    (__root__ / 'includes' / f'problem-and-solution-{docdepth}.tex').write_text(contents, encoding='utf-8')

# - homework-assignment
contents = (__location__ / 'init' / 'includes' / 'homework-assignment.tex').read_text(encoding='utf-8')
command = (__location__ / 'init' / 'includes' / 'homework-assignment-command').read_text(encoding='utf-8')
docdepth = len(config['document_types']['homework-assignment']['default_path'].split('/'))
for source, info in config['problem_sources'].items():
    probdepth = info['directory_levels'] + 1
    midstring = ".".join(map(lambda i: f"#{i}", range(2, probdepth+1)))
    endstring = "/#".join(['', *map(str, range(2, probdepth+1))])
    contents += (command.replace("SOURCE", source)
        .replace("PROBDEPTH", str(probdepth))
        .replace("MIDSTRING", midstring)
        .replace("DOCDEPTHSTRING", "../" * docdepth)
        .replace("ENDSTRING", endstring))
(__root__ / 'includes' / 'homework-assignment.tex').write_text(contents, encoding='utf-8')

# - homework-solutions
contents = (__location__ / 'init' / 'includes' / 'homework-solutions.tex').read_text(encoding='utf-8')
command = (__location__ / 'init' / 'includes' / 'homework-solutions-command').read_text(encoding='utf-8')
docdepth = len(config['document_types']['homework-solutions']['default_path'].split('/'))
for source, info in config['problem_sources'].items():
    probdepth = info['directory_levels'] + 1
    midstring = ".".join(map(lambda i: f"#{i}", range(2, probdepth+1)))
    endstring = "/#".join(['', *map(str, range(2, probdepth+1))])
    contents += (command.replace("SOURCE", source)
        .replace("PROBDEPTH", str(probdepth))
        .replace("MIDSTRING", midstring)
        .replace("DOCDEPTHSTRING", "../" * docdepth)
        .replace("ENDSTRING", endstring))
(__root__ / 'includes' / 'homework-solutions.tex').write_text(contents, encoding='utf-8')
