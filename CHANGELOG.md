# Changelog

All notable changes to this project are documented here.

The format follows Semantic Versioning and Keep a Changelog conventions.

## [Unreleased]

### Planned
- Expanded multi-cloud cost policy support
- Additional FinOps reporting integrations
- Broader infrastructure provider coverage

## [1.0.0] - 2026-09-11

### Added
- YAML-driven FinOps policy configuration
- Python policy generation engine
- Jinja2-based Rego policy generation
- Multi-environment monthly budget policies
- Resource-level EC2 and EBS cost guardrails
- Cost increase percentage guardrail
- Automated OPA policy tests
- Python unit tests for policy generation and cost analytics
- Terraform infrastructure with reusable FinOps stack module
- Development environment configuration
- LocalStack-compatible AWS infrastructure testing
- Ansible webserver deployment and FinOps dashboard
- Dockerized OPA execution
- Infracost-based infrastructure cost estimation
- Automated cost analysis and Markdown reporting
- GitHub Actions FinOps policy enforcement
- Pull request cost-policy reporting
- Slack notification integration
- Security scanning with Gitleaks
- Python dependency auditing with pip-audit
- Pre-commit quality gates with Ruff and yamllint
- Pinned OPA container image using an immutable digest
- Architecture Decision Records documenting major design choices

### Engineering
- Removed dependency on Windows-only `opa.exe`
- Added reproducible local OPA execution
- Added Terraform formatting and validation checks
- Added Ansible syntax validation
- Added CI coverage for policy, infrastructure, automation, and security checks

[Unreleased]: https://github.com/AryanThakur30/finops-policy-as-code-engine/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/AryanThakur30/finops-policy-as-code-engine/releases/tag/v1.0.0
