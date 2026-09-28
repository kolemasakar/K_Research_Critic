FROM python:3.13-slim

WORKDIR /app
COPY plugins/krc_migration_candidate/mcp_canary /app/mcp_canary

ENV PYTHONUNBUFFERED=1 \
    KRC_MCP_BIND_HOST=0.0.0.0 \
    KRC_MCP_PORT=8000 \
    KRC_MCP_AUTH_MODE=none

EXPOSE 8000

CMD ["python", "-m", "mcp_canary.http_server"]
