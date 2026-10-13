from pathlib import Path
import json

# TODO: Shared templates loaded, instead of having them reloaded each time.
#       Especially for things that won't have odd templates (ie all project cards)
# TODO: Instead of print(warning), do it properly, lol
# TODO: Project card CSS (After build_resume is done)
# TODO: Everything (but resume) uses main.css, remove it from the filling, just place in template

# Going for that absolute.
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"

page_data = DATA_DIR.glob("*.json")


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
    
    template = (
        (TEMPLATE_DIR / project_data['card_template'])
        .read_text(encoding='utf-8')
    )

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

    base_template = (
        (TEMPLATE_DIR / data['base_template'])
        .read_text(encoding='utf-8')
    )
    
    # file meta info
    css = data['css']
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
    base_template = (
        base_template
        .replace("{{css}}", css)
        .replace("{{meta_title}}", meta_title)
        .replace("{{meta_description}}", meta_description)
        # .replace("{{page_title}}", page_title)
        .replace("{{main_content}}", main_content)
        .replace("{{aside_content}}", aside_content)
    )

    # lame, but works
    if not aside_content:
        base_template = base_template.replace('class="content-with-aside"', "")

    # Projects
    if 'projects' in data:
        base_template = (
            base_template.
            replace('{{project_cards}}', insert_project_cards(data['projects']))
        )

    destination.write_text(base_template, encoding='utf-8')
