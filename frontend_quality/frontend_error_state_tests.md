# Frontend Error State Tests

## Request states covered

| State | Implementation |
|---|---|
| loading | `LoadingPanel` |
| error | `ErrorPanel` |
| retry | `useAsyncResource.reload()` |
| fallback | API client deterministic demo fallback |
| success | dashboard renders typed data |

## Manual test checklist

1. Start dashboard without API URL.
2. Confirm fallback data renders.
3. Trigger invalid API URL.
4. Confirm retry panel appears.
5. Click retry.
6. Confirm retry count increments.
7. Toggle dark/light mode.
8. Resize browser to mobile width.
