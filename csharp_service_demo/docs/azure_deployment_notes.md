# Azure Deployment Notes for C# Proof Layer

## Possible Deployment Target

- Azure App Service
- Azure Container Apps
- Azure SQL Database
- Azure Monitor / Application Insights
- Azure Key Vault for secrets

## Environment Variables

| Variable | Purpose |
|---|---|
| ASPNETCORE_ENVIRONMENT | Environment name |
| SQL_CONNECTION_STRING | SQL Server / Azure SQL connection |
| APPLICATIONINSIGHTS_CONNECTION_STRING | App Insights telemetry |

## Deployment Sketch

```text
React/Vite dashboard
→ FastAPI AgentGrid API
→ C# Minimal API support decision service
→ Azure SQL
→ Azure Monitor / App Insights
Scope

These notes show Azure deployment readiness and architecture familiarity. The current proof layer is local/in-memory and is not deployed to Azure.
