# GitHub DevOps Runbook
## USASpending Enterprise AI Medallion Solution

## Purpose
Defines source control, branching, tagging, release, GitHub Actions, and wiki propagation practices.

## Standard Workflow
```powershell
cd C:\GitHub\usaspending_enterprise_ai_solution
git status
git add .
git commit -m "Describe meaningful change"
git push origin main
```

## Initial Setup
```powershell
git init
git branch -M main
git remote add origin https://github.com/ajaytester007/usaspending_enterprise_ai_solution.git
git add .
git commit -m "Initial working medallion pipeline"
git push -u origin main
```

## Branching
| Branch | Purpose |
|---|---|
| main | Stable baseline |
| feature/* | New functionality |
| hotfix/* | Urgent fixes |
| release/* | Release hardening |

## Tagging
```powershell
git tag -a build-1.0.0-databricks-working -m "Build 1.0.0 Databricks working dashboard version"
git push origin build-1.0.0-databricks-working
```

```powershell
git tag -a release-1.0.0-databricks-working -m "Release 1.0.0 Databricks Medallion Dashboard working baseline"
git push origin release-1.0.0-databricks-working
```

## GitHub Release
```powershell
gh release create v1.0.0 --verify-tag --title "USASpending Enterprise AI Solution v1.0.0" --notes "Initial enterprise release with PySpark medallion architecture, Flask dashboards, SparkSQL analytics, GitHub Actions CI/CD, RAG/MCP scaffolding, and Databricks-ready enterprise analytics foundation."
```

## Wiki Propagation
GitHub Wiki is a separate Git repo.

```powershell
cd C:\GitHub
git clone https://github.com/ajaytester007/usaspending_enterprise_ai_solution.wiki.git
cd usaspending_enterprise_ai_solution.wiki
copy ..\usaspending_enterprise_ai_solution\docs\wiki\*.md .
git add .
git commit -m "Update enterprise wiki documentation"
git push
```

## Release Checklist
- Main pushed
- CI passing
- Notebook export committed
- Dashboard SQL committed
- Wiki docs updated
- Tag pushed
- GitHub release created
