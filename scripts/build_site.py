from pathlib import Path
import json

pages = Path('../data').glob("*.json")
templates = Path('../templates')

for page in pages:
    data = json.loads(page.read_text(encoding='utf-8'))

    location = Path(f"../{data['location']}")
    template = (
        Path(f"../templates/{data['template']}")
        .read_text(encoding='utf-8')
    )
    del data['location']
    del data['template']

    for key in data:
        # if isinstance(data[key], list):
        #     data[key] = "\n".join(data[key])
        if key in ['main_content', 'aside'] and data[key]:
            replacement = (
                Path(f"../templates/{data[key]}")
                .read_text(encoding='utf-8')
            )
        else:
            replacement = data[key]
        template = (
            template
            .replace('{{' + key + '}}', replacement)
        )

    location.write_text(template, encoding='utf-8')

    break

