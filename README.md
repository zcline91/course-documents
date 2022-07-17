# Course Documents

This is a directory structure and document generator for the various documents one needs to create while teaching a course (e.g. course notes, worksheets, homework, solutions, quizzes, ...).
This is originally designed for a Mathematics course, but I'm sure has applications in other disciplines.

**This is a work-in-progress at the moment, and is not ready to deploy.**

## Notes-to-self

- At present, pdf files will be ignored by git, since the pdfs generated by TeX are reproducible.
This can present a problem if trying to include pdf graphics in a TeX file though.
For that reason, any pdf files in folders named `img` (or subdirectories thereof) will not be ignored

## To-Do

- [x] Implement the creation of homework solution files
- [ ] Implement the creation of worksheets and notes for class
    - [x] Create a class for worksheets
    - [x] Create a class for notes
- [x] Implement the creation of quizzes
    - [x] Create a class for quizzes
- [ ] Implement the creation of tests
    - [ ] Currently 'problem-and-solution' includes only don't allow for the assignment of points. Fix this for tests.
- [ ] Brainstorm how to store assessment problems in a way which makes them reusable.
- [x] Add coursewide .sty file (and potentially others for homework, worksheets, etc.) (Used the idea of 'includes' instead to accomplish the same goal.)
- [ ] Continue to alter the format of `course_info.json` to store all the necessary info for the course.
- [ ] (Make more functions in `config.py` and then make it a command-line program which will set up the whole course if run with no arguments, and will use arguments from the command-line to perform particular tasks after the course has been initialized.) Note: I've abandoned `config.py` for `setup.py`, but have kept it arround for now in case some of the options are useful.
- [ ] Currently, scripts like `create_quiz.py` and `create_test.py` are mostly the same with a few exceptions. Create one such script, that can be used for both. Doing so might require the creation of more includes, and possibly more options to be added to `config.json`. 
- [ ] Make subfolders in includes for different depths, so that instead of multiple `problem-and-solution-x` includes with different valuse of x, there are folders `2`, `3`, `4`, etc. each with a file `problem-and-solution.tex`.

## Set-Up

- Copy the directory somewhere, probably with the name of the course.
- Edit `config.json` for the course:
  - Set the course information at the top of the json file.
  - Edit/add problem sources. Problem sources could include textbooks, colleagues, etc. Use only alphabetical characters for names (maybe use roman numerals  for edition numbers of textbooks).  
    - `standard_tex_files` is an array of files to be created when a problem is created. E.g. solution, statement, comment. 
    - `directory_levels` indicates for this problem source how deep the    directory structure will go for problems. E.g. if textbook problems will be organized by chapter/section/problem_number, then set directory_levels to 3.
  - Edit/add document types for the course 
    - `default_directory` is the place a new document of that type will be placed, unless otherwise specified.
    - `includes` are the files from the directory of includes that will be imported at the top of tex files of the given document type.
    - Note: For includes for clicker-questions, the include `clicker-questions` must be included before `course-info`.