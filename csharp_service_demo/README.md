# AgentGrid C# / ASP.NET Core Minimal API Proof Layer

## Purpose

This folder provides a small C# / ASP.NET Core Minimal API proof layer for AgentGrid support decisions.

It is intended for Microsoft, Cognizant, Azure, .NET, and Microsoft 365-oriented applications where showing C# / ASP.NET Core familiarity is useful.

## Endpoints

| Endpoint | Purpose |
|---|---|
| GET /health | Health check |
| POST /support/decision | Create support decision |
| GET /support/decisions | List support decisions |
| GET /support/decisions/{decisionId} | Get one decision |

## Example Request

```json
{
  "traceId": "trace_123",
  "issueType": "tool_failure",
  "finalDecision": "escalate",
  "reason": "tool_call_failure",
  "supportAction": "Route to engineering owner"
}
Scope

This is a proof-layer implementation. It demonstrates ASP.NET Core Minimal API familiarity and API modeling for AgentGrid support decisions. It does not claim production .NET experience.
