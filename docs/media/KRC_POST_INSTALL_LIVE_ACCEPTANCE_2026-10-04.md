# Post-installation live MEDIA acceptance — 2026-10-04

User explicitly requested live checks after installation. Existing Gemini Free data-use and free STT consent reused; FREE_ONLY preserved. One fresh start per tested platform; no automated provider replay.

## YouTube

- URL: https://www.youtube.com/watch?v=jNQXAC9IVRw
- PreflightPASS:9d0089c4-2271-472e-9ee1-14f5b7a1a255; lookup404 before fresh start.
- Job:KRCM_19370440-037a-441f-a580-801173dcb635.
- Start request:8c787205-7714-4eed-99d1-a295f22d624c.
- Created17:09:45.064Z, FAILED17:09:50.417Z.
- Error:GEMINI_YOUTUBE_FAILED, providerHTTP503, providercode=service_unavailable,retryabletrue. provider_error_reason/statusnull.
- Independent R3C status request:f57c314f-eec1-44d1-80cc-afa5a9a09c58 confirmed same state.
- Modelgemini-3.7-flash,consentacktrue;0segments,0chars,0STTseconds,0credits,chargeuncertainfalse.
- Safe provider metadata is observable. This503 does not prove that earlier400 has been repaired. No retry after503.

## Instagram

- URL:https://www.instagram.com/reel/Dcea3BiPTBm/
- PreflightPASS:2b61b936-ba0e-4047-b77b-9b2324df0ef8;lookup404beforetest.
- Bounded E2 activation deploy:dep-db18gqvavr4c73ap38ug,commit138a77c6554b792d49a90438d043089d7d42f670.

- Activation verifiedlive,HTTP200/statusok/probeonlyfalse.
- Exactly one tool start returnedvoicebridge_http_error HTTP429,retryabletrue,nojobID. No replay.
- E2 app logs shownewinstanceptzhl starting17:38:58Z,oauth/token20017:39:03Z,POST/mcp20017:39:49Z. The HTTP200 is MCP transport status; structured execution result is429.
- Immediate R3C lookupalso429; after canonical VoiceBridgehealthHTTP200 request2add522c-9be9-4eec-b4ec-6be6bf985079 at17:40:44.309Z,lookup404.
- No accessible Instagram job or established consumption. Do not infer zero consumption from missingjobID.
- VoiceBridge app log:stoppingSIGTERM17:25:00.194Z,startednewinstanceqngkn17:40:39.351Z. This shows a sleep/restart during the confirmation interval; causal location of429 remains unproven.
- Source inspection:the E2 HTTP adapter has a pre-existing health-only warmup loop with45s budget and5s perrequest, preceding the newlyinstalled readiness gate. It can returngenericvoicebridge_http_error429 without sending the consequential POST. The current public error does not distinguish warmup from POST failure; a stage diagnostic is needed to establish the exact failure location.
- E2 restoredprobeonlytrue bydeploydep-db18usqd0e5s73eln5kg,commit138a77c6554b792d49a90438d043089d7d42f670,live17:40:43.964Z. Final E2healthHTTP200/statusok/probeonlytrue.
- E3/E4 notactivatedorchanged during this acceptance.
 
## Outcome
 
Real successful transcript acceptance remains2/4:Facebook andTelegram previouslyPASS. YouTubethisattemptFAILEDprovider503service_unavailable;Instagramstart429withoutaccessiblejob. No successclaim for either; no paid fallback or automaticretry.
