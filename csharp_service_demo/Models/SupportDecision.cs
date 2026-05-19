namespace AgentGridSupport.Models;

public class SupportDecision
{
    public required string DecisionId { get; set; }
    public required string TraceId { get; set; }
    public required string IssueType { get; set; }
    public required string FinalDecision { get; set; }
    public required string Reason { get; set; }
    public required string SupportAction { get; set; }
    public DateTime CreatedAtUtc { get; set; }
}
