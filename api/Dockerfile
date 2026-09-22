# Agent Fabric API — the hosted wedge service (compile/validate/grade/migrate/
# query over HTTP, metered per call). Separate image from the root Dockerfile,
# which packages the `fab` CLI only and is not a long-running service.
FROM python:3.11-slim

LABEL org.opencontainers.image.title="Agent Fabric API"
LABEL org.opencontainers.image.description="Hosted HTTP API over the fab toolchain: compile, validate, grade, migrate, query — metered per API key."
LABEL org.opencontainers.image.source="https://github.com/AGenNextHub/Agent-Fabric"

WORKDIR /app

# Pure standard library — no pip install needed for the service itself.
COPY tools/ ./tools/
COPY schema/ ./schema/
COPY api/ ./api/

# Fail the build if the toolchain the API wraps regresses.
RUN python tools/fab.py test

# Where the SQLite key/usage store lives; mount a volume here in production
# so keys and usage survive container restarts.
ENV FABRIC_API_DB=/data/fabric_api.db
RUN mkdir -p /data

RUN useradd --create-home --uid 10001 fabric && chown -R fabric:fabric /app /data
USER fabric

EXPOSE 8080
ENTRYPOINT ["python", "api/server.py"]
CMD ["--host", "0.0.0.0", "--port", "8080"]
