# ADR-002: Use YAML as the Policy Configuration Surface

## Status

Accepted

## Context

FinOps policies contain values that should be configurable without requiring contributors to manually edit Rego source.

Examples include:

- Environment budget thresholds
- Resource-level cost limits
- Cost increase thresholds
- Feature enablement

The configuration surface should be readable by engineers who understand infrastructure and FinOps but do not necessarily write Rego.

## Decision

Use YAML as the human-facing policy configuration format.

A single YAML configuration describes budgets, resource limits, and cost-increase guardrails. The Python policy generator consumes this configuration and produces executable Rego.

## Alternatives Considered

### JSON

JSON is machine-friendly but more verbose and less readable for configuration maintained by humans.

### TOML

TOML is readable, but YAML has broader adoption across infrastructure, DevOps, CI/CD, Kubernetes, and configuration tooling.

### Direct Rego configuration

Putting thresholds directly into Rego would make the policy layer less accessible and require policy-language knowledge for routine configuration changes.

## Consequences

### Positive

- Human-readable configuration
- Easy environment and threshold changes
- Clear separation between configuration and policy implementation
- Works naturally with Git-based review
- Familiar format for infrastructure engineers

### Negative

- YAML syntax can be sensitive to indentation
- Configuration validation must be implemented
- Generated Rego must be treated as a build artifact rather than the primary configuration interface
