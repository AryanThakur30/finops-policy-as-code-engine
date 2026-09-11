FROM openpolicyagent/opa:latest

WORKDIR /project

COPY docker/opa-tests /project/policies

CMD ["test", "/project/policies", "-v"]
