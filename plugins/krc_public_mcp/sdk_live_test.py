import asyncio, json, time, os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

URL = os.environ.get("KRC_TEST_URL", "http://127.0.0.1:19013/mcp")

async def one(i):
    async with streamablehttp_client(URL) as (read, write, _):
        async with ClientSession(read, write) as s:
            init = await s.initialize()
            names = [t.name for t in (await s.list_tools()).tools]
            assert "guest_session" in names
            assert "research_submit" in names
            g = await s.call_tool("guest_session", {})
            raw = g.structuredContent if getattr(g, "structuredContent", None) else json.loads(g.content[0].text)
            token = raw["guest_token"]
            submit = await s.call_tool("research_submit", {
                "guest_token": token, "tool": "claim_evidence_audit",
                "payload": {"evidence_origins": ["a", "a", "b"], "required": 2}
            })
            obj = submit.structuredContent if getattr(submit, "structuredContent", None) else json.loads(submit.content[0].text)
            jid = obj["job_id"]
            for _ in range(100):
                st = await s.call_tool("research_status", {"guest_token": token, "job_id": jid,
                                                          "acknowledge_delivery": True})
                obj = st.structuredContent if getattr(st, "structuredContent", None) else json.loads(st.content[0].text)
                if obj["status"] in ("done", "failed"):
                    assert obj["status"] == "done", obj
                    assert obj["result"]["achieved_independent"] == 2, obj
                    return names
                await asyncio.sleep(0.02)
            raise AssertionError("timeout")

async def main():
    for n in (1, 3, 10):
        t = time.monotonic()
        results = await asyncio.gather(*(one(i) for i in range(n)))
        print(f"OFFICIAL_SDK_CONCURRENT={n} PASS={len(results)}/{n} SEC={time.monotonic()-t:.3f} TOOLS={len(results[0])}")
asyncio.run(main())