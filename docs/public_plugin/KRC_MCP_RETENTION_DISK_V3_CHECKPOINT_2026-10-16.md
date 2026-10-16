# KRC MCP retention and disk guard — v3 checkpoint

Status: OFFLINE PROTOTYPE / NOT DEPLOYED.

Implemented on local inherited code snapshot:
- 10-hour undelivered result expiry from completion instead of 24h.
- 10-hour delivered result expiry from acknowledgement.
- Upload timeout reduced from 24h to 10h; queued/running documents excluded from cleanup.
- Filesystem statvfs admission guard: projected available space after append/job record must remain at least 10% of filesystem capacity.
- Additional tests: undelivered expiry, completed-unclaimed document expiry, denial below disk reserve.

Validation: Python unittest discover 19/19 PASS. One regression was detected during development and corrected. Local archive: `KRC_PUBLIC_MCP_RETENTION_DISK_V3_2026-10-16.zip` (conversation download; **source is not yet committed into GitHub**).

Important unresolved deployment gates: no OCI co-load test, no proof of full MCP Streamable HTTP compatibility, no complete abuse protection, SQLite connection ResourceWarning, no bound against unrelated services consuming disk concurrently, and no systemd/Caddy production configuration. Do NOT expose publicly. KRC Cobalt production unchanged.
