# Unsupported Output Review

## What to Flag

- fabricated production deployments
- fake customer metrics
- unsupported root-cause claims
- invented integrations
- unverified model benchmark claims
- claims of real traffic without evidence

## AgentGrid Handling

Unsupported outputs should be:
- blocked by eval gate
- routed to human review
- logged with trace ID
- converted into product feedback if recurring
