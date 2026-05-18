# C# / ASP.NET Core Minimal API Proof Layer

## Purpose

This document explains how AgentGrid support-decision outputs could be exposed through a C# / ASP.NET Core Minimal API layer for .NET/Azure-facing roles.

## Example Concept

```csharp
app.MapPost("/support/decision", (SupportDecision decision) =>
{
    return Results.Ok(new {
        decision.TraceId,
        decision.FinalDecision,
        decision.Reason,
        decision.SupportAction
    });
});
Example Model
public record SupportDecision(
    string TraceId,
    string FinalDecision,
    string Reason,
    string SupportAction
);
Scope

This is a proof-layer design note. It demonstrates C# / ASP.NET Core Minimal API familiarity, not production .NET experience.
