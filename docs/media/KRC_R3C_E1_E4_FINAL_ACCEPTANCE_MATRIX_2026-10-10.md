# KRC MEDIA — матриця фінального приймання R3C / E1–E4
Дата: 2026-10-10. Статус: `NOT ACCEPTED`, попри успішні окремі інтеграційні тести.

## Гейти
| Gate | R3C Readonly | E1 YouTube | E2 Instagram | E3 Facebook | E4 Telegram |
|---|---|---|---|---|---|
| Підключення/auth/route | PASS | PASS | PASS | PASS | PASS (локальна інтеграція) |
| Safe capabilities / preflight | PASS (коли warm) | PASS | PASS | PASS (read/status) | PASS (локальна інтеграція) |
| Consequential start — один POST / consent | N/A | PASS (раніше) | PASS короткий | PASS 180 с | LIVE BLOCKED |
| Підтверджено LIVE COMPLETED | N/A | PASS (4 сегменти, duration null) | PASS 41 с | PASS 180 с | NOT VERIFIED |
| LIVE 480–720 с з голосом, мова+контент | N/A | NOT VERIFIED | OPEN | OPEN | BLOCKED |
| Сквозна пагінація/UTF-16 | PASS локально | PASS локально | PASS локально | PASS 3 LIVE сегменти | PASS локально |
| Актуальна cross-repo local HTTPS | PASS | PASS | PASS | PASS | PASS |
| Lost reply без дубля provider | PASS local | PASS local, live evidence | PASS local | PASS local, live evidence | PASS local |
| Безпека FREE_ONLY/paid fallback 0 | PASS | PASS | PASS | PASS | PASS local; LIVE blocked |
| Холодний Render → VoiceBridge | **FAIL** (HTTP 429) | DEPENDENCY FAIL | DEPENDENCY FAIL | DEPENDENCY FAIL | DEPENDENCY FAIL |
| Live durable job after restart | PARTIAL (старий FAILED) | PARTIAL | OPEN | OPEN | OPEN |
| Фінальний вердикт | **OPEN** | **PARTIAL** | **PARTIAL** | **PARTIAL** | **BLOCKED** |

## 17 opt-in пропусків — закриття тестового пропуску
- Звичайний базовий набір: 482 PASSED, 17 SKIPPED. Всі пропуски з `tests/test_media_all_routes_voicebridge_integration.py`: 4 basic cross-route, 3 fail-closed scope, 1 limiter, 1 diagnostic 429, 4 long multilingual (480–720 s, 57 сегментів), 4 lost-reply recovery.
- Перший opt-in прогін на старому fixture VoiceBridge checkout `f416d8c`: 15 PASS, 2 FAIL (Facebook/Telegram lost reply); у старому коді відсутній `lookupFreeRoute`.
- Прямий прогін на повністю актуальному VoiceBridge branch `5293e4e`: 4 PASS, 13 FAIL. Цей fixture не сумісний без адаптації з поточними production config/engines; не трактувати як production regressions.
- Контрольований ізольований overlay старого fixture `f416d8c` + **два** production source файли `managed_media_http.ts` і `managed_media_service.ts` із актуальної гілки VoiceBridge `5293e4e`. TypeScript build PASS. Результат opt-in local HTTPS: **17 PASS, 0 FAIL, 0 SKIP** (35.31 s). Реальні зовнішні медіа та провайдери не викликалися, пам’ять замість Postgres. Production не змінювався.
- **Критерій offline opt-in — PASS з fixture overlay**. Для відтворюваності потрібен окремий чистий commit fixture compatibility, а не незафіксований оверлей; до того інтеграційний gate має позначку `PASS_ISOLATED_FIXTURE`.

## Незакриті вимоги та stop conditions
1. **P0:** контрольований холодний HTTP 429 після паузи, запланованої власником з 2026-10-11 10:00 Europe/Kyiv; зафіксувати allowlisted edge headers + Render/MCP correlation. Якщо origin не доведений, не змінювати політики rate/concurrency наосліп.
2. **P1:** перевірені public audiovisual 480–720 с Instagram та Facebook, COMPLETED і звірка трьох audio checkpoints, cost 0.
3. **P1:** Telegram live block; не обходити правила безпеки; зберігати BLOCKED.
4. **P1:** перевірка справжньої durable database consistency після контрольованого restart/redeploy, не підмінювати memory fixture.
5. **P2:** окремий committed fixture compatibility, повний локальний прогін + перевірка, що сервісні політики, FREE_ONLY і маршрути залишились незмінними.
6. **P2:** підсумковий owner acceptance тільки після всіх обов’язкових gates. Немає підстав позначати весь проєкт `DONE`.

## Операційні обмеження
- Не звертатися до Render/VoiceBridge після початку паузи до запланованого холодного read-only тесту; не використовувати keepalive.
- Не робити автоматичних повторних consequential POST після 429/503/втрати відповіді.
- Не комітити секрети, транскрипти користувачів, сирі response headers; не активувати платні маршрути.


## Addendum 2026-10-13 — owner-authorized short reels scope and current status
This historical 2026-10-10 matrix is preserved as the state **at that date**. The owner on 2026-10-13 explicitly cancelled Instagram/Facebook 480–720s acceptance. The 480–720s gate in the table above is **SUPERSEDED FOR E2 AND E3** and must not be treated as an outstanding release blocker. The original historic row is not an obligation to search for long social videos. Current authority: `docs/media/KRC_P1_OWNER_SHORT_REELS_SCOPE_DECISION_2026-10-13.md`.

- **R3C P0:** three independent cold auto-wake cycles passed after fixing relay token. A later concurrent read-only capabilities check (R3C + E1) passed after a bounded concurrent relay fix, with direct positive krc-cobalt journald evidence. These newer tests supersede the historical **cold Render FAIL** row for the demonstrated cases only; concurrency join branch was exercised offline, but not separately demonstrated by two simultaneously received relay POSTs in production. See `docs/media/KRC_P0_COLD_AUTO_WAKE_3_OF_3_PASS_2026-10-13.md` and `docs/media/KRC_P1_CONCURRENT_RELAY_RUNTIME_PATCH_AND_MEDIA_ADMISSION_2026-10-13.md`.
- **E2 Instagram:** historical short live COMPLETED 41.11675s, one segment, 331 chars, credits reported zero. **SHORT-LIVE PARTIAL**, with remaining independent transcript/audio 3-point accuracy, current retrieval/readback, and restart durability gates. E2 `Invalid params` from attempted long IGTV `/tv/B3It-ECHZrA/` is now **DIAGNOSED_NOT_A_SHORT_REEL_REGRESSION**: `plugins/krc_migration_candidate/mcp_canary/r3e2.py`, lines 148–159, intentionally allow only `/reel/` and `/p/`, not `/tv/`. The action thus returned MCP -32602 before `backend_call`; no need to extend the route for out-of-scope long IGTV.
- **E3 Facebook:** historical 180.302938s COMPLETED, 3 segments, 2984 chars, zero credits reported. **SHORT/MEDIUM-LIVE PARTIAL** pending explicit current audio accuracy and persistence gates; no new short Facebook job required without a specific evidence gap.
- **E1 YouTube:** long-form comparator remains an independent track, with Gemini Free disclosure; prior attempted start returned `voicebridge_not_ready` with `consequential_post_attempted=false`; do not convert to media completion.
- **E4 Telegram:** live BLOCKED, unchanged.
- **Overall R4 MEDIA:** HOLD / NOT ACCEPTED. Read-only historical traces are not a substitute for complete current persistence, status/segments and safety acceptance.
