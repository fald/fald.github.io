from pathlib import Path
import json

pages = Path('../data')
templates = Path('../templates')
loaded_templates = {

}

def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def load_page_data(pages):
    return pages.iterdir()


pages = load_page_data(pages)
for page in pages:
    data = load_json(page)

    location = Path(f"../{data['location']}")
    template = (
        Path(f"../templates/{data['template']}")
        .read_text(encoding='utf-8')
    )
    del data['location']
    del data['template']

    for key in data:
        if type(data[key]) is list:
            data[key] = "\n".join(data[key])
        template = (
            template
            .replace('{{' + key + '}}', data[key])
        )

    location.write_text(template)

