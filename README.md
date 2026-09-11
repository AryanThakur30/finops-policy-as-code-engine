
# 💰 FinOps Policy as Code Engine

<p align="center">
  <img src="https://img.shields.io/badge/FinOps-Policy%20as%20Code-00A67E?style=for-the-badge" alt="FinOps">
  <img src="https://img.shields.io/badge/Open%20Policy%20Agent-OPA-7B61FF?style=for-the-badge" alt="OPA">
  <img src="https://img.shields.io/badge/Terraform-IaC-844FBA?style=for-the-badge" alt="Terraform">
  <img src="https://img.shields.io/badge/Ansible-Automation-EE0000?style=for-the-badge" alt="Ansible">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge" alt="Python">
  <img src="https://img.shields.io/badge/Jinja2-Templates-B41717?style=for-the-badge" alt="Jinja2">
  <img src="https://img.shields.io/badge/Docker-Reproducible-2496ED?style=for-the-badge" alt="Docker">
</p>

<p align="center">
  <strong>Automated cloud cost governance using Infrastructure as Code, Policy as Code, cost analytics, and CI/CD enforcement.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OPA%20Tests-10%2F10-success?style=flat-square" alt="OPA Tests">
  <img src="https://img.shields.io/badge/Python%20Tests-10%2F10-success?style=flat-square" alt="Python Tests">
  <img src="https://img.shields.io/badge/Terraform-Validated-success?style=flat-square" alt="Terraform">
  <img src="https://img.shields.io/badge/Ansible-Syntax%20Validated-success?style=flat-square" alt="Ansible">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License">
</p>

---

## 🚀 Overview

**FinOps Policy as Code Engine** brings cloud cost governance directly into the infrastructure delivery lifecycle.

Instead of discovering excessive cloud spending after deployment, infrastructure changes are evaluated during the pull request process.

The system combines:

- 💰 Infracost for infrastructure cost estimation
- 📜 Open Policy Agent for policy enforcement
- 🐍 Python for policy generation and cost analytics
- 🧩 Jinja2 for maintainable Rego templates
- 🏗️ Terraform for infrastructure as code
- 🔧 Ansible for FinOps dashboard deployment
- 🐳 Docker for reproducible OPA execution
- 🔄 GitHub Actions for CI/CD enforcement
- 💬 GitHub PR reporting
- 🚨 Slack notifications for policy violations

The core idea is simple:

> **Make cloud cost a deployment constraint before it becomes a cloud bill.**

---

# 🧠 Architecture

