import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Build a resume from component parts.")
parser.add_argument("-o", "--output", 
                    help="output file or directory",
                    default=Path("../outputs/"),
                    metavar="PATH",
                    type=Path,
                    )

parser.add_argument("-f", "--format",
                    help="output format(s)",
                    default="both",
                    choices=['md', 'pdf', 'both'],
                    )

parser.add_argument("-p", "--profile",
                    help="profile variant",
                    default="base",
                    choices=['base', 'ai', 'fintech', 'consulting'],
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

# ---
# FORMAT
# ---

# ---
# OUTPUT 
# ---
