# Передача KRC / VoiceBridge у новий чат — 2026-10-10

## Команда власника та точка зупинки
О 2026-10-10T13:48:57+03:00 власник наказав зафіксувати проєкт і документацію, перейти в новий чат, а потім виконати лише:
1. Уточнити джерело 429 на межі Render.
2. Провести довші живі перевірки Instagram, Facebook і Telegram.

У цьому чаті нових provider jobs після цієї команди не запускати. Продовження аудиту NASA не входить до наступного погодженого переліку. Генератор переходу власник у цій команді не надавав; це самостійний технічний checkpoint.

## Авторитетні репозиторії
| Проєкт | Репозиторій | Робоча гілка | HEAD перед цим checkpoint |
|---|---|---|---|
| KRC | https://github.com/kolemasakar/K_Research_Critic | agent/krc-public-media-r3-integration | 7e4eaf687efa80987313b994b02cc2b1a6b4f71f |
| VoiceBridge | https://github.com/kolemasakar/VoiceBridge | agent/krc-media-gemini-migration | 92fdc7d6b02656f2a6f4ea237af7745e9e068d51 |

Результуючі commit SHA цього checkpoint взяти з GitHub branch heads після читання файлу. Не вважати попередні SHA найновішими без перевірки. Main не змінювати, не зливати гілки, не публікувати приватний плагін.

Повні поточні протоколи:
- KRC: docs/media/KRC_COLD_START_AND_LONG_MEDIA_CHECK_2026-10-10.md
- VoiceBridge: docs/KRC_FREE_ROUTE_LOOKUP_RECOVERY_2026-10-10.md

## Реалізовані можливості
- Перевірка readiness VoiceBridge: до 45 секунд / 24 health GET; окремий GET до 5 секунд; готовність лише HTTP 200 і JSON status=ok.
- Одна повторна спроба оголошеного читання після тимчасової помилки й підтвердженої готовності. Явні API rate limits та Retry-After не повторюються.
- Readiness перед усіма чотирма start routes; якщо сервіс не готовий, consequential POST не надсилається.
- Після втрати транспортної відповіді на вже надісланий start виконується лише lookup. PROCESSING/COMPLETED відновлює відповідь, без повторного POST.
- Scoped Facebook/Telegram lookup використовує правильну free-route identity: normalized URL, language hint, owner digest. Читання лише наявного retry chain до 16 записів; без резервування, reconciliation або provider work.
- Safe diagnostics: stage, факт спроби POST, readiness counters, формат json/html; без raw secrets.

## Перевірки та межі
- KRC: 496/496 PASS, без пропусків, 83.59 с. Серед них 17 справжніх локальних HTTPS integration scenarios із production handlers/engines та fake providers.
- VoiceBridge: 276/276 PASS, build PASS, 86.968 с.
- Локальні довгі сценарії: 8–12 хвилин, en/ru/uk, 57 сегментів, 9 сторінок по 7; UTF-16, порядок і завершення pagination перевірені.
- Чотири локальні lost-start-response scenarios: рівно один provider call на кожен route.
- Fake provider + memory store не підтверджують живу STT-точність або DB failover.
- Історичні короткі живі тести 4 жовтня: 4/4 COMPLETED; 268 секунд STT (4 хв 28 с), free allowance. Не видавати їх за довгі живі перевірки.
- Instagram NASA Dcea3BiPTBm: 41 с, 1 сегмент, 331 символ; Facebook NASA video 8368792419872400: 167 с, 3 сегменти, 2630 символів; Telegram dw_ukraina/27146: 58 с, 1 сегмент, 677 символів. Це попередні кейси, не готові довгі кандидати.
- Результати MEDIA тимчасові; відомий TTL=3600 с. 404 сам по собі не доводить TTL expiry. Повні транскрипції в репозиторії не архівовані.

## Живий YouTube NASA — завершено
URL: https://www.youtube.com/watch?v=_T8cn2J13-4
Назва: NASA How We Are Going to the Moon. Офіційна сторінка: https://science.nasa.gov/resource/how-we-are-going-to-the-moon/

Перша спроба:
- KRCM_e71f7ede-6598-4718-b5fb-a26b6dcdf6df, 08:28:22.143Z → FAILED 08:31:49.714Z.
- GEMINI_YOUTUBE_FAILED, provider_http_status=503, provider_error_code=service_unavailable, retryable=true, без транскрипції.
- Діагностика збереглася після реального перезапуску VoiceBridge.

Повтор після окремої явної згоди власника 2026-10-10T10:18:09Z:
- KRCM_a95042aa-7952-40f2-ba5c-30801d2702b7.
- Створено 10:20:48.516Z, COMPLETED 10:21:17.968Z.
- Start request_id=80d9ddfc-c8e8-41b9-aa5b-3e451685490e, start_response_recovered=true, reused=true. Живе підтвердження відновлення через lookup без повторного start.
- Segments request_id=508dfd16-cd75-4713-ac46-c01bf0d83cb4: 4 сегменти, індекси 0–3, next_cursor=null; точна сума UTF-16 text=5186. Chunks склеюються без додаткових розділювачів.
- Таймкоди, confidence та media_duration_seconds=null. Повнота payload перевірена; аудіоточність не перевірена. Не вигадувати тривалість чи таймкоди.
- credits_charged=0, stt_seconds_charged=0, credit_charge_uncertain=false; Gemini tokens не виміряні; provider_data_deleted=null.
- limit=100 для segments спричинив Invalid params; limit=10 спрацював.
- Отриманий повний текст надано тимчасовим вкладенням у попередньому чаті; доступність цього вкладення в новому чаті не гарантована.

