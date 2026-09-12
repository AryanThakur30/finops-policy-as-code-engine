@'
# FinOps Policy as Code Engine

[![FinOps Cost Policy](https://github.com/AryanThakur30/finops-policy-as-code-engine/actions/workflows/infracost.yml/badge.svg)](https://github.com/AryanThakur30/finops-policy-as-code-engine/actions/workflows/infracost.yml)
[![Security Checks](https://github.com/AryanThakur30/finops-policy-as-code-engine/actions/workflows/security.yml/badge.svg)](https://github.com/AryanThakur30/finops-policy-as-code-engine/actions/workflows/security.yml)
[![Release](https://img.shields.io/github/v/release/AryanThakur30/finops-policy-as-code-engine)](https://github.com/AryanThakur30/finops-policy-as-code-engine/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A production-style FinOps Policy as Code pipeline that analyzes infrastructure cost, generates OPA/Rego policies from YAML configuration, evaluates Terraform infrastructure against cost guardrails, and reports violations automatically through GitHub Actions.

The goal is simple:

> **Prevent infrastructure cost from becoming a production surprise.**

Instead of reviewing cloud cost after infrastructure is deployed, this project moves cost governance into the infrastructure delivery workflow.

---

## What This Project Does

The engine combines Terraform, Infracost, Python, OPA/Rego, Ansible, Docker and GitHub Actions into one automated FinOps workflow.

```text
Developer
   │
   ▼
Terraform Infrastructure
   │
   ├── Terraform fmt / validate
   │
   ▼
Infracost
   │
   ▼
Cost JSON
   │
   ▼
Python Cost Analytics
   │
   ├── enriched cost data
   └── Markdown report
   │
   ▼
YAML Policy Configuration
   │
   ▼
Python + Jinja2
   │
   ▼
Generated OPA/Rego Policies
   │
   ▼
Key Capabilities
Policy as Code

FinOps rules are expressed as version-controlled policy configuration instead of being hidden inside CI scripts.

The current policy engine supports:

Environment-specific monthly budgets
Development, staging and production limits
Resource-level EC2 cost limits
Resource-level EBS cost limits
Monthly cost increase guardrails
Multiple simultaneous policy violations
Human-readable violation messages
Automated OPA tests

Example configuration:

budgets:
  development:
    monthly_limit: 100
  staging:
    monthly_limit: 250
  production:
    monthly_limit: 500

cost_increase:
  enabled: true
  max_percentage: 20

resources:
  ec2:
    enabled: true
    max_monthly_cost: 200
  ebs:
    enabled: true
    max_monthly_cost: 100

Changing a budget does not require manually rewriting Rego. The policy generator converts the configuration into executable policies.

Python Automation

Python is used as application logic, not just as a helper script.

The policy-generator component provides:

YAML configuration loading
Configuration validation
Dynamic Rego policy generation
Jinja2-based policy templating
CLI execution
Cost analysis
Enriched cost JSON generation
Markdown cost reporting
Automated unit tests

The generator produces the canonical policy file:

policies/generated/cost.rego

Generated policies are intentionally separated from handwritten policy/configuration sources so the generated artifact can be reproduced deterministically.

Cost Guardrails

The policy engine evaluates several dimensions of infrastructure cost.

Environment budgets
development < $100/month
staging     < $250/month
production  < $500/month
Resource-level controls
EC2 < $200/month
EBS < $100/month
Cost increase control

The engine can reject infrastructure when monthly cost increases beyond the configured percentage.

For example:

Previous: $200/month
Current:  $260/month
Increase: 30%

Allowed increase: 20%

Result: POLICY VIOLATION

Example violation:

Monthly infrastructure cost must be less than $100.00
(actual cost is $281.12)
OPA / Rego

Open Policy Agent provides the policy evaluation layer.

OPA is executed through Docker rather than relying on a platform-specific binary.

The container image is pinned by SHA256 digest for reproducible execution:

FROM openpolicyagent/opa:1.20.2@sha256:7b15f9d96345dfa639322ad97f65a0b38260f95efcdd7f5c24e284228708f06c

This removes the previous Windows-only opa.exe dependency and makes local and CI evaluation consistent.

Automated Policy Tests

The repository includes OPA tests covering:

Development budget pass
Development budget boundary
Development budget violation
Cost increase within limit
Cost increase violation
Staging budget violation
Production budget violation
EC2 resource violation
EBS resource violation
Generated policy behaviour

Current validation:

OPA tests:     10 / 10 PASS
Python tests:  10 / 10 PASS
Terraform:     validate PASS
Terraform Infrastructure

The Terraform layer represents a realistic infrastructure scenario instead of a single placeholder resource.

It includes:

VPC
Subnet
Security group
EC2 instance
EBS volume
Variables
Outputs
Reusable Terraform module
Environment-specific configuration

Structure:

terraform/
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
├── environments/
│   └── development.tfvars
└── modules/
    └── finops_stack/
        ├── main.tf
        ├── variables.tf
        └── outputs.tf

Terraform validation is performed in CI using:

terraform fmt -check -recursive
terraform init -backend=false
terraform validate

LocalStack is used for local AWS-compatible testing, so the infrastructure workflow can be exercised without requiring a real AWS account.

Infracost Integration

Infracost converts Terraform infrastructure into estimated cloud cost data.

The CI pipeline:

Initializes Terraform
Generates an Infracost estimate
Produces JSON cost data
Runs Python cost analytics
Generates a Markdown report
Evaluates the result against OPA policies
Comments the result on the Pull Request
Fails the workflow when a mandatory policy is violated
Optionally sends a Slack notification

This turns cost estimation into an actual CI quality gate.

Ansible

Ansible is used for the deployment/configuration layer.

The role:

Installs Nginx
Configures the service
Deploys the FinOps dashboard
Configures the Nginx site
Enables the site
Disables the default site
Starts/enables the service
Uses a handler for service restart

Dashboard templates:

ansible/roles/webserver/templates/
├── dashboard.html.j2
└── finops-dashboard.conf.j2

Ansible syntax is validated in CI.

Docker

OPA is containerized for reproducible local policy evaluation.

docker/
└── Dockerfile.opa

docker-compose.yml

Run the policy test environment with:

docker compose build
docker compose run --rm opa-tests

This gives developers the same OPA execution model used by the project instead of depending on a locally installed platform-specific binary.

CI/CD Pipeline

The main FinOps workflow is designed around Pull Request governance.

Pull Request
     │
     ▼
Terraform fmt
     │
     ▼
Terraform validate
     │
     ▼
Python dependencies
     │
     ▼
Python tests
     │
     ▼
Generate Rego
     │
     ▼
Docker OPA tests
     │
     ▼
Ansible syntax check
     │
     ▼
Infracost estimate
     │
     ▼
Python cost analytics
     │
     ▼
OPA policy enforcement
     │
     ├── PASS ──► PR succeeds
     │
     └── FAIL ──► PR comment
                    │
                    ├── Slack alert (if configured)
                    └── CI failure

The workflow therefore treats infrastructure cost as a first-class engineering quality gate.

Security and Supply Chain Controls

The repository also includes engineering-quality and security checks.

Gitleaks

Detects accidentally committed secrets.

pip-audit

Audits Python dependencies for known vulnerabilities.

pre-commit

Runs repository quality gates before commits.

Configured checks include:

Ruff
Ruff formatting
yamllint
Gitleaks
trailing whitespace detection
EOF normalization
YAML validation
large-file detection
Immutable OPA image

The OPA container is pinned by digest instead of relying only on a mutable image tag.

Architecture Decisions

Important design choices are documented as ADRs:

docs/adr/
├── README.md
├── ADR-001-use-opa-rego.md
├── ADR-002-yaml-policy-configuration.md
└── ADR-003-generated-rego-policies.md

The ADRs explain:

Why OPA/Rego was selected
Why YAML is the policy configuration surface
Why policies are generated rather than maintained entirely by hand
The trade-offs against alternative approaches
Project Structure
finops-policy-as-code-engine/
│
├── .github/
│   └── workflows/
│       ├── infracost.yml
│       └── security.yml
│
├── ansible/
│   ├── inventory.ini
│   ├── site.yml
│   └── roles/
│       └── webserver/
│
├── docker/
│   └── Dockerfile.opa
│
├── docs/
│   └── adr/
│
├── policies/
│   ├── cost.rego
│   ├── cost_test.rego
│   └── generated/
│       └── cost.rego
│
├── policy-generator/
│   ├── config/
│   │   └── policies.yaml
│   ├── src/
│   │   ├── generate_policies.py
│   │   └── analyze_cost.py
│   ├── tests/
│   │   └── test_generator.py
│   └── requirements.txt
│
├── terraform/
│   ├── environments/
│   └── modules/
│       └── finops_stack/
│
├── .pre-commit-config.yaml
├── .yamllint.yml
├── CHANGELOG.md
├── docker-compose.yml
├── LICENSE
└── README.md
Local Setup
Requirements

Install:

Python 3.12+
Terraform
Docker
Docker Compose
Ansible
Infracost
Git

OPA itself does not need to be installed on Windows. Docker is used for policy evaluation.

Python environment
cd policy-generator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Generate policies
python src/generate_policies.py \
  --config config/policies.yaml \
  --output ../policies/generated/cost.rego
Run Python tests
pytest -q
Validate Terraform
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform validate
Run OPA tests
docker compose build
docker compose run --rm opa-tests
Run Ansible syntax validation
cd ansible
ansible-playbook site.yml --syntax-check
GitHub Configuration

For the complete CI workflow, configure the following repository secrets where required:

INFRACOST_API_KEY
SLACK_WEBHOOK_URL   # optional

SLACK_WEBHOOK_URL is optional. The workflow skips the Slack notification when it is not configured.

Release

The project follows semantic versioning.

Current release:

v1.0.0

Release history is maintained in:

CHANGELOG.md
Validation Status

The final development state has been validated across the major engineering layers:

Python tests          10 / 10 PASS
OPA tests             10 / 10 PASS
Terraform validate    PASS
Terraform fmt         PASS
Ansible syntax        PASS
pip-audit             PASS
pre-commit checks     PASS
Gitleaks              PASS
Docker OPA            PASS
Infracost integration PASS
CI policy enforcement  PASS
Engineering Principles

This project intentionally demonstrates more than infrastructure provisioning.

The main engineering principles are:

Infrastructure cost is treated as code.
Policies are version-controlled and reproducible.
Configuration is separated from generated policy.
Cost analysis happens before infrastructure approval.
Policy enforcement is automated rather than manual.
Local execution and CI execution use the same OPA container model.
Infrastructure, policy, application logic and configuration are tested independently.
Security and dependency checks are part of CI.
Architecture decisions are documented with ADRs.
Releases are versioned using semantic versioning.
Roadmap

Possible future extensions:

AWS Organizations / multi-account cost policies
Cost allocation by team or project
FinOps budget forecasting
Historical cost trend analysis
Policy exemptions with approval workflows
Additional cloud providers
Terraform plan JSON ingestion
Automated remediation workflows
Dashboard deployment to a managed environment
License

This project is licensed under the MIT License. See LICENSE.

Author

Aryan Thakur

GitHub: @AryanThakur30
OPA Policy Evaluation
   │
   ├── PASS → Pull Request continues
   │
   └── FAIL → PR report + optional Slack alert
