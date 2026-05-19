# SQL Server-Style Schema Notes

## Table: SupportDecisions

```sql
CREATE TABLE SupportDecisions (
    DecisionId NVARCHAR(64) PRIMARY KEY,
    TraceId NVARCHAR(64) NOT NULL,
    IssueType NVARCHAR(128) NOT NULL,
    FinalDecision NVARCHAR(32) NOT NULL,
    Reason NVARCHAR(256) NOT NULL,
    SupportAction NVARCHAR(512) NOT NULL,
    CreatedAtUtc DATETIME2 NOT NULL
);
Indexes
CREATE INDEX IX_SupportDecisions_TraceId
ON SupportDecisions (TraceId);

CREATE INDEX IX_SupportDecisions_FinalDecision
ON SupportDecisions (FinalDecision);

CREATE INDEX IX_SupportDecisions_CreatedAtUtc
ON SupportDecisions (CreatedAtUtc);
Scope

This schema is documentation-only. The proof service stores decisions in memory.
