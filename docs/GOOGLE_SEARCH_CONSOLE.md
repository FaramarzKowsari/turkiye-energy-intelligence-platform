# Google Search Console checklist

Expected URL:

`https://faramarzkowsari.github.io/turkiye-energy-intelligence-platform/`

1. Enable GitHub Pages using the included Pages workflow.
2. Open Google Search Console and add the exact URL-prefix property above.
3. Select HTML file upload or HTML meta-tag verification.
4. For file upload, place Google's exact verification file inside `docs/` and commit it unchanged.
5. For meta-tag verification, paste Google's exact tag into the `<head>` of `docs/index.html`.
6. Verify ownership.
7. Submit `sitemap.xml`.
8. Inspect the homepage URL, run Test Live URL, then Request Indexing.

The repository already includes `robots.txt`, `sitemap.xml`, canonical tags, alternate-language tags and structured data. Only Google's unique verification token must be supplied by the owner.


## Safe file installer

Keep Google's verification file unchanged and copy it into `docs/` with:

```bash
python scripts/install_search_console_verification.py /path/to/google-verification-file.html
```
