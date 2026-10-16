# Owner billing screenshot evidence — 2026-10-16

Three owner-provided screenshots were read locally; initial attachment-path errors resolved. No account navigation or billing changes. Raw images,account email and billing identifiers not copied into repository.

AssemblyAI screenshot140038: Plan Details Free; free credits remaining$48.27; credits spent$1.73. This verifies displayed account free plan/grant, not deployed API key mapping or auto-pay state (not visible). Spent credits are grant consumption, not proof of card charges.

Gemini Rate Limit screenshot140147: project VoiceBridge,Free tier,28 Days,explicitly peak usage per model over last28days. Displayed limits:
Gemini3.7Flash RPM5,TPM250000,RPD20; peaks3RPM,319.45KTPM,7RPD.
Gemini3.8Flash RPM5,TPM250000,RPD20; peaks1RPM,67TPM,4RPD.
3.7peak exceeds TPM; banner says reached a rate limit. This is historical28day peak evidence,not proof currently exhausted or cause of3.8provider503.3.8row is below displayed limits.
Gemini Billing screenshot140121 selects a different project My First Project; Free shown and billing account inactive/unsupported. Do not attribute its account status to VoiceBridge or treat inactive billing as established cause of503.
Deployed key-to-VoiceBridge mapping remains unverified; no keys requested or exposed.

Implications: actual model quota5RPM/250KTPM/20RPD is stricter than shared internal admission maximum60RPM/1sec. Patchc9f5ee7 fixes route coverage only; it does not claim these provider quotas enforced. Need configurable Gemini-specific limits and token/daily request accounting. A single long video request may exceed250KTPM even at1concurrent; splitting/clipping requires distinct design and does not guarantee meeting provider token estimation. Do not evade quotas via keys/projects or automatically upgrade.
Free balance is finite. No new provider starts,deploys,paid plans,cookies or social sessions introduced.
Status: account-screen evidence PARTIAL (Free plans/grant shown); precise deployed-key linkage and AssemblyAI auto-pay not independently verified; Gemini3.8503 root cause OPEN.
