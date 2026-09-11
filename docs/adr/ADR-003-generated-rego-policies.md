# ADR-003: Generate Rego Policies from Configuration

## Status

Accepted

## Context

The project supports multiple environments and multiple policy dimensions.

Maintaining every environment and threshold as separate handwritten Rego rules would create duplication and increase the risk of inconsistent policy behavior.

The project also needs a clear distinction between human-authored configuration and executable policy artifacts.

## Decision

Generate Rego policies from the YAML configuration using Python and Jinja2.

The YAML file is the human-facing source of policy configuration. Python validates and orchestrates generation, while Jinja2 provides the Rego template structure.

Generated Rego is committed to the repository so CI and reviewers can inspect the exact policy artifact being evaluated.

## Alternatives Considered

### Handwritten Rego only

This is simple for a small policy set, but becomes repetitive as environments, resources, and thresholds increase.

### Dynamic policy construction at runtime

Generating policy only during execution would reduce repository visibility and make debugging and review harder.

### Custom Python policy engine

A Python-only evaluator would couple policy semantics to application code and remove the benefits of a dedicated policy engine.

## Consequences

### Positive

- Less duplicated policy code
- Configuration-driven scaling
- Clear source-of-truth model
- Generated policy is reviewable in Git
- Rego remains the execution layer
- Jinja2 makes policy structure explicit and maintainable

### Negative

- Generation becomes part of the build pipeline
- Template and configuration changes must be tested together
- Contributors should not manually edit generated policy files
