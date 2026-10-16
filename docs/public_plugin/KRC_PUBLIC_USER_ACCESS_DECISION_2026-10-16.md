# KRC Public — approved user-access model (2026-10-16)

Decision: user connects K-Research & Critic once inside ChatGPT and subsequently works exclusively in ChatGPT. No separate KRC registration, login, passwords, local program installation, dashboard, or manual MCP interaction. Responses and FIFO queue status should surface inside the ChatGPT conversation.

Security caveat: installing/connecting the plugin does NOT inherently provide the remote MCP server with a validated ChatGPT user identity. Do not claim the platform guarantees identity forwarding. Implement invisible per-job access isolation with short-lived opaque capabilities or a compatible platform authentication method, without user-visible additional login. Validate cross-user isolation and client support before publication.

State: OWNER_APPROVED DESIGN, not a statement that the user-facing workflow is already deployed or technically validated.
