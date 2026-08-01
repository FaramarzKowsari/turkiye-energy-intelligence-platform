# Trust, Governance and Reproducibility

## Design principles

1. **No hidden dependency:** demo and local-file modes remain functional if an external provider is unavailable.
2. **Bring your own credentials:** EPİAŞ credentials remain on the user's machine or secret manager.
3. **Visible provenance:** every normalized row carries source and synthetic-data indicators.
4. **Immutable raw layer:** production users should preserve provider responses before transformation.
5. **Reproducible transformations:** cleaning, feature engineering and exports are code-driven.
6. **No false authority:** project pages distinguish demonstration output from official data.

## Data-quality controls

- Timestamp parsing and chronological sorting
- Duplicate-hour removal
- Negative-value invalidation for non-negative energy measures
- Missing-column creation for schema stability
- Hourly coverage calculation
- Missing-value counts by field
- Synthetic-row accounting
- Schema and metadata checks in CI

## Security controls

- `.env` and credential directories are ignored by Git
- Optional GitHub Actions refresh uses encrypted repository secrets
- Read-only analytical API
- No credentials in logs, outputs or demo data
- Dependency updates through Dependabot

## Auditability roadmap

Future versions should add raw-response hashes, OpenLineage-compatible events, Great Expectations suites, signed release attestations and provider-schema drift alerts.
