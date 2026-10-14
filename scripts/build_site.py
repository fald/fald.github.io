from pathlib import Path
import json

# TODO: Profile image
# TODO: skills: scikit-learn, ETL/data-pipelines, time-series forecasting
# TODO: Resume contact link - padding? separate lines so the image doesn't overlap with next line
#       pref via CSS to not do any more in-html fiddling.
# TODO: Clear up HTML comments/drafts
# TODO: This would've been simplified if I read he markdown docs:
#       Resume URLs aren’t links. The markdown library doesn’t autolink bare URLs. Write <https://github.com/fald> or [GitHub](https://github.com/fald) in header.md
# TODO: Structured data; JSON-LD block to base.html for Person (name, job title, sameAs, URL) - used by search engines?
# TODO: Project card displays technologies as list structure, style it up.
# TODO: Shared templates loaded, instead of having them reloaded each time.
#       Especially for things that won't have odd templates (ie all project cards)
# TODO: Instead of print(warning), do it properly, lol
# TODO: Project card CSS (After build_resume is done)
# TODO: CSS rem instead of pt, better scaling
# TODO: CSS: possibly change contact css; clear up the dead elements
# TODO: aria-labels on nav
# TODO: aria-current on active page
# TODO: Dark mode, possible print stylesheet, skip links (overkill w. small site)?
# TODO: populate README
# TODO: Social sharing (eugh. But...networking.) OpenGraph, Twitter??? tags, canonical links (?)
#       <link rel="canonical">, opengraph tags (og:title, description, and image)
# TODO: robots.txt, sitemap
# TODO: Use logging instead of print warning
# TODO: Wrap stuff in functions
# TODO: Major simplification
# TODO: Strip comments in the build with re.sub(r"<!--.*?-->", "", md, flags=re.S)
# TODO: Safe to kill resume.css?
# TODO: Tests; test folder, check json schema, required keys, 1 h1 tag, images have alts,
#       titles under 60 char, unique, descriptions under 160, no stray {{...}}...
# TODO: As part of simplification, just bite the bullet, undo all the work, and use Jinja2 lmfao.
# TODO: Add to ongoing project check


# Going for that absolute.
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"

page_data = DATA_DIR.glob("*.json")
base_template = (TEMPLATE_DIR / 'base.html').read_text(encoding='utf-8')


def insert_project_cards(project_list):
    final_info = ""

    for project in project_list:
        final_info += generate_project_card(project)
        final_info += "\n"

    return final_info


def generate_project_card(project_name):
    file_path = DATA_DIR / f'projects/{project_name}.json'
    if not file_path.exists():
        print(f'WARNING: No such project data ({project_name})')
        return ""

    project_data = json.loads(file_path.read_text(encoding='utf-8'))
    fill_fields = ['project_name', 'project_description', 'project_page_url', 'technologies']
    
    template = (TEMPLATE_DIR / 'project_card.html').read_text(encoding='utf-8')

    # project_data['technologies'] = str(project_data[])
    for field in fill_fields:
        template = template.replace('{{' + field + '}}', str(project_data[field]))

    return template


for page in page_data:
    data = json.loads(page.read_text(encoding='utf-8'))

    # I will assume the same correct structure for all
    # Deviations to be caught during automated tests but not
    # really handled apart from warnings/errors.
    destination = ROOT / data['destination']
    # ensure parent directory exists; probably not needed
    destination.parent.mkdir(parents=True, exist_ok=True)
    
    # file meta info
    meta_title = data['meta_title']
    meta_description = data['meta_description']

    # visible elements
    # This is always just going to be my name, so whatever.
    # page_title = data['page_title']
    main_content = (
        (TEMPLATE_DIR / data['main_content_src'])
        .read_text(encoding='utf-8')
    )
    if data['aside_content_src']:
        aside_content = (
            (TEMPLATE_DIR / data['aside_content_src'])
            .read_text(encoding='utf-8')
        )
    else:
        aside_content = ""

    # lol probably should've just stuck with a loop, oh well
    # it ain't even imposter syndrome at this point, I'm just
    # bad :P
    curr_page = (
        base_template
        .replace("{{meta_title}}", meta_title)
        .replace("{{meta_description}}", meta_description)
        .replace("{{main_content}}", main_content)
        .replace("{{aside_content}}", aside_content)
    )

    # lame, but works
    if not aside_content:
        curr_page = curr_page.replace('class="content-with-aside"', "")

    # Resume modifications for web display; lame, but works, again
    # TODO: Add download button when pdf is made
    if 'resume/index.html' in data['destination']:
        mbox_svg =  """<object class="mbox contact-item" width="180" height="24" data="/assets/images/mbox.svg" type="image/svg+xml"></object>"""
        linkedin =  """https://www.linkedin.com/in/firas-aldabbas/"""
        github =    """https://github.com/fald"""
        portfolio = """https://fald.github.io"""

        curr_page = (curr_page
                     # name's already on site header
                     .replace("<h1>Firas Aldabbas</h1>", "")
                     # don't want plaintext email
                     .replace("firas.aldabbas@gmail.com", mbox_svg)
                     # make the links clickable.
                     # TODO: shoulda just make a function for this
                     .replace(linkedin, f'<a href="{linkedin}">{linkedin}</a>') 
                     .replace(github, f'<a href="{github}">{github}</a>')
                     .replace(portfolio, f'<a href="{portfolio}">{portfolio}</a>')
                     )

    # Projects
    if 'projects' in data:
        curr_page = (
            curr_page.
            replace('{{project_cards}}', insert_project_cards(data['projects']))
        )

    destination.write_text(curr_page, encoding='utf-8')
