# All four MEDIA routes: real acceptance PASS — 2026-10-04

## Result

Each supported platform produced a real COMPLETED transcript in this integration session. This is one sample per platform, not a guarantee for every public URL or continuous availability. Earlier provider400/503 and infrastructure429 causes are not proven permanently resolved.

|Platform|Source|Job|Segments|UTF16 characters|STTseconds|
|---|---|---|---:|---:|---:|
|YouTube|https://www.youtube.com/watch?v=jNQXAC9IVRw|KRCM_fabae184-3b16-46c6-baca-c3df701dd61b|1|220|0|
|Instagram|https://www.instagram.com/reel/Dcea3BiPTBm/|KRCM_ac91b1b2-c29a-404e-9555-690aaeecad06|1|331|42|
|Facebook|https://www.facebook.com/NASASCaN/videos/8368792419872400/|KRCM_27482717-917a-454a-a69d-c2a55821a86c|3|2630|168|
|Telegram|https://t.me/dw_ukraina/27146|KRCM_afe3cfb7-cbec-44b2-a17a-ce2d76bd3e94|1|677|58|

EarlierFacebook/Telegram evidence, full-pagination verification and actual process restart durability are in KRC_LIVE_ACCEPTANCE_PROGRESS_2026-10-04.md. Their temporary jobs may expire; this table records the verified historical session result.

## New YouTube acceptance

One user-authorized fresh start after preflightPASS5e34f96e-0bc1-449d-9c03-01829a407780 and lookup of previous FAILED503job. No automated replay.
Created18:13:53.805Z,completed18:14:03.776Z. Modelgemini-3.7-flash, consentacktrue. Startrequestdc1aa5d2-fc2e-4bd8-86e4-634edea0f3db; independentstatusd7bc31fb-d98f-4b28-a16a-1f9b93dd39cd. Fullsegmentsrequest429e79a0-a785-4691-a745-1854ef60f6be:cursor0,nextnull,index0,220JSUTF16chars, exact servercount. Reread identical.0credits,chargeuncertainfalse; provider_data_deletednull(do not claim Google deletion).

## New Instagram acceptance

E2 stage-diagnosticcommit6a6a998012a807ca3b45ed52036b7b24b0ef4364 deployeddep-db199mvavr4c73as8ar0,live18:03:45.785Z,HTTP200/statusok/probeonlyfalse. PreflightPASS75842101-6ea4-4ad9-b01b-4b0132ee0873,lookup404. ONEstartcreated18:27:20.943Z,completed18:27:35.788Z. Startrequest37ce13bf-f094-40f3-a664-c072d13a0df3; independentstatusb68d0859-f4b2-4158-a707-db6c60523d34. Duration41.11675s,languageen,Cobalt+AssemblyAI,42STTseconds,0credits,chargeuncertainfalse,provider_data_deletedtrue.
Fullsegmentsrequestf6182313-16a1-4ca1-a59c-7c086bbc79a7:cursor0,nextnull,index0,start720ms,end34780ms,331JSUTF16chars matches servercount. Reread identical.

## Changes and limits

Narrow Facebook URL repair and safe Gemini diagnostics remain deployed on VoiceBridgec2ba34f292d0c2189bc9e994121011693488dc84. E2 now distinguishes warmup/readiness/start failures and POSTattempt status; existing timeoutbudget and singlePOST/no-replay behavior preserved. Tests:425KRC PASS/9fixture-skipped, finaltype-validation+crossrepo13PASS. Google official request/pricing checked; no model/API/requestshape change justified or made. Source: https://ai.google.dev/gemini-api/docs/video-understanding and https://ai.google.dev/gemini-api/docs/pricing.

Successful-session free STT accounting:58+168+42=268seconds(4m28s). This attempt added42seconds. YouTubeusesGeminiandtheSTTcounteris0; this does not imply no Gemini request was made. Paid fallback disabled, no new infrastructure/mainmerge/publication. Full transcripts are temporary active-chat data; only metadata is archived here.

## Restore

E2 restoredeploydep-db19l9qd0e5s73eok200 at exact6a6a998 commit. E3/E4 were not activated during this turn. Restorelive18:28:28.295Z. Final E2healthHTTP200/statusok/probeonlytrue; E3healthHTTP200/statusok/probeonlytrue. E4health requests timedouttwice at45s each; no E4env ordeploy changes made. Current E4frontend availability remainsunverified despite its prior successful transcript acceptance. Latest E4app logquery18:28Z onwardempty; insufficient to establish cause.

R3C finalcapabilities requeste0521ae4-3deb-46f4-acda-a06cec7cc2b6:configuredtrue,allfourplatforms,paidfallbackfalse,GeminiFreeonlytrue. NewYouTubeandInstagramlookup bothreusedsameCOMPLETEDjob (readonly, no new provider work).
