FROM openpolicyagent/opa:latest

WORKDIR /project

COPY policies/generated/cost.rego /project/policies/cost.rego
COPY policies/cost_test.rego /project/policies/cost_test.rego

CMD ["test", "/project/policies", "-v"]
