FROM openpolicyagent/opa:1.20.2@sha256:7b15f9d96345dfa639322ad97f65a0b38260f95efcdd7f5c24e284228708f06c

WORKDIR /project

COPY policies/generated/cost.rego /project/policies/generated/cost.rego
COPY policies/cost_test.rego /project/policies/cost_test.rego

ENTRYPOINT ["opa"]
