# Live acceptance progress: Facebook and Telegram PASS — 2026-10-04

Status: 2/4 LIVE DIRECTIONS PASS (Facebook, Telegram); YouTube and Instagram unresolved.
Supersedes the earlier all-failed bounded attempt, without rewriting historical evidence. Owner instructed continuation; confirmed Render workspace remains tea-d9dsqdjrjlhs73ba1ga0. Gemini Free/STT consent remains valid.

## Narrow deployed VoiceBridge repair
Production branch agent/krc-media-gemini-migration previously pointed at d3873bf13e60c4932ab08cae449c924051be4a37. Prepared isolated baseline worktree with ONLY managed_media_url.ts fix, 3 Facebook regression tests and rollout document; research peer diagnostics/wrapper injection excluded.

Full exact release npm run check: TypeScript build PASS,273/273 tests PASS,0 failures,95.061s. Published release commit0b6dca4e4cd4fd5670fe2ed8afa2f9e6917bcc0d. Fast-forwarded existing deployment branch, autoDeploy remainedOFF, triggered ONE existing free service deploy dep-db16riqd0e5s73ecvaig. Render confirmed exact release SHA and live at15:16:57Z; canonical health200 request3983d776-58e0-405e-9cb4-545c18976f67. No main merge, instrumentation enablement, secrets, new infrastructure or paid fallback.

## Telegram real PASS
Public input https://t.me/dw_ukraina/27146.
Before STT, fetched exact Telegram embed and its asset. MP4 structural inspection:6,457,614 bytes,duration58.901333s,video and audio track handlers present. Caption describes an interview with an instructor; input chosen as short speech-bearing public video. No provider work in this selection probe. Temporary media was not archived. Host ffprobe was unavailable, so structural inspection used the MP4 moov/mvhd/trak/mdia/hdlr boxes.

E4 activation dep-db16r3u0tbcc739qctlg at KRC4402392bd7072ad3bad8e68e8695dda176f0f3ab, verifiedlive/probe-only=false. ONE new source start:
- job KRCM_afe3cfb7-cbec-44b2-a17a-ce2d76bd3e94
- start request26f02eaf-6008-4470-9130-e17b7dd8775b
- COMPLETED,languageuk,providerassemblyai,retrievaltelegram_public_web
- STT seconds58,credits0,charge_uncertain=false,provider_data_deleted=true
-1segment,677UTF-16characters;created15:17:42Z,completed15:17:50Z.
Read all segments with limit1,cursor0,next_cursor=null; index0; actual text length677 exactly matches status. Repeated status and segment reads preserve identity/text. The first attempt to use segment limit100 yielded MCP Invalid params; corrected to supportedlimit1, no provider replay. E4 restored via dep-db16sck9v7es73e7t99g,live; health200/probe-only=true.

## Facebook real PASS after URL repair
Original descriptive NASA URL now correctly canonicalizes to https://www.facebook.com/NASASCaN/videos/8368792419872400/.
E3 activation dep-db16stvavr4c73ai9amg,health confirmedfalse. ONE fresh start after the deployed repair:
- job KRCM_27482717-917a-454a-a69d-c2a55821a86c
- start requestba02ca14-afaa-4687-be85-4349bf65065a
- COMPLETED,languageen_us,free Cobalt+AssemblyAI
- media duration167.275938s,STT seconds168,credits0,charge_uncertain=false,provider_data_deleted=true
-3segments,2630UTF-16characters;created15:32:19Z,completed15:32:36Z.
Read EVERY page withlimit1:cursor0->1->2->null,indexes0/1/2. Joining text with the implementation's newline separators gives2630,exactstatus match. Re-read same3segments withlimit3,next_cursor=null,identicaltext. E3 restored via dep-db173bgu01pc73d4vs3g,live;healthtrue.

