from pathlib import Path
from playwright.sync_api import sync_playwright

# TODO: type hints etc for all code
# TODO: Update all errors/warnings, too
# TODO: Decide between this style and main page style

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / 'resume/outputs'
PDF_DIR = ROOT / 'assets/files'

name = "Firas-Aldabbas"
profiles = ('base', 'adgm')
# gotta be done this way, zz I hate web dev
# set_content loads into blank page, no url, no relative css path, so it needs to be inline
# also putting the tags in here so IDE stops yelling at me about the internal style formatting
css = f"<style>{(ROOT / 'assets/css/resume.css').read_text(encoding='utf-8')}</style>"
base = (ROOT / 'templates/resume.html').read_text(encoding='utf-8').replace('{{css}}', css)


def build_page(page, profile: str) -> Path:
    # Locate generated HTML
    # Open in Chromium (Playwright by Chromium)
    # Wait for page/stylesheet to load
    # Render page as pdf
    #   ATS-friendly, text-based (primary purpose of chromium)
    # Save in correct location to be downloaded
    
    source = OUTPUT_DIR / f'{profile}/{name}.html'
    if not source.exists():
        raise SystemExit(f"Missing {source}. Try running /scripts/build_resume.py first.")

    html = base.replace("{{main_content}}", source.read_text(encoding='utf-8'))

    # magic playwright stuff
    # TODO: Look into this enough to actually understand it and not copy-paste
    #       it does seem simple enough, but I doubt I could recreate it on the fly lol
    page.set_content(html, wait_until='load')
    page.emulate_media(media='print')

    suffix = '' if profile == 'base' else f'-{profile}'
    target = PDF_DIR / f'{name}{suffix}.pdf'
    page.pdf(
        path=str(target),
        format='Letter',
        print_background=True,
        margin={
            'top': '0.6in',
            'bottom': '0.6in',
            'left': '0.7in',
            'right': '0.7in'
        }
    )

    return target


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        for profile in profiles:
            print(f'wrote: {build_page(page, profile)}')
        browser.close()


if __name__ == "__main__":
    main()
