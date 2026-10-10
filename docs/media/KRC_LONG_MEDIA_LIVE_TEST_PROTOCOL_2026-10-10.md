# KRC MEDIA — протокол довгих живих транскрипцій v1.0
Дата: 2026-10-10. Сфера: Instagram (E2), Facebook (E3), Telegram (E4, тільки коли знято блокування); R3C read, E1 YouTube як базовий контроль. Статус: ПІДГОТОВЛЕНО / live gate NOT YET PASSED.

## Правила безпеки
- Режим FREE_ONLY; жодних платних резервних маршрутів, сторонніх платних сервісів, публікації, змін default/main.
- Виробничі MEDIA start лише після preflight/підтвердження дії. Одна обробка для кожного підтвердженого URL. Не повторювати start після невизначеної транспортної відповіді — лише scoped lookup/status. Не обходити Telegram safety block.
- Не запускати нових звернень до Render/VoiceBridge від моменту початку погодженої паузи **2026-10-11 10:00 Europe/Kyiv** до окремо погодженої холодної перевірки. Не тримати сервіси у warm стані.
- Живий тест на відео допускається лише після явного підтвердження публічної URL, фактичної тривалості 480–720 с, розбірливої мовної аудіодоріжки та доступного FREE_ONLY provider capacity. Відсутність даних про тривалість НЕ означає PASS.

## Вхідні критерії (обов’язкові)
1. Канонічний permalink `instagram.com/reel|p|tv/<id>` або `facebook.com/.../videos/<id>`/підтримуваний permalink; сторінка має відкриватися публічно без авторизації.
2. Незалежна перевірка тривалості (метадані плеєра або `ffprobe format.duration` доступного законним шляхом відеофайлу): 480.000–720.000 с включно. Записати джерело і точність вимірювання; аудіо не обчислювати за довжиною тексту.
3. Підтвердження аудіодоріжки: `ffprobe -show_streams` має audio stream із кодеком, sample_rate >0; у контрольних фрагментах на початку/середині/кінці є людська мова, не тільки музика або тиша. Для неотриманого відео — `UNVERIFIED`.
4. FREE_ONLY і `automatic_paid_fallback=false` у capabilities; доступність провайдерів, preflight і дозволені мови. Для Instagram/Facebook не використовувати YouTube/Gemini consent як заміну власного preflight.
5. Для живого навантаження зафіксувати UTC дату/час, language_hint, URL, platform, route, request_id і передтестовий баланс/ліміти, але не секрети.

## Виконання на одну платформу
A. READ-ONLY: capabilities + preflight (де підтримується); зберегти request_id, provider route, FREE_ONLY. Якщо readiness 429 — зупинитися, зафіксувати safe diagnostics, не дублювати POST.
B. ЄДИНИЙ CONSEQUENТIAL POST start до погодженого URL. Записати факт спроби і повернений job_id. Якщо відповідь втрачена — виключно scoped lookup; не повторювати POST.
C. Лише status/segments (read-only): завершити `COMPLETED`, `FAILED`, чи зафіксувати `PROCESSING` як незавершений. Не приписувати FAILED статусу PASS.
D. Перевірити `job_id` між start/status/segments; `segment_count` і послідовні `index = 0..N-1`; cursor починається з 0, без циклів і пропусків, завершується `next_cursor=null`. Перевірити відповідність сумарного UTF-16 (із **канонічним** правилом розділювачів саме цього маршруту) `transcript_characters`.
E. Якщо `start_ms/end_ms` присутні, перевірити `0 <= start < end`, неспадання інтервалів і останній end_ms у межах довжини медіа з обґрунтованою похибкою. Відсутні/null timestamps — позначити `TIMECODES_UNVERIFIED`, не підмінювати їх генерацією.
F. Перевірити detected_language, language_hint і змішані en/uk/ru фрагменти, Unicode/emoji, роздільники, відсутність обрізання між сторінками. Вручну звірити 3 короткі аудіофрагменти (початок, середина, кінець); автоматичний успіх не дорівнює точності STT.
G. Витрати: `credits_charged=0`, `paid fallback=false`, `credit_charge_uncertain=false`. Порівняти stt_seconds_charged із фактичною тривалістю із зазначенням похибки/округлення; `provider_data_deleted` перевіряти, якщо вказано, `null` ≠ true.
H. Durability: виконувати після COMPLETED один заздалегідь погоджений restart на тестовому середовищі, потім read-only status/segments і перевірити той самий job_id, вміст та витрати. Без доказу DB persistence ставити `DURABILITY_NOT_LIVE_VERIFIED`.
I. Архівувати тільки технічні метадані/агрегати та посилання; не зберігати транскрипти без окремої потреби/дозволу. Для будь-якого збою — code, stage, request_id, retryable, timestamp; не зберігати токени, raw headers, provider payload.

## Умови PASS
- Для кожної платформи: 1 перевірений публічний 480–720 с ролик з голосом; COMPLETED, повний status + усі segments; однозначна ідентичність job; правильна пагінація, довжина і Unicode; ручна звірка 3 аудіофрагментів; кошти 0/ніяких paid calls.
- Для стійкості: немає повторного provider start після lost response; read-only after actual reboot/redeploy зі сталою identity; сценарій явного failure fail-closed.
- Для повного KRC acceptance: R3C/E1–E4 матриця `PASS` за прийнятими gates. `BLOCKED`, `UNKNOWN` і `NOT_RUN` не конвертуються в PASS.

## Зафіксоване виконання до протоколу
- Instagram 2026-10-10: 41.11675 с, 1 сегмент, 331 символ, COMPLETED, 42 STT seconds, credits 0. Це SHORT, не 8–12 хв.
- Facebook 2026-10-10: 180.302938 с, 3 сегменти, 2984 символи, COMPLETED, 181 STT seconds, credits 0, job KRCM_c7547bbc-cb9b-4f20-b18d-079991116343; це MEDIUM, не 8–12 хв.
- Facebook додатковий кандидат https://www.facebook.com/Mythopia1/videos/1199799383478976/ — start tool повернув HTTP 429, без підтвердженого job, тривалість/аудіо не верифіковані; повторного POST немає.
- Instagram/Facebook 8–12 хв: на 2026-10-10 **немає незалежно підтверджених URL разом із тривалістю й аудіо**; живий критерій відкритий. Результати веб-пошуку, що містять слова «10 хв», часто описують інший контекст, не доводять duration файла.
- Telegram: попередній tool call заблокований системою безпеки; не повторювати без зміни дозволеного маршруту.

## Запис результату
Для кожного кейсу: `platform, canonical_url, verified_public, duration_seconds, audio_present, spoken_audio_verified, verification_source, route, start_request_id, job_id, start_response_recovered, status_request_id, final_status, segment_count, pages, transcript_characters, utf16_match, timecodes_valid_or_null, human_audio_spotcheck, stt_seconds_charged, credits_charged, paid_fallback, provider_data_deleted, failure_code, retryable, verdict, evidence_utc`.