## Actual process restart read continuity
VoiceBridge app logs identify instance5mkb8 stopping(SIGTERM)15:49:57.159Z and NEW instancerlptm starting15:52:57.697Z.
AFTER this actual process restart, R3C status and ALL segment reads still returned the same completed Facebook and Telegram jobs/text/counts:
- Telegram segment request2f1775ac-f195-403c-9930-2be59a97bee3:1/677,next_cursornull,identicalsegments.
- Facebook segment request5d24ae67-1f9f-4d46-8e7b-aa1d2089d587:3/2630,next_cursornull,identicalsegments.
This is actual process restart/read persistence for these jobs, beyond the earlier in-memory HTTP-wrapper tests. It does not prove DB failover or unlimited retention; declared TTL remains3600s.

## YouTube concrete failure
After healthy capabilities and preflightPASS,lookup404/no reusable job,ONE fresh owner-continuation start on jNQXAC9IVRw created:
KRCM_551dd8fc-f2af-4400-927a-a472b1a11927,requestaed4d352-5fd5-46e1-82d0-7c1782e0f583.
FAILED,GEMINI_YOUTUBE_FAILED,retryablefalse,provider_http_status400,provider_error_code/statusnull,modelgemini-3.7-flash,consent acknowledged,0segments/characters/STTseconds. Independent status requestd8b1e894-635e-4625-a09a-11eb561f6b45 confirms same terminal job.
This is a provider HTTP400, separate from previously observed VoiceBridge HTTP429. Exact400 reason remainsunknown because safe current metadata lacks detail. No subsequent retry.

Official Google documentation checked:
https://ai.google.dev/gemini-api/docs/video-understanding
https://ai.google.dev/api/interactions-api-v1
The current official REST YouTube example uses v1beta/interactions and a video URI without mime_type,matching the implementation's broad request structure. Documentation example model differs(current3.8); that difference is NOT proof our3.7 model caused400. No speculative model/API change made.

## Instagram latest attempt unresolved
Selected alternative short NASA reel https://www.instagram.com/reel/Dcea3BiPTBm/; public indexed description gives astronaut/Mission Control voice communication,~41seconds. PreflightPASS requestb4059863-b44d-4d52-8177-e5bc6f4116d3,lookup404.
E2 activation dep-db17487avr4c73aj83mg live,healthfalse. ONE start returned VoiceBridgeHTTP429,retryabletrue,nojobID. No repeatstart. Canonical health subsequently200 request70f63c49-29e7-4cb2-82c2-99794e5e18ac;lookup404 again. No accessible job/state or consumption established.
E2 restored dep-db17cltg1s2s738ti8ng,live. Latest E2 health confirmedstatusok/probe-only=true;restoredeploy reachedlive. A combined sweep initially timed out on E3; a separate bounded read-only recheck subsequently confirmed BOTH E3 and E4 HTTP200/statusok/probe-only=true. All three routes are restored and verified.
VoiceBridge stop preceded this latest429 and warmup/read404. Temporal correlation is recorded, not proof of cold-start cause. Need diagnostics/readiness inside execution timing; do NOT change identity/rate limiter based on inference.

Earlier Instagram C_bnaTAO2Ll normalization failure remains a separate failed-input result. Restricted host /opt/krc-cobalt listing returned permissiondenied; sudo status helper returned Command not allowed from RDC. No privilege expansion or bypass attempted.

## Billing, artifacts and remaining work
Known successful free STT consumption:58+168=226seconds (~3m46s). All recorded credit charges0,paidfallbackfalse. Zero monetary billing is not inferred solely from STT counter; configuration is FREE_ONLY and paid paths stayeddisabled.
Transcript text lives only in temporary active-chat tool state; permanent project docs retain metadata/evidence only. No full transcripts archived.

Remaining: establish GeminiHTTP400 cause through safe error diagnostics; diagnose/warm execution-time upstream readiness for Instagram429; then complete the two remaining directions with exact pagination/counts. Do not replay failed/uncertain jobs automatically, enable paid routes, or publishPlugin. Facebook and Telegram are verified livePASS; wholefour-directionintegration is NOT yetPASS.
