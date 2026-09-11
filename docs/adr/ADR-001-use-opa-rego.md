# ADR-001: Use OPA/Rego for Policy Evaluation

## Status

Accepted

## Context

The FinOps Policy as Code Engine needs a deterministic policy evaluation layer that can run locally, inside CI, and independently of a specific cloud provider.

The policy engine must support multiple independent guardrails, structured violation messages, automated tests, and reproducible execution.

## Decision

Use Open Policy Agent (OPA) with Rego as the policy evaluation engine.

Rego policies evaluate normalized infrastructure-cost data produced by the FinOps pipeline. OPA runs as a standalone container so policy evaluation is reproducible across developer machines and CI environments.

## Alternatives Considered

### HashiCorp Sentinel

Sentinel provides strong policy-as-code capabilities, but it is tightly associated with the HashiCorp ecosystem and is less suitable for this project's provider-neutral standalone policy engine.

### Custom Python checks

Python could implement the checks directly, but policy logic would become coupled to application code. It would also make policy evaluation less declarative and harder to separate from orchestration.

### Celery-style task checks

A task queue is useful for asynchronous workloads, but it is not a policy language or policy evaluation engine. It would add operational complexity without solving the policy expression problem.

## Consequences

### Positive

- Declarative policy definitions
- Provider-neutral evaluation
- Native structured policy results
- Excellent local and CI reproducibility
- Straightforward automated policy testing
- Clear separation between policy logic and orchestration

### Negative

- Rego introduces a separate language for contributors to learn
- Generated policies must remain compatible with the selected OPA version
- Policy input schemas need to be maintained carefully
