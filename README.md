<div align="center">

# 💰 FinOps Policy as Code Engine

### 🚦 Automated Cloud Cost Governance Before Deployment

<p>
  <strong>Terraform</strong> •
  <strong>Infracost</strong> •
  <strong>Open Policy Agent</strong> •
  <strong>Python</strong> •
  <strong>Ansible</strong> •
  <strong>Docker</strong> •
  <strong>GitHub Actions</strong>
</p>

<br>

<img src="https://img.shields.io/badge/FinOps-Policy%20as%20Code-00C853?style=for-the-badge&logo=googlecloud&logoColor=white">
<img src="https://img.shields.io/badge/Terraform-Infrastructure-7B42BC?style=for-the-badge&logo=terraform&logoColor=white">
<img src="https://img.shields.io/badge/OPA-Rego-EF7B4D?style=for-the-badge&logo=openpolicyagent&logoColor=white">
<img src="https://img.shields.io/badge/Python-Automation-3776AB?style=for-the-badge&logo=python&logoColor=white">

<br>

<img src="https://img.shields.io/badge/Docker-Reproducible-2496ED?style=for-the-badge&logo=docker&logoColor=white">
<img src="https://img.shields.io/badge/Ansible-Configuration-EE0000?style=for-the-badge&logo=ansible&logoColor=white">
<img src="https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?style=for-the-badge&logo=githubactions&logoColor=white">
<img src="https://img.shields.io/badge/LocalStack-Local%20AWS-6B4FBB?style=for-the-badge&logo=amazonaws&logoColor=white">

<br><br>

<img src="https://img.shields.io/badge/Policy%20Tests-10%2F10%20Passing-00C853?style=flat-square">
<img src="https://img.shields.io/badge/Python%20Tests-2%2F2%20Passing-00C853?style=flat-square">
<img src="https://img.shields.io/badge/Terraform-Validated-00C853?style=flat-square">
<img src="https://img.shields.io/badge/CI-Passing-00C853?style=flat-square">

</div>

---

## 🎯 What Is This?

**FinOps Policy as Code Engine** is an automated cloud cost-governance system that evaluates the financial impact of Terraform infrastructure **before it gets deployed**.

Instead of discovering excessive infrastructure costs after deployment, this project turns FinOps rules into executable policies and makes **cloud cost a CI/CD quality gate**.

