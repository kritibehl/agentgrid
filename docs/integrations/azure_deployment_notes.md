# Azure Deployment Notes

## Possible Azure Mapping

| AgentGrid component | Azure equivalent |
|---|---|
| FastAPI backend | Azure Container Apps / App Service |
| Redis worker queue | Azure Cache for Redis |
| SQLite/Postgres-like storage | Azure Database for PostgreSQL |
| Metrics | Azure Monitor / Application Insights |
| Secrets | Azure Key Vault |
| CI/CD | GitHub Actions to Azure |

## Deployment Sketch

```text
React dashboard
→ FastAPI AgentGrid API
→ Redis validation queue
→ AutoOps incident API
→ Azure Monitor / App Insights
Scope

These are deployment notes for Azure familiarity and architecture discussion. The live deployment currently uses Vercel and Google Cloud Run.
