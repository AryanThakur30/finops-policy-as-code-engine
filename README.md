# FinOps Policy as Code Engine

A policy-driven FinOps pipeline that automatically evaluates infrastructure cost changes before they are merged into the main branch.

The project combines Terraform, Infracost, Open Policy Agent (OPA), Rego, Docker, and GitHub Actions to enforce infrastructure cost guardrails directly in the development workflow.

## Architecture

Terraform
   |
   v
Infracost
   |
   v
Infrastructure Cost Estimate
   |
   v
OPA + Rego Policy
   |
   v
GitHub Actions
   |
   v
Pull Request Cost Enforcement

## How It Works

1. Infrastructure is defined using Terraform.
2. Infracost generates an estimated monthly infrastructure cost.
3. The estimate is evaluated against a Rego-based FinOps policy.
4. Open Policy Agent evaluates whether the cost violates the configured guardrail.
5. GitHub Actions runs the complete validation automatically on pull requests.
6. Infracost posts the policy result directly to the GitHub pull request.
7. A cost violation causes the CI check to fail, preventing an unsafe change from being treated as compliant.

## Current Cost Policy

The current policy enforces a maximum monthly infrastructure cost of:

.00

Example policy result:

Actual monthly cost: .12
Maximum allowed cost: .00

Result:

Policy violation

The CI pipeline therefore exits with code 1 and reports the violation on the pull request.

## Project Structure

`	ext
finops-policy-as-code-engine/
|
|-- .github/
|   -- workflows/
|       -- infracost.yml
|
|-- policies/
|   -- cost.rego
|
|-- terraform/
|   -- main.tf
|
|-- .gitignore
-- README.md