```text
        Terraform Infrastructure
                  │
                  ▼
           💵 Infracost
                  │
                  ▼
          📊 Cost Analysis
                  │
                  ▼
          🧠 Open Policy Agent
                  │
          ┌───────┴────────┐
          ▼                ▼
       ✅ PASS           ❌ FAIL
          │                │
          ▼                ├── 💬 PR Report
      Merge Allowed        ├── 🔔 Slack Alert
                           └── 🚫 CI Failed
🚀 Why This Project?

Infrastructure can be technically correct and still be financially irresponsible.

A seemingly innocent Terraform change can introduce:

💸 Oversized EC2 instances
💾 Excessive EBS storage
📈 Unexpected cost increases
🏗️ Infrastructure beyond environment budgets
⚠️ Resource-level spending violations

Traditional CI/CD pipelines ask:

"Does the infrastructure work?"

This project adds another question:

"Can we afford this infrastructure?"

✨ Key Features
<table> <tr> <td width="50%">
💰 Multi-Environment Budgets

Different environments can have different monthly limits.

development: $100
staging:     $250
production:  $500
</td> <td width="50%">
📈 Cost Increase Guardrails

Detect infrastructure changes that increase monthly cost beyond an allowed percentage.

max_percentage: 20
</td> </tr> <tr> <td>
🖥️ Resource-Level Policies

Control individual resource categories.

EC2 < $200/month
EBS < $100/month
</td> <td>
🤖 Automated Enforcement

Every pull request can automatically run:

Terraform → Infracost → OPA

No manual cost review required.

</td> </tr> <tr> <td>
🧪 Automated Testing

The project tests:

Rego policies
Python generator
Terraform
Ansible
</td> <td>
🔔 Developer Feedback

Policy failures are surfaced directly in the PR with:

Cost estimate
Failed policy
Violation message
Optional Slack alert
</td> </tr> </table>
🧠 Policy as Code

FinOps rules are not hardcoded into the CI pipeline.

They are defined through YAML:

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

A custom Python engine converts this configuration into executable Rego.

┌──────────────────┐
│   policy.yml     │
│                  │
│ Budgets          │
│ Resource Limits  │
│ Cost Guardrails  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Python Generator │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Generated Rego   │
│                  │
│ cost.rego        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Open Policy      │
│ Agent            │
└──────────────────┘

This makes policy management:

Configurable → Version Controlled → Testable → Automated

🛡️ Example FinOps Enforcement

Suppose a Terraform change produces:

Estimated Monthly Cost
        ↓
     $281.12

But the development environment has:

Monthly Budget
        ↓
     $100.00

OPA evaluates the infrastructure and returns:

❌ POLICY VIOLATION

Monthly infrastructure cost for development
must be less than $100.00

Actual Cost: $281.12

The GitHub Actions workflow then fails the pull request.

Result
Terraform      ✅
Python Tests   ✅
OPA Tests      ✅
Ansible        ✅
Infracost      ✅
Cost Policy    ❌
──────────────────
CI Result       ❌ BLOCKED
📊 Cost Increase Protection

The engine can compare the current infrastructure cost against a previous baseline.

Example:

Previous Cost     $200/month
Current Cost      $260/month
────────────────────────────
Increase          30%
Allowed           20%

Result            ❌ BLOCKED

This catches expensive infrastructure changes even when the absolute environment budget has not been exceeded.

🏗️ Infrastructure Architecture

The Terraform infrastructure represents a realistic cloud environment rather than a single demo resource.

                         ☁️ Cloud Infrastructure
                                  │
                                  ▼
                              ┌───────┐
                              │  VPC  │
                              └───┬───┘
                                  │
                         ┌────────┴────────┐
                         │                 │
                         ▼                 ▼
                  Public Subnet      Security Group
                         │                 │
                         └────────┬────────┘
                                  │
                                  ▼
                             ┌─────────┐
                             │   EC2   │
                             └────┬────┘
                                  │
                                  ▼
                             ┌─────────┐
                             │   EBS   │
                             └─────────┘

Terraform uses a reusable module architecture:

terraform/
│
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
│
├── environments/
│   └── development.tfvars
│
└── modules/
    └── finops_stack/
        ├── compute.tf
        ├── network.tf
        ├── security.tf
        ├── variables.tf
        └── outputs.tf
⚙️ CI/CD Pipeline

The entire workflow is automated through GitHub Actions.

                 Pull Request
                       │
                       ▼
              ┌─────────────────┐
              │ Terraform       │
              │ fmt + validate  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Python Tests    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Generate Rego   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ OPA Policy Test │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Ansible Check   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Infracost    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Cost Analytics  │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ FinOps Policy   │
              │   Enforcement   │
              └────────┬────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
           ✅ PASS             ❌ FAIL
              │                 │
              ▼                 ├── 💬 PR Report
        Merge Allowed            ├── 🔔 Slack
                                  └── 🚫 CI Failed
🧪 Testing

The project has automated tests across multiple layers.

Layer	Validation
🏗️ Terraform	fmt + validate
🐍 Python	pytest
🧠 Rego	OPA test suite
⚙️ Ansible	Syntax validation
💵 Infracost	Cost estimation
🚦 Policy Engine	Automated enforcement
Current Policy Test Suite
✅ Development under budget
❌ Development at budget
❌ Development over budget

✅ Allowed cost increase
❌ Excessive cost increase

❌ Staging budget violation
❌ Production budget violation

❌ EC2 resource violation
❌ EBS resource violation
Test Result
┌──────────────────────────┐
│   OPA POLICY TESTS       │
│                          │
│       10 / 10            │
│        PASS ✅            │
└──────────────────────────┘

Python generator tests:

2 / 2 PASS ✅
🐍 Python Automation

The Python layer provides meaningful application logic rather than acting as a simple script wrapper.

Policy Generator
YAML Configuration
        ↓
Configuration Parsing
        ↓
Policy Generation
        ↓
Rego Output
Cost Analytics

The analytics component consumes Infracost JSON output and generates an environment-aware Markdown cost report.

This separates:

Cost Estimation

from:

Policy Enforcement

making the architecture easier to extend.

🐳 Dockerized OPA

The project includes a dedicated Docker environment for OPA.

docker/
└── Dockerfile.opa

docker-compose.yml

Run locally:

docker compose build
docker compose run --rm opa

Expected result:

PASS: 10/10

This removes dependency on a machine-specific OPA installation and makes local policy execution reproducible.

☁️ Local AWS Development

The project uses LocalStack for local AWS-compatible infrastructure testing.

This allows Terraform workflows to be exercised without requiring a real AWS deployment.

Developer Machine
       │
       ▼
   Terraform
       │
       ▼
   LocalStack
       │
       ▼
AWS-Compatible APIs

This keeps development:

Local → Reproducible → Low Cost

⚙️ Ansible Automation

Ansible provides the configuration-management layer.

ansible/
│
├── inventory.ini
├── site.yml
│
└── roles/
    └── webserver/
        ├── defaults/
        │   └── main.yml
        ├── handlers/
        │   └── main.yml
        ├── tasks/
        │   └── main.yml
        └── templates/
            └── index.html.j2

The role handles:

📦 Nginx installation
⚙️ Service configuration
🌍 Environment-aware deployment
🔄 Service restart handlers
🚀 Service enablement
🔔 Slack Notifications

FinOps policy failures can optionally trigger Slack notifications.

Configure the GitHub repository secret:

SLACK_WEBHOOK_URL

The pipeline remains fully functional without Slack configured.

Policy Failure
      │
      ├───────────────► GitHub PR Comment
      │
      └───────────────► Slack Alert 🔔
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
│
├── docker/
│   └── Dockerfile.opa
│
├── policy-generator/
│   ├── src/
│   │   ├── analyze_cost.py
│   │   └── generate_policies.py
│   ├── tests/
│   │   └── test_generator.py
│   └── requirements.txt
│
├── policies/
│   ├── generated/
│   │   └── cost.rego
│   └── cost_test.rego
│
├── terraform/
│   ├── main.tf
│   ├── providers.tf
│   ├── variables.tf
│   ├── outputs.tf
│   │
│   ├── environments/
│   │   └── development.tfvars
│   │
│   └── modules/
│       └── finops_stack/
│           ├── compute.tf
│           ├── network.tf
│           ├── security.tf
│           ├── variables.tf
│           └── outputs.tf
│
├── docker-compose.yml
├── .gitignore
└── README.md
🧰 Tech Stack
<div align="center">
Technology	Role
🟣 Terraform	Infrastructure as Code
🟠 Open Policy Agent	Policy Enforcement
🔵 Rego	Policy Language
🐍 Python	Automation & Analytics
💵 Infracost	Cloud Cost Estimation
🔴 Ansible	Configuration Management
🐳 Docker	Reproducible Execution
🟪 LocalStack	Local AWS Environment
⚫ GitHub Actions	CI/CD Automation
🔔 Slack	Notifications
🧪 Pytest	Python Testing
</div>
🎓 Engineering Concepts Demonstrated

This project combines multiple areas of modern DevOps and cloud engineering:

                 ┌─────────────────────┐
                 │       FinOps        │
                 └──────────┬──────────┘
                            │
       ┌────────────────────┼────────────────────┐
       ▼                    ▼                    ▼
 Infrastructure         Policy as Code        Automation
       │                    │                    │
       ▼                    ▼                    ▼
   Terraform               OPA                 Python
       │                    │                    │
       └────────────────────┼────────────────────┘
                            │
                            ▼
                         CI / CD
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
              GitHub                 Slack
📈 What This Project Solves
Traditional Problem	This Engine
💸 Discover cost after deployment	💰 Evaluate before deployment
🧑‍💻 Manual cost review	🤖 Automated policy enforcement
📋 Static cost documentation	🧠 Executable policies
🔒 Hardcoded thresholds	⚙️ YAML-driven configuration
🧪 Untested policies	✅ Automated OPA tests
🖥️ Machine-specific tooling	🐳 Dockerized OPA
☁️ Real AWS required for experiments	🧪 LocalStack
📢 Cost issue discovered later	💬 PR feedback immediately
🔥 Example End-to-End Scenario

A developer increases infrastructure capacity.

Step 1

Terraform describes the infrastructure.

Terraform
    ↓
EC2 + EBS + Network
Step 2

Infracost estimates:

$281.12/month
Step 3

The development budget is:

$100/month
Step 4

OPA evaluates the generated policy.

$281.12 > $100
Step 5

Policy fails.

❌ FinOps Policy Violation
Step 6

GitHub Actions reports the result.

PR Comment
    +
Slack Alert
    +
CI Failure
Final Result
🚫 Expensive infrastructure
   does not silently reach production.
🏆 Project Highlights
<div align="center">
💰 Cost Governance
🧠 Policy as Code
🤖 Python Automation
🏗️ Terraform Modules
🧪 Automated Testing
🐳 Docker Reproducibility
⚙️ Ansible Configuration
🔄 GitHub Actions CI/CD
🔔 Slack Integration
☁️ Local AWS Testing
</div>
🔮 Future Extensions

The architecture can be extended toward:

🌎 Multi-cloud cost governance
📊 Historical cost trend analysis
🚨 Cost anomaly detection
👥 Team-level budgets
☸️ Kubernetes cost policies
🤖 Automated optimization recommendations
📈 FinOps dashboards
🔐 Policy approval workflows
🏢 Organization-level cloud governance
💡 Core Philosophy
Cloud infrastructure should be secure, reliable, scalable, and financially responsible.

Most infrastructure pipelines already enforce:

Security
Reliability
Testing
Deployment Quality

This project adds:

💰 Financial Responsibility

as an automated engineering constraint.

<div align="center">
🚦 Build Infrastructure.
💰 Measure Its Cost.
🧠 Enforce Policy.
🚀 Deploy Responsibly.
