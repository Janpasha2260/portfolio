# Janpasha Mohammad — AI/ML Professional Portfolio

This is a static GitHub Pages portfolio containing six workshop artifacts, a separate final project, and a landing page for each artifact.

Every artifact landing page concludes with a separate three-paragraph reflection explaining learning, professional growth, limitations, and future application.

Workshops Four and Five use the real Wisconsin Diagnostic Breast Cancer dataset from the UCI Machine Learning Repository through scikit-learn. The final project uses the real scikit-learn diabetes dataset. These artifact folders include executable Python, source-data evidence, CSV metrics, recorded output, predictions, and generated charts.

## Publish with GitHub Pages

1. Create a new public GitHub repository, for example `ai-ml-portfolio`.
2. Upload every file and folder from this package to the repository root.
3. Open **Settings → Pages** in the repository.
4. Under **Build and deployment**, choose **GitHub Actions**.
5. The included workflow publishes the site automatically after a push to `main`.

The public address will normally be:

`https://YOUR-USERNAME.github.io/ai-ml-portfolio/`

## Open locally — easiest method

1. Extract the ZIP completely. Do not open `index.html` from inside the ZIP preview.
2. Open the extracted folder.
3. Double-click `index.html`.

The portfolio and all seven artifact pages work directly from local files. No installation or server is required.

## Optional local server

Run this command from the project folder:

```bash
python -m http.server 8000
```

Then open `http://localhost:8000`.

## Structure

- `index.html` — portfolio home page
- `styles.css` — responsive design
- `script.js` — artifact data and rendering
- `artifacts/<artifact-name>/index.html` — seven separate artifact landing pages
- `artifacts/files/` — reports, code, and results
- `assets/` — portfolio visuals
- `.github/workflows/pages.yml` — GitHub Pages deployment workflow

The Workshop Four, Workshop Five, and final-project analyses use real public data but remain educational demonstrations. They are not clinical tools and should not be used for real medical decisions.
