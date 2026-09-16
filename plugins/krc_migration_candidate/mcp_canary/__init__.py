"""Repository-only KRC MEDIA MCP canary.

This package is intentionally transport-neutral and not deployed. It exposes a
small deterministic MCP protocol core for later bounded remote-MCP validation.
"""

from .server import (
    CANARY_TOOL_NAME,
    MCP_PROTOCOL_VERSION,
    canary_result,
    dispatch_mcp,
    tool_descriptor,
)

__all__ = [
    "CANARY_TOOL_NAME",
    "MCP_PROTOCOL_VERSION",
    "canary_result",
    "dispatch_mcp",
    "tool_descriptor",
]