```text
                         ┌─────────────────────┐
                         │    Pull Request     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Terraform      │
                         │   Infrastructure    │
                         │       Changes      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      Infracost      │
                         │  Cost Estimation    │
                         └──────────┬──────────┘
                                    │
                                    ▼
                    ┌──────────────────────────────┐
                    │       Python Analytics       │
                    │                              │
                    │  analyze_cost.py             │
                    │  • Current cost              │
                    │  • Previous cost              │
                    │  • Cost delta                 │
                    │  • Increase percentage        │
                    │  • Resource analysis          │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │     YAML Policy Config       │
                    │                              │
                    │     policies.yml              │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │     Python + Jinja2           │
                    │     Policy Generator          │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                    ┌──────────────────────────────┐
                    │        Generated Rego        │
                    │      cost.rego                │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         ┌─────────────────────┐
                         │         OPA         │
                         │  Policy Evaluation  │
                         └──────────┬──────────┘
                                    │
                           ┌────────┴────────┐
                           │                 │
                           ▼                 ▼
                        ✅ PASS            ❌ FAIL
                           │                 │
                           │          ┌──────┴────────┐
                           │          │               │
                           │          ▼               ▼
                           │     PR Report      Slack Alert
                           │
                           ▼
                  Continue Infrastructure Flow
✨ Key Features
Feature	Technology	Purpose
💰 Cost estimation	Infracost	Estimate infrastructure cost before deployment
📜 Policy as Code	OPA + Rego	Enforce FinOps rules automatically
⚙️ Policy generation	Python + Jinja2	Generate policies from YAML configuration
🧠 Cost analytics	Python	Analyze and enrich cost data
🏗️ Infrastructure	Terraform	Define realistic cloud infrastructure
🔧 Configuration	Ansible	Deploy the FinOps dashboard
🐳 Reproducibility	Docker	Run OPA consistently locally and in CI
🧪 Policy testing	OPA	Validate FinOps rules
🧪 Unit testing	Pytest	Validate Python logic
🔄 CI/CD	GitHub Actions	Automate the entire governance pipeline
💬 PR reporting	Infracost + GitHub	Surface cost information directly in PRs
🚨 Notifications	Slack	Alert on policy violations
📊 Dashboard	Ansible + Jinja2	Render FinOps cost information
💵 FinOps Policy Engine

The policy engine supports multiple layers of cost governance.

1. Environment-Specific Budgets

Each environment can have its own monthly budget.

budgets:
  development:
    monthly_limit: 100

  staging:
    monthly_limit: 250

  production:
    monthly_limit: 500

This means:

Development → $100/month
Staging     → $250/month
Production  → $500/month

A development infrastructure change estimated at $101/month fails even though production has a higher budget.

2. Cost Increase Guardrail

The engine compares the current monthly cost with the previous monthly cost.

Previous monthly cost: $250.00
Current monthly cost:  $281.12

Monthly increase:
($281.12 - $250.00) / $250.00 × 100

= 12.45%

With a configured maximum increase of 20%, this passes.

A 30% increase fails.

Configuration:

cost_increase:
  enabled: true
  max_percentage: 20
3. Resource-Level Cost Policies

Individual resource categories can have their own limits.

resources:
  ec2:
    enabled: true
    max_monthly_cost: 200

  ebs:
    enabled: true
    max_monthly_cost: 100

This prevents a single expensive resource from being hidden inside an otherwise acceptable infrastructure budget.

🧩 Configuration-Driven Policy Generation

The project separates policy configuration from policy implementation.

policy-generator/config/policies.yml
                │
                ▼
       generate_policies.py
                │
                ▼
          Jinja2 Template
                │
                ▼
    policies/generated/cost.rego
                │
                ▼
               OPA

This provides a cleaner workflow than manually editing large Rego files whenever a budget changes.

Example:

development:
  monthly_limit: 100

can generate a Rego rule equivalent to:

deny contains out if {
    input.environment == "development"
    actualCost := to_number(input.totalMonthlyCost)
    actualCost >= 100
}

The generated policy is deterministic and reproducible from the YAML configuration.

🐍 Python Automation

The custom Python layer contains two meaningful components.

Policy Generator

generate_policies.py:

Reads YAML configuration
Validates configured policy structures through generation logic
Loads Jinja2 templates
Generates Rego
Creates the output directory when required
Produces a deterministic policy file

Usage:

python policy-generator/src/generate_policies.py \
  --config policy-generator/config/policies.yml \
  --output policies/generated/cost.rego
Cost Analytics

analyze_cost.py processes the Infracost JSON output.

It calculates and exposes:

Environment
Current monthly cost
Previous monthly cost
Monthly cost delta
Percentage increase
Resource count
Top resources

Example:

FinOps Cost Analysis

Environment: development
Current monthly cost: $281.12
Previous monthly cost: $250.00
Monthly delta: $31.12
Cost increase: 12.45%
Resources analyzed: 2
🛡️ OPA Policy Testing

The project contains an automated OPA test suite covering both valid and invalid infrastructure scenarios.

Current result:

PASS: 10/10

Test coverage includes:

Development $80       → PASS
Development $99       → PASS
Development $100      → FAIL
Development $281      → FAIL

Cost increase 12.5%  → PASS
Cost increase 30%    → FAIL

Staging $250          → FAIL
Production $500       → FAIL

EC2 $250              → FAIL
EBS $120              → FAIL

OPA runs inside Docker to keep policy execution reproducible.

Run locally:

docker compose build
docker compose run --rm opa

Expected:

PASS: 10/10
🧪 Python Test Suite

The Python automation layer is covered by Pytest.

The tests validate:

Environment-specific policy generation
Cost increase guardrails
Resource-level policies
Generated policy structure
Cost analytics
Environment enrichment
Cost calculations
Resource analysis

Run:

pytest -q policy-generator/tests

Expected:

10 passed
🏗️ Terraform Infrastructure

The Terraform configuration models a realistic infrastructure stack rather than a single placeholder resource.

VPC
│
├── Subnet
│
├── Security Group
│
├── EC2 Instance
│
└── EBS Volume

The configuration uses reusable modules and environment-specific variables.

terraform/
│
├── environments/
│   └── development.tfvars
│
├── modules/
│   └── finops_stack/
│       ├── compute.tf
│       ├── network.tf
│       ├── security.tf
│       ├── variables.tf
│       └── outputs.tf
│
├── main.tf
├── providers.tf
├── variables.tf
└── outputs.tf

Terraform validation:

terraform -chdir=terraform init -backend=false
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform validate

Expected:

Success! The configuration is valid.

The project uses LocalStack-compatible provider endpoints for local development and validation, avoiding the need for a real AWS deployment during testing.

🔧 Ansible FinOps Dashboard

Ansible is not included merely as a generic configuration-management example.

It is connected to the FinOps pipeline.

The flow is:

Infracost JSON
      │
      ▼
Python Cost Analytics
      │
      ▼
FinOps Dashboard Variables
      │
      ▼
Ansible Role
      │
      ▼
Jinja2 Dashboard Template
      │
      ▼
FinOps Dashboard

The Ansible role can:

Install Nginx
Create the dashboard directory
Render the FinOps dashboard
Configure an Nginx virtual host
Enable the dashboard site
Disable the default Nginx site
Restart Nginx when configuration changes
Ensure Nginx is enabled and running

The role also supports a render-only CI mode, allowing the dashboard template to be validated without privileged system configuration.

Validate:

ansible-playbook \
  -i ansible/inventory.ini \
  --syntax-check \
  ansible/site.yml
🐳 Docker

OPA execution is containerized using Docker.

docker/
└── Dockerfile.opa

docker-compose.yml

The container consumes the canonical policy locations:

policies/generated/cost.rego
policies/cost_test.rego

Run:

docker compose build
docker compose run --rm opa

This removes the dependency on a platform-specific opa.exe binary.

🔄 GitHub Actions CI/CD

The entire governance process is automated through GitHub Actions.

Pull Request
     │
     ▼
Terraform fmt
     │
     ▼
Terraform init
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
Dockerized OPA tests
     │
     ▼
Ansible syntax validation
     │
     ▼
Infracost estimation
     │
     ▼
Python cost analytics
     │
     ▼
FinOps dashboard rendering
     │
     ▼
FinOps policy enforcement
     │
     ├───────────────┐
     ▼               ▼
   PASS             FAIL
     │               │
     ▼               ├── GitHub PR report
 Continue            ├── Slack alert
                     └── Workflow failure

The workflow runs when relevant infrastructure, policy, automation, Docker, or workflow files change.

🚨 Example Policy Violation

Consider an infrastructure change that produces:

Environment: development

Configured budget:
$100.00/month

Estimated cost:
$281.12/month

The policy engine produces a violation similar to:

Monthly infrastructure cost for development
must be less than $100.00
(actual cost is $281.12)

The GitHub Actions job then fails.

This creates a cost gate directly inside the infrastructure review process.

📊 Example Cost Analysis

Example input:

{
  "totalMonthlyCost": "281.12",
  "pastTotalMonthlyCost": "250.00",
  "projects": [
    {
      "breakdown": {
        "resources": [
          {
            "name": "aws_instance.web",
            "monthlyCost": "220.00"
          },
          {
            "name": "aws_ebs_volume.data",
            "monthlyCost": "61.12"
          }
        ]
      }
    }
  ]
}

The analytics engine derives:

Current cost       = $281.12
Previous cost      = $250.00
Monthly delta      = $31.12
Increase           = 12.45%
Resources analyzed = 2

The enriched data is then consumed by downstream FinOps automation.

📁 Project Structure
finops-policy-as-code-engine/
│
├── .github/
│   └── workflows/
│       └── infracost.yml
│
├── ansible/
│   ├── inventory.ini
│   ├── site.yml
│   └── roles/
│       └── webserver/
│           ├── defaults/
│           │   └── main.yml
│           ├── handlers/
│           │   └── main.yml
│           ├── tasks/
│           │   └── main.yml
│           └── templates/
│               ├── dashboard.html.j2
│               └── finops-dashboard.conf.j2
│
├── docker/
│   └── Dockerfile.opa
│
├── policies/
│   ├── cost.rego
│   ├── cost_test.rego
│   └── generated/
│       └── cost.rego
│
├── policy-generator/
│   ├── config/
│   │   └── policies.yml
│   ├── src/
│   │   ├── analyze_cost.py
│   │   └── generate_policies.py
│   ├── templates/
│   │   └── cost.rego.j2
│   ├── tests/
│   │   └── test_generator.py
│   └── requirements.txt
│
├── terraform/
│   ├── environments/
│   │   └── development.tfvars
│   ├── modules/
│   │   └── finops_stack/
│   ├── main.tf
│   ├── outputs.tf
│   ├── providers.tf
│   └── variables.tf
│
├── docker-compose.yml
├── LICENSE
├── .gitignore
└── README.md
⚙️ Local Setup
1. Clone
git clone https://github.com/AryanThakur30/finops-policy-as-code-engine.git

cd finops-policy-as-code-engine
2. Create Python Environment
python3 -m venv policy-generator/.venv

source policy-generator/.venv/bin/activate

pip install -r policy-generator/requirements.txt
3. Generate the Policy
python policy-generator/src/generate_policies.py \
  --config policy-generator/config/policies.yml \
  --output policies/generated/cost.rego
4. Run Python Tests
pytest -q policy-generator/tests
5. Run OPA Tests
docker compose build
docker compose run --rm opa
6. Validate Terraform
terraform -chdir=terraform init -backend=false
terraform -chdir=terraform fmt -check -recursive
terraform -chdir=terraform validate
7. Validate Ansible
ansible-playbook \
  -i ansible/inventory.ini \
  --syntax-check \
  ansible/site.yml
🔐 GitHub Secrets

The CI workflow supports the following repository secrets:

INFRACOST_API_KEY
SLACK_WEBHOOK_URL

SLACK_WEBHOOK_URL is optional.

If it is not configured, the workflow skips the Slack notification safely.

Never commit:

API keys
Passwords
Private keys
Cloud credentials
Slack webhook URLs

to the repository.

🧪 Validation Status
Component	Result
🐍 Python tests	✅ 10/10
🛡️ OPA tests	✅ 10/10
🏗️ Terraform validation	✅ Valid
🔧 Ansible syntax	✅ Valid
🧩 Jinja2 policy generation	✅ Integrated
🐳 Dockerized OPA	✅ Working
💰 Infracost	✅ Integrated
📊 Python cost analytics	✅ Working
📊 FinOps dashboard rendering	✅ Integrated
🔄 GitHub Actions	✅ Automated
💬 PR cost reporting	✅ Integrated
🚨 Slack notification	✅ Supported
🎯 Engineering Principles
Shift-Left FinOps

Cost governance happens during infrastructure review rather than after deployment.

Policy as Code

FinOps rules are version-controlled, testable, reviewable, and executable.

Configuration Driven

Budgets and resource limits are defined through YAML rather than being scattered across the codebase.

Reproducible Execution

OPA runs through Docker so the policy runtime is consistent across development and CI.

Modular Infrastructure

Terraform uses reusable modules and environment-specific configuration.

Automated Enforcement

A pull request can automatically trigger:

Cost estimation
      ↓
Analytics
      ↓
Policy generation
      ↓
Policy tests
      ↓
Policy enforcement
      ↓
PR feedback
      ↓
Notification
📈 Why FinOps Policy as Code?

Traditional cloud cost monitoring primarily answers:

"How much did we spend?"

This project focuses on a different question:

"Should this infrastructure change be allowed?"

That changes cost governance from a reporting problem into an engineering control.

Instead of waiting for the monthly cloud bill, teams can identify problematic infrastructure changes before they are deployed.

🚀 Future Roadmap

The architecture can be extended with:

📈 Cost anomaly detection
🏷️ Mandatory cost-center and ownership tags
☁️ Multi-cloud policy support
📅 Budget forecasting
🔍 Automated resource optimization recommendations
🤖 Automated remediation
📊 Historical cost trends
🔐 Approval workflows for policy exceptions
🧠 AI-assisted FinOps recommendations
📉 Cost optimization suggestions based on utilization
🛠️ Technology Stack
Infrastructure
└── Terraform

Cost Intelligence
└── Infracost
└── Python

Policy Engine
└── Open Policy Agent
└── Rego
└── Jinja2

Configuration Management
└── Ansible
└── Nginx

Reproducibility
└── Docker
└── Docker Compose

CI/CD
└── GitHub Actions

Notifications
└── Slack
📜 License

This project is licensed under the MIT License.

See the LICENSE file for details.

👨‍💻 Author
Aryan Thakur

GitHub:

https://github.com/AryanThakur30

Project:

https://github.com/AryanThakur30/finops-policy-as-code-engine

💰 Make cloud cost a constraint before it becomes a bill.</strong> </p> <p align="center"> Terraform • Infracost • Python • Jinja2 • Rego • OPA • Ansible • Docker • GitHub Actions • Slack </p> EOF

echo "===== README READY ====="
wc -l README.md

echo
echo "===== README CHECK ====="
grep -n "FinOps Policy as Code Engine|Architecture|Policy Engine|Ansible FinOps Dashboard|GitHub Actions|Validation Status|MIT License" README.md

echo
echo "===== GIT STATUS ====="
git status --short
