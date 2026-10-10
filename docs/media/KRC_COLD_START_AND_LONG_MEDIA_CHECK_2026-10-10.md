# KRC MEDIA: холодний запуск, втрата відповіді та розширена перевірка — 2026-10-10

## Рішення та межі робіт
Виконано план інженерних робіт за командою власника «виконуй план».
FREE_ONLY, наявні чотири маршрути, обов'язкові підтвердження запуску та згода Gemini збережені.
Нових сервісів не створено. Ключі не ротовано. Main не змінено.

## Реалізовано
- Обмежене очікування готовності VoiceBridge: до 45 секунд, до 24 health GET, тайм-аут окремого GET до 5 секунд. Здоровий стан вимагає HTTP 200 та JSON status=ok.
- Після тимчасової помилки оголошеної операції читання допускається лише один повтор цієї операції після готовності. Явні API rate limits і Retry-After повертаються без внутрішнього повтору.
- Та сама перевірка готовності застосована перед усіма чотирма маршрутами запуску. Якщо готовності немає, запит на обробку не надсилається.
- Після транспортної втрати відповіді на вже надісланий запуск виконується лише lookup. PROCESSING/COMPLETED повертається як відновлений стан; запуск обробки не повторюється. Невдалий, відсутній або некоректний lookup зберігає початкову помилку.
- VoiceBridge: для scoped lookup Facebook/Telegram додано правильні ключі безкоштовних маршрутів. Читання проходить лише вже наявний ланцюг до 16 спроб. Воно не резервує нове завдання, не виправляє orphan-стан і не запускає провайдера. Старий native lookup збережений.
- Діагностика показує етап, факт спроби consequential POST, кількість перевірок готовності та allowlisted формат відповіді json/html. Сирі повідомлення та секрети не виводяться.

## Перевірки
- KRC: **496/496 PASS**, без пропусків, 83.59 секунди. Лог: /tmp/krc_all_four_outcome_check_20261010.log.
- Серед них 17 перевірок через справжній локальний HTTPS та VoiceBridge handlers/engines із фіктивними провайдерами.
- Чотири сценарії тривалістю 8–12 хвилин: en/ru/uk, 57 сегментів, дев'ять сторінок по сім сегментів. Перевірено точну послідовність, UTF-16 підрахунок із розділювачами, кінцеві часові мітки, відсутність повторних provider calls та paid fallback.
- Чотири сценарії втрати HTTPS-відповіді після виконання start: усі маршрути знаходять COMPLETED без другого виклику провайдера.
- VoiceBridge: **276/276 PASS**, без пропусків, 86.968 секунди; build PASS. Лог: /tmp/krc_free_lookup_final_check_20261010.log..
- Cross-repository fixture ізольований: база research f416d8c; production Gemini, managed HTTP та managed service синхронізовані. Ін'єкція фіктивних engines і memory store не переноситься в production. Це не перевірка точності живого STT чи відмовостійкості PostgreSQL.

## Живі результати 10 жовтня
- Після зовнішньої перевірки всі шість health endpoints повернули HTTP 200; E2/E3/E4 залишилися у робочому режимі.
- Усі дев'ять операцій читання відповіли: capabilities та два preflight успішні; шість lookup/status/segments повернули application JSON 404 для відсутніх результатів. Попередні результати 4 жовтня мають TTL=3600 секунд. Сам HTTP 404 не доводить причину зникнення.
- Capabilities request_id: 15b56891-db67-42f2-8310-fb4a38ac7557.
- Довше живе відео: https://www.youtube.com/watch?v=_T8cn2J13-4, NASA «How We Are Going to the Moon». Посилання підтверджене на https://science.nasa.gov/resource/how-we-are-going-to-the-moon/.
- Перша спроба зупинилася на readiness, consequential_post_attempted=false; завдання не створено.
- Наступний запуск утратив транспортну відповідь через 20 секунд; lookup знайшов PROCESSING. Завдання KRCM_e71f7ede-6598-4718-b5fb-a26b6dcdf6df створене 08:28:22.143Z, завершилося FAILED 08:31:49.714Z.
- Остаточна причина цієї обробки: GEMINI_YOUTUBE_FAILED, provider_http_status=503, provider_error_code=service_unavailable, retryable=true. Транскрипції немає.
- STT seconds=0, credits_charged=0, credit_charge_uncertain=false; це не вимірювання Gemini token usage. provider_data_deleted=null.
- Після FAILED повторного запуску не було. Для нового повтору потрібна нова явна команда власника.

## Відкрита проблема холодного запуску
Перший capabilities повернув 429. Після першого розгортання реальна холодна перевірка також завершилася 429 з readonly_health_ready=false та 22 health attempts.
Журнал VoiceBridge не показав запуску за час цієї перевірки. Після зовнішнього GET з krc-cobalt сервіс стартував 08:21:29.214Z, зовнішній health повернув 200 о 08:21:35.157Z, а наступний capabilities був успішним.
Це підтверджує різницю спостережень для Render → Render і зовнішнього запиту. Точний механізм 429 не встановлено; збільшення бюджету саме по собі не усунуло його.
Документація Render описує зупинку free web service після 15 хвилин простою та запуск приблизно за хвилину: https://render.com/docs/free.
Живий provider 503 також не вважається виправленим інженерними змінами.

## Розгортання
Підтверджено live для всіх шести сервісів та HTTP 200 на їхніх health endpoints.

KRC production code: c7b7f9c9a8d168ce63d1f1efbc5fb8e1dd5bdebe; VoiceBridge production code: 072658ff512802262cef00ff424b87eedde1f934.

| Сервіс | Deploy | Live UTC |
|---|---|---|
| VoiceBridge | dep-db4vlu0473hc739b20sg | 2026-10-10T08:45:08.683295Z |
| Readonly | dep-db4vluflk1mc73870pdg | 2026-10-10T08:45:22.179817Z |
| YouTube | dep-db4vluvlot8c73d6lea0 | 2026-10-10T08:45:27.160664Z |
| Instagram | dep-db4vlv2jnfac738n9cug | 2026-10-10T08:45:24.27319Z |
| Facebook | dep-db4vlvflot8c73d6lhjg | 2026-10-10T08:46:13.541255Z |
| Telegram | dep-db4vlvqd0e5s73dlv9h0 | 2026-10-10T08:45:27.481933Z |

Після реального перезапуску VoiceBridge lookup/status зберегли той самий FAILED job та Gemini 503. Це підтверджує збереження цієї діагностики через цей перезапуск, не DB failover.
Після розгортання capabilities request_id=8aedcff7-2fc0-4a57-814d-c1e5e5a7e12b; lookup request_id=f9a39e2d-fcd5-4cf7-b8d8-93bc6669b5b8; status request_id=c80f070f-b48a-441e-bad5-3e115fc98272.
E2/E3/E4 confirmation_probe_only=false; підтвердження дії та згода Gemini залишаються обов'язковими.

## Наступна робота
1. Дослідити джерело холодного 429 на межі Render; не змішувати його з rate limit VoiceBridge чи Gemini 503.
2. Повторити довше живе відео лише після нової явної команди; не використовувати paid fallback.
3. Погодити CriticProfile для теми «Плани Artemis у відео NASA та їхня актуальність станом на 10.10.2026». Профіль REVIEW_REQUIRED, незалежне дослідження не починалося.
