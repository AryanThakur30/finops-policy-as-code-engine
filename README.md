# FinOps Policy as Code Engine

> Prevent over-budget infrastructure changes before they reach production.

A policy-driven FinOps pipeline that automatically estimates infrastructure cost, evaluates it against a defined cost guardrail, and enforces the result directly inside GitHub Pull Requests.

**Terraform → Infracost → OPA/Rego → GitHub Actions → Pull Request Enforcement**

---

## What This Project Does

Cloud infrastructure changes can introduce unexpected costs when cost is reviewed only after deployment.

This project moves cost governance into the development workflow.

Whenever infrastructure changes are submitted through a Pull Request, the pipeline:

1. Generates an Infracost estimate.
2. Evaluates the estimated monthly cost against an OPA/Rego policy.
3. Applies a configurable cost guardrail.
4. Posts the result directly to the Pull Request.
5. Fails the CI check when the infrastructure violates the policy.

This makes infrastructure cost a policy-controlled engineering concern rather than a post-deployment surprise.

---

## Architecture

```mermaid
flowchart TD
    A[Terraform Infrastructure] --> B[Infracost]
    B --> C[Monthly Cost Estimate]
    C --> D[OPA + Rego Policy]
    D --> E[GitHub Actions]
    E --> F{Cost Policy Check}
    F -->|PASS| G[CI Pass]
    F -->|FAIL| H[CI Failure]
    H --> I[Infracost PR Comment]
    J[Cost Guardrail: $100/month] --> D
