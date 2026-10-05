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

print(args)

sections = [
    'header',
    'summary',
    'skills',
    'certifications',
    'projects',
    'experience',
    'education'
]

# CHOOSING SECTIONS
# TODO: --sections overrides
section_dir = Path('../sections/')

if args.profile != 'base':
    postfix = f'_{args.profile}.md'
else:
    postfix = '.md'
