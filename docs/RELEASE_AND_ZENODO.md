# Release and Zenodo DOI checklist

## Repository release

1. Confirm tests pass: `pytest`.
2. Confirm the demo and exports build: `python scripts/generate_demo.py` then `python scripts/build_exports.py`.
3. Update version values in `pyproject.toml`, `src/enerjinabiz/__init__.py`, `CITATION.cff` and `.zenodo.json` if needed.
4. Commit and push the repository.
5. Create GitHub Release `v1.0.0` with title `Türkiye Energy Intelligence Platform v1.0.0`.

## Zenodo

1. Sign in to Zenodo and link GitHub.
2. Open the Zenodo GitHub integration page and sync repositories.
3. Enable `turkiye-energy-intelligence-platform`.
4. Create the GitHub release. Zenodo will archive the release and mint a DOI.
5. Add the DOI to `CITATION.cff`, README and the website, then create a patch release if desired.

The repository contains both `CITATION.cff` and `.zenodo.json`. Zenodo gives precedence to `.zenodo.json` for GitHub archiving metadata, while GitHub uses `CITATION.cff` to display citation guidance.


## Automated metadata update

After Zenodo issues the DOI, run:

```bash
python scripts/apply_zenodo_doi.py 10.5281/zenodo.YOUR_ID
```

Before publishing a release, run:

```bash
python scripts/release_audit.py
```
