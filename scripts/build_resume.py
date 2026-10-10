import argparse
from pathlib import Path
import markdown

# TODO: split the fragment from the display page
# TODO: and have some other way to select which version to display
# TODO: On such pages, fill in necessary parts of the template.
# TODO: Hide email from showing up and being scrapeable
# TODO: Github Actions to auto-process
# TODO: pdf version on github action
# TODO: Private site, split public-facing from actual repo
# TODO: Also, endless scroll? This todo shouldn't be here, but.
# TODO: Linkedin, Github profile updates
# TODO: Include Itch.io at some point
# TODO: refactor resume/scripts to /scripts
# TODO: git, linkedin, vibe-git links for aside
# TODO: PDF
# TODO: Github align
# TODO: Light/dark mode
# TODO: handle asides better; aside tag in the sub-template,
#   in-python handling of empty/null, deciding if I can just
#   put ext links in contact.
# TODO: Aria stuff across more pages - currently only partially in contact.html
# TODO: automated tests to include json validation

# until fix
exit()

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
                    # TODO: probably just remove choices
                    choices=['base', 'adgm', 'ai', 'fintech', 'consulting']
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
    description = ""
    p_title = ""
    title = ""
    stylesheet = "/assets/css/resume.css"
    button = """<aside><a class="download-button" href="resume.pdf" download>
    Download PDF
</a></aside><main>"""

    # TODO: Split the fragment from the page lol
    html = Path('../../templates/base.html').read_text(encoding='utf-8')
    # Infomercial voice: There's gotta be a better way! (There are several)
    html = (
        html
        .replace('/assets/css/main.css', stylesheet)
        .replace('{{PAGE DESCRIPTION}}', description)
        .replace('{{PAGE TITLE}}', p_title)
        .replace('{{MAIN TITLE}}', title)
        .replace('{{PAGE CONTENT}}', fragment)
        .replace('<main>', button)
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
