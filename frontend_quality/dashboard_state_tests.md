# Dashboard State Tests

## State Coverage

| State | Expected dashboard behavior |
|---|---|
| loading | show spinner and loading message |
| success | render metrics, trace viewer, eval gate, and incident timeline |
| error | render error panel with retry button |
| retry | increment retry count and re-run API loaders |
| empty | use deterministic fallback data |
| hold | show HOLD badge and blocked release state |
| escalate | show escalation routing |
| ship | show safe release state |

## Manual Test Flow

1. Load dashboard without API URL.
2. Confirm fallback data renders.
3. Toggle light/dark mode.
4. Click each nav tab.
5. Validate trace, incident, release, and overview views.
6. Simulate invalid API URL.
7. Confirm retry state appears.
