# Code Review Guardrails

## Review Checklist

- Does this change introduce unsupported claims?
- Are generated outputs grounded in repo artifacts?
- Are schema files valid JSON?
- Are tests updated?
- Does README wording avoid production overclaiming?
- Are fallback/error states handled?
- Are unsafe outputs blocked or routed to review?

## Merge Rule

Do not merge AI-assisted changes unless tests pass and claims remain defensible.
