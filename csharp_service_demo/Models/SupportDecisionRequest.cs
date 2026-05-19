namespace AgentGridSupport.Models;

public class SupportDecisionRequest
{
    public required string TraceId { get; set; }
    public required string IssueType { get; set; }
    public required string FinalDecision { get; set; }
    public required string Reason { get; set; }
    public required string SupportAction { get; set; }
}
