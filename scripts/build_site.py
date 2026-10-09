from pathlib import Path
import json

# Going for that absolute.
ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"

page_data = DATA_DIR.glob("*.json")

for page in page_data:
    data = json.loads(page.read_text(encoding='utf-8'))

    # I will assume the same correct structure for all
    # Deviations to be caught during automated tests but not
    # really handled apart from warnings/errors.
    destination = ROOT / data['destination']
    # ensure parent directory exists; probably not needed
    destination.parent.mkdir(parent=True, exist_ok=True)

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
    aside_content = (
        (TEMPLATE_DIR / data['aside_content_src'])
        .read_text(encoding='utf-8')
    )

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

    destination.write_text(base_template, encoding='utf-8')

    break

