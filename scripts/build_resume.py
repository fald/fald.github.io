import argparse
from pathlib import Path
import markdown

# TODO: UAE photo, nationality, relocation, adgm profuke
# TODO: Resumes are built, should be in .gitignore? 
# TODO: (cohesion) Linkedin, Github profile updates
# TODO: (future) - links to find elsewhere; vibe coding git page, 'other stuff' (tech, non-tech), itch.io

ROOT = Path(__file__).resolve().parent.parent
RESUME_DIR = ROOT / 'resume'
SECTION_DIR = RESUME_DIR / 'sections'
OUTPUT_DIR = RESUME_DIR / 'outputs'
TEMPLATE_DIR = ROOT / 'templates'

NAME = "Firas-Aldabbas"
PROFILES = ('base', 'adgm')

# Kinda gotta do it this way to simplify 
# not including variants because of how I
# structured it; ie, non-optimally.
sections = (
    'header',
    'summary',
    'skills',
    'certifications',
    'projects',
    'experience',
    'education'
)

# This was all a massive waste.
# I will always build the md as a way towards the html
# The html will always be built on the way to the pdf
# The only maybe is for variants, I guess.

# parser = argparse.ArgumentParser(description="Build a resume from component parts.")
# parser.add_argument("-o", "--output", 
                    # help="output directory",
                    # default=OUTPUT_DIR,
                    # metavar="PATH",
                    # type=Path
                    # )

# parser.add_argument("-f", "--format",
#                     help="output format(s)",
#                     # pdf is such a goddamn pain
#                     default=['md', 'html'],
#                     choices=['md', 'html'],
#                     nargs='+'
#                     )

# parser.add_argument("-p", "--profile",
#                     help="profile variant",
#                     default="base",
                    # choices=['base', 'adgm', 'ai', 'fintech', 'consulting']
                    # sections with filename ending in _<profile>,
                    # except for base, get used; experience_ai.md, for ex.
                    # should give feedback for which sections
                    # to ensure no surprise missed
                    # )

# parser.add_argument("--sections",
#                     help="section overrides",
#                     default=None,
#                     metavar="FILE",
#                     nargs='+')

# args = parser.parse_args()


# PROFILE
for profile in PROFILES:
    postfix = f'_{profile}' if profile != 'base' else ''

    content = []

    for section in sections:
        path = SECTION_DIR / f'{section}.md'
        if postfix:
            profile_path = SECTION_DIR / f'{section}{postfix}.md'
            if profile_path.exists():
                path = profile_path
            else:
                print(f'WARNING: no {profile} variant for {section}. Falling back to default.')

        if not path.exists():
            print(f'WARNING: missing section: {section}')
            continue

        content.append(path.read_text(encoding='utf-8'))

    # FORMAT
    md = '\n\n'.join(content)
    html = markdown.markdown(md)

    # OUTPUT 
    # ensure directory exists
    output = OUTPUT_DIR / profile
    output.mkdir(parents=True, exist_ok=True)

    # within folder, place the file(s)
    (output / f'{NAME}.md').write_text(md, encoding='utf-8')
    (output / f'{NAME}.html').write_text(html, encoding='utf-8')