## Core research pilot — окремий стан
CriticProfile KRC_ARTEMIS_MEDIA_PILOT_20261010/v1:
- Затверджено власником 2026-10-10T08:57:42Z.
- Домен: космічна наука та інженерія; тема: плани Artemis у відео NASA та актуальність на 10.10.2026.
- MEDIUM, 1 незалежне підтвердження; primary source + independent evidence; поріг 0.8; українська; FREE_ONLY.
- Одна редакція; експертна оцінка 0.78; COMPLETED_WITH_LIMITATIONS.
- Перевірено 3 ключові твердження, не всі деталі відео. Водопостачання Orion: 1/1 PASS (NASA engineering + ESA власний операційний звіт). Gateway-центрична схема та EUS застаріли як поточний план, але 0/1 SHORTFALL щодо незалежного походження доказів; GAO перевіряє документацію NASA, не створює незалежний факт плану.
- Повний аудит NASA не продовжувати без окремого доручення.

## Невирішений холодний 429 — пріоритет
- Readonly capabilities/lookup/preflight іноді повертають voicebridge_http_error, http_status=429, retryable=true, readonly_health_ready=false.
- 10:15–10:16 UTC: readiness attempts 22 та 23, обидві операції не відновили VoiceBridge.
- Readonly app log POST /mcp HTTP 200: 10:16:01.840231801Z та 10:16:47.175464397Z. 429 був у tool result про upstream, а не HTTP transport самого MCP.
- Зовнішній GET із krc-cobalt відновив доступність: VoiceBridge service_started=10:18:30.270266163Z, зовнішній health HTTP 200/status=ok; процес 13.57 с.
- Раніше 08:21 спостерігався той самий ефект: VoiceBridge стартував після зовнішнього GET.
- Request-log query 429 за 10:10–10:25 UTC для Readonly/VoiceBridge порожній. Це не доказ відсутності 429 і не його root cause.
- Механізм 429 на Render edge vs application ще не встановлений. Збільшення readiness budget до 45 с не усунуло проблему.
- Не плутати із явними VoiceBridge quota/rate limits та Gemini 503. Успішний повтор Gemini не доводить виправлення попереднього 503.
- Не створювати keepalive, платні сервіси, альтернативні pipelines або інфраструктуру за непідтвердженою гіпотезою.
- Документація Render free: https://render.com/docs/free (останнє перевірене: spin-down 15 хв простою; старт близько хвилини). Для нових висновків прочитати актуальну документацію.

## Доступ та розгортання
Підтверджений workspace Render: tea-d9dsqdjrjlhs73ba1ga0. Не просити вибір повторно.
Remote Desktop Commander device: 71b80124-ac49-4899-828f-930b2249c509, krc-cobalt.
Checkout KRC: /tmp/krc_all_routes_integration_20261004.
Checkout VoiceBridge: /tmp/krc_facebook_url_release_20261004 (може бути detached HEAD).
Git push у терміналі не має credentials; записувати через наявний GitHub connector, потім fetch і звіряти вміст. Не виводити та не переносити credentials.
Remote rg відсутній; використовувати Python fallback. /opt/krc-cobalt недоступний krcops; не обходити привілеї.
Ізольована HTTPS fixture: /tmp/krc_ready_cross_20261004/src/cloud; base f416d8c37b1c63e1c34521ebbcadf8445cb62b44, fake engines/memory store, не для deploy.

| Сервіс | Render service ID | Deployed code |
|---|---|---|
| VoiceBridge | srv-da1kic5bedkc73d6fk60 | 072658ff512802262cef00ff424b87eedde1f934 |
| R3C Readonly | srv-dale3r942hec73c5t9hg | c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe |
| E1 YouTube | srv-dall4qv40ujc73ednpqg | c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe |
| E2 Instagram | srv-dan7vsijnfac73fmrtl0 | c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe |
| E3 Facebook | srv-danerqmgekts738oejsg | c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe |
| E4 Telegram | srv-danertv40ujc73bn9hog | c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe |

Останнє підтверджене розгортання всіх шести: live 10 жовтня 08:45–08:46 UTC; це не твердження поточної готовності після простою.
VoiceBridge health: https://voicebridge-krc-media-beta-kolemasakar.onrender.com/api/v1/health
Readonly health: https://krc-mcp-auth-sentinel.onrender.com/healthz

## Незмінні дозволи й обмеження
- FREE_ONLY; Gemini Free та безкоштовні STT-хвилини власник погодив. Перевіряти залишок і умови preflight перед довгими тестами; не переходити на paid fallback.
- Підтвердження дії на platform tool зберігається; E2/E3/E4 confirmation_probe_only=false — робочий режим, не повертати probe-only.
- Наявні чотири маршрути; не змінювати app mappings, не створювати нові parallel pipelines, не ротувати секрети.
- FAILED free-only retry лише за новою явною командою; не auto-loop. Paid/charge-uncertain replay заблокований.
- COMPLETED/PROCESSING повторно використовувати. При поверненні спочатку platform lookup/status; 404/429 не дають дозволу на нову обробку.
- Перед новою YouTube обробкою показувати data-use notice Gemini Free; явно підтверджена згода залишається обов'язковою.
- Публічні відео для довших IG/FB/TG перевірок підбирає агент самостійно. Не обіцяти підтримку довгого формату, якщо preflight або retrieval його відхиляє.
- Не архівувати повні транскрипції без окремого запиту.
- Не використовувати HP-OMEN; не розширювати sudo/root доступ.
- Відповіді українською, початок №N.; звичайні пункти маркерами, варіанти/подальші дії 1) 2) 3).
