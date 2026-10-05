import argparse
from pathlib import Path
import markdown
from justhtml import JustHTML

parser = argparse.ArgumentParser(description="Build a resume from component parts.")
parser.add_argument("-o", "--output", 
                    help="output directory",
                    default=Path("../outputs"),
                    metavar="PATH",
                    type=Path
                    )

parser.add_argument("-f", "--format",
                    help="output format(s)",
                    # pdf is such a goddamn pain
                    default=['md', 'html'],
                    choices=['md', 'html'],
                    nargs='+'
                    )

parser.add_argument("-p", "--profile",
                    help="profile variant",
                    default="base",
                    choices=['base', 'ai', 'fintech', 'consulting']
                    # sections with filename ending in _<profile>,
                    # except for base, get used; experience_ai.md, for ex.
                    # should give feedback for which sections
                    # to ensure no surprise missed
                    )

# parser.add_argument("--sections",
#                     help="section overrides",
#                     default=None,
#                     metavar="FILE",
#                     nargs='+')

args = parser.parse_args()

sections = [
    'header',
    'summary',
    'skills',
    'certifications',
    'projects',
    'experience',
    'education'
]

# ---
# PROFILE
# ---
section_dir = Path('../sections')

# if args.profile != 'base':
postfix = f'_{args.profile}' if args.profile != 'base' else ''


# could probably interleave with file opening
# but then have to deal with format choices etc
# so nah
content = []

for section in sections:
    path = section_dir / f'{section}.md'
    if postfix:
        profile_path = section_dir / f'{section}{postfix}.md'
        if profile_path.exists():
            path = profile_path
        else:
            print(f'WARNING: no {args.profile} variant for {section}. Falling back to default.')

    if not path.exists():
        print(f'WARNING: missing section: {section}')
        continue

    # with open(path, 'r') as f:
    #     content.append(f.read())
    # Smoother.
    content.append(path.read_text(encoding='utf-8'))


# lol overkill, I know my own name and no one else is
# gonna use this.
name = content[0][2:content[0].index('\n')].replace(' ', '-')


# ---
# FORMAT
# ---
# This is intermediate to html, so it'll always happen
md = '\n\n'.join(content)

if 'html' in args.format:
    fragment = markdown.markdown(md)
    # html = JustHTML(fragment).to_html()
    # feels...sloppy
    description = ""
    p_title = ""
    title = ""
    stylesheet = "../assets/styles/resume.css"

    html = Path('../../templates/base.html').read_text(encoding='utf-8')
    html = (
        html
        .replace('/assets/css/main.css', stylesheet)
        .replace('{{PAGE DESCRIPTION}}', description)
        .replace('{{PAGE TITLE}}', p_title)
        .replace('{{MAIN PAGE TITLE}}', title)
        .replace('{{PAGE CONTENT}}', fragment)
    )



# ---
# OUTPUT 
# ---
# ensure directory exists
output = args.output / args.profile
output.mkdir(parents=True, exist_ok=True)

# within folder, place the file(s)
if 'md' in args.format:
    # with open(output) # nope, Path has its own thing
    (output / f'{name}.md').write_text(md, encoding='utf-8')

if 'html' in args.format:
    (output / f'{name}.html').write_text(html, encoding='utf-8')
