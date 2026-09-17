# Agent Fabric — the `fab` toolchain as a container.
# Pure Python standard library: no pip install, no services, no GPU.
FROM python:3.11-slim

LABEL org.opencontainers.image.title="Agent Fabric"
LABEL org.opencontainers.image.description="The kernel-native, real-time, structured metabase for enterprise autonomous agents — the fab toolchain."
LABEL org.opencontainers.image.source="https://github.com/AGenNextHub/Agent-Fabric"
LABEL org.opencontainers.image.documentation="https://github.com/AGenNextHub/Agent-Fabric/tree/main/book"

WORKDIR /app

# The toolchain is stdlib-only, so we just copy the sources.
COPY tools/ ./tools/
COPY schema/ ./schema/
COPY spec/ ./spec/
COPY examples/ ./examples/
COPY sdk/ ./sdk/
COPY tests/ ./tests/

# Run as an unprivileged user.
RUN useradd --create-home --uid 10001 fabric && chown -R fabric:fabric /app
USER fabric

# Fail the build if the conformance suite regresses (32/32).
RUN python tools/fab.py test

# `docker run <image> <subcommand> …` maps straight onto the fab CLI.
ENTRYPOINT ["python", "tools/fab.py"]
CMD ["--help"]
