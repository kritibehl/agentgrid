using AgentGridSupport.Models;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

var decisions = new List<SupportDecision>();

app.MapGet("/health", () =>
{
    return Results.Ok(new
    {
        status = "healthy",
        service = "agentgrid-csharp-proof-layer"
    });
});

app.MapPost("/support/decision", (SupportDecisionRequest request) =>
{
    var decision = new SupportDecision
    {
        DecisionId = $"decision_{Guid.NewGuid():N}"[..21],
        TraceId = request.TraceId,
        IssueType = request.IssueType,
        FinalDecision = request.FinalDecision,
        Reason = request.Reason,
        SupportAction = request.SupportAction,
        CreatedAtUtc = DateTime.UtcNow
    };

    decisions.Add(decision);

    return Results.Ok(decision);
});

app.MapGet("/support/decisions", () =>
{
    return Results.Ok(decisions);
});

app.MapGet("/support/decisions/{decisionId}", (string decisionId) =>
{
    var decision = decisions.FirstOrDefault(item => item.DecisionId == decisionId);

    return decision is null
        ? Results.NotFound(new { error = "decision_not_found", decisionId })
        : Results.Ok(decision);
});

app.Run();
