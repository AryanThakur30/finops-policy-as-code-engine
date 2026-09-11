FROM openpolicyagent/opa:latest

WORKDIR /project/policies

COPY policies/generated/cost.rego ./cost.rego
COPY policies/cost_test.rego ./cost_test.rego

CMD ["test", ".", "-v"]
