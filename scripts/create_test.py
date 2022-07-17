import json
import sys
import re

from pathlib import Path


__location__ = Path.cwd().joinpath(Path(__file__).parent).resolve()
__root__ = __location__.parent # Set parent directory as root
config = json.loads((__location__ / 'config.json').read_text(encoding='utf-8'))

test_conf = config['document_types']['test']

test_name = sys.argv[1]
filename = re.sub("[^0-9a-zA-z]+", "-", test_name).lower()
if len(sys.argv) > 2:
    pathstr = sys.argv[2]
else:
    pathstr = (test_conf['default_path'].replace('@title@', filename))
    print(f"The file will be created at {pathstr} in the documents folder. "
        "To change the path, specify a second argument (as a '/' separated string).")
docdepth = len(pathstr.split('/'))
inc_str = ''
for name in test_conf['includes']:
    if name == 'problem-and-solution':
        name += f"-{docdepth}"
    inc_str += ("\input{" + "../" * docdepth + f"includes/{name}.tex}}\n")
contents = ((__root__ / 'templates' / 'test.tex').read_text(encoding='utf-8')
    .replace("TITLE", test_name)
    .replace("INCLUDES", inc_str))
path = (__root__ / "documents" / pathstr)
path.parent.mkdir(parents=True)
path.write_text(contents, encoding="utf-8")