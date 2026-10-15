# fald.github.io

Source for my portfolio site at https://fald.github.io

A small, albeit overcomplicated, static site built with plain Python scripts and no framework.  
Page content is determined through JSON files that link templates and content.  
The resume itself is assembled from markdown files split into sections.  
GitHub Actions builds, assembles, and deploys to GitHub Pages.  
  

## Steps

- `build_resume.py` joins Markdown sections into one resume, allowing for multiple profiles. Markdown and HTML formats.
- `build_resume_pdf.py` then renders the HTML to a text-based PDF using Playwright.
- `build_site.py` fills in templates with content and metadata from relevant JSON files.  
  
Running the scripts in that order will (should) correctly build everything.  
  

## Layout

- `data/*.json`: Metadata, one file per page.  
- `data/projects/`: Metadata specific to chosen projects.
- `templates/`: Page and project shells, PDF wrapper, and page content.
- `resume/sections/`: Markdown sections, one file each.
- `resume/outputs/`: Generated HTML and Markdown files.
- `assets/`: CSS, images, and PDFs.
- `scripts/`: The three build scripts.
- `.github/workflows/build.yml`: Build/deploy to GitHub Pages.  
  

## Build Locally

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium

python scripts/build_resume.py
python scripts/build_resume_pdf.py
python scripts/build_site.py

python -m http.server 8000
```

Then open http://localhost:8000
This step is necessary since pages use root-relative paths.  
Then again, why would you want to build this locally?
