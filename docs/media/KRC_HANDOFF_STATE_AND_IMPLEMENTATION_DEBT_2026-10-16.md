# KRC — стан, борги реалізації та відновлення в новому чаті
Дата:2026-10-16. Власник завершив поточний чат після звіту№82; поточне завдання — фіксація, без нових медіазапусків чи deploy.

## Обов'язкові рішення власника
Лише публічні відео без соціального login,cookies,credentials. FREE_ONLY. Instagram development PAUSED. Попередній план авторизованої Instagram-сесії CANCELLED_NOT_EXECUTED. Не відновлювати цей план.
R4 PRIVATE=PARTIAL; PUBLIC=HOLD; TELEGRAM LIVE=BLOCKED. Історичні дозволи не скасовують цих обмежень.
Зміни обмежувача підготовлені тільки для тестового середовища; окремий production-допуск не наданий.
Нові provider starts поставлені на паузу до завершення account-level перевірки FREE_ONLY.

## Авторитетні репозиторії та версії
- Документація:kolemasakar/K_Research_Critic,branch agent/krc-public-media-r3-integration. Head перед цим checkpoint2769a5bc4d7730d7702fb28a6c8d268fb22d4ccc.
- Runtime:kolemasakar/VoiceBridge,branch agent/krc-media-gemini-migration. GitHub HEAD підтверджено c9f5ee7b9ccccdf407265c7d085cbec42aa553be.
- Render service srv-da1kic5bedkc73d6fk60,workspace tea-d9dsqdjrjlhs73ba1ga0 (My Workspace).
- Повторна перевірка Render під час checkpoint:dep-db8v5g3rjlhs73dlhhm0 LIVE,production commit65737cfb7e3a89bdaaed95bdf5519d65abae0acf. Новий c9f5ee7 НЕ розгорнутий. autoDeploy раніше підтверджено no.
- Локальний VoiceBridge у scratch має HEAD65737cf і робочі зміни, які вже збережено в GitHubc9f5ee7; їхню точну відповідність код/тести/док перевірено. Не вважати їх незбереженим новим patch і не комітити вдруге. Для продовження брати чистий checkout GitHubc9f5ee7.

## Виконана реалізація
Production65737cf:безпечна allowlist-класифікація Cobalt HTTP400; TypeScript PASS,повна регресія284/284.
Test-only c9f5ee7:YouTube Gemini start і managed start охоплені спільним process-local admission; включені scoped E1–E4 tokens; read-only маршрути не витрачають admission.
Відповіді Gemini,Cobalt,managed jobs додають provider_billing_verified=false,provider_cost_usd=null,provider_free_balance_usd=null.
Legacy credits_charged/credits_remaining_estimate/credit_charge_uncertain не змінені задля сумісності:це внутрішні retrieval credits,НЕ рахунок чи баланс провайдера.
Перевірки c9f5ee7:TypeScript PASS,цільові30/30,повна285/285 PASS,без skips/fails,49.11s,diff check і GitHub parity PASS. Нових live provider calls при цій зміні не було.
Опис:
https://github.com/kolemasakar/VoiceBridge/blob/c9f5ee7b9ccccdf407265c7d085cbec42aa553be/docs/media/KRC_YOUTUBE_ADMISSION_AND_BILLING_VISIBILITY_2026-10-16.md

## Результати платформ
Facebook:новий public NASA source https://www.facebook.com/NASASCaN/videos/8368792419872400/ .
job KRCM_b8b621ce-144f-4bba-bcfb-67747e80a2c5;request2ca96f7c-b749-4d31-8300-7960b05ad4a1;2026-10-16T13:29:47–13:30:04UTC.
COMPLETED,reused=false,duration167.275938s,STT168s,3segments2630chars,provider_data_deleted=true;окреме читання всіх сегментів PASS,request39003b81-249c-4d66-86a0-c982593b3b13.
Працездатність одного анонімного маршруту підтверджена;не універсальна підтримка Facebook.
YouTube:public source https://www.youtube.com/watch?v=6yXU8a5CK2Q .
Дві terminal відмови Gemini3.8Flash:
jobKRCM_8f3accb1-7b7f-45e0-ba36-a80c00eeba19,status request57aa645e-a749-4905-b0c8-688802bae15a;
jobKRCM_f1231bb9-1fd1-4dcf-adea-8389376ecbdc,status requestc8683af5-1715-486b-9922-b5b35921a715.
GEMINI_YOUTUBE_FAILED,HTTP503,service_unavailable,STT0,transcript0. Це не доказ потреби YouTube-login або вичерпання квоти. Root cause OPEN;Render logs за інтервал порожні. Не повторювати безконтрольно.
Instagram:container helperv3,source Dcea3BiPTBm:oEmbed401,GraphQL401,login_required і temporary-wait marker;embed200 без legacy/context;web prerequisites присутні;Cobalt400 error.api.fetch.empty. API auth працює,внутрішній ключ не виводився. Працездатний анонімний retrieval не встановлений,розвиток PAUSED. Не заявляти глобальну неможливість anonymous viewing.
Telegram:офіційний public-web/embed route і історичний completed від04.10 доводять можливість;нового start не виконували через LIVE BLOCKED.
Історичні jobs Facebook/Telegram і YouTube lookup повернули404;конкретна причина не встановлена. TTL default1h може пояснювати відсутність,але це не доведений діагноз і не доказ втрати PostgreSQL.

## Підтвердження тарифів від власника
Три зображення16.10 переглянуто;raw screenshots,emails,billing IDs у GitHub не копіювали.
AssemblyAI:Free,$48.27free credits remaining,$1.73grant consumed. Auto-pay на зображенні не видно. Прив'язку production API key саме до цього workspace не звірено.
Google Rate Limit:project VoiceBridge,Free tier.3.7Flash і3.8Flash:5RPM,250000TPM,20RPD.
Екран28Days показує ПІКИ,не поточний залишок:3.7=3RPM,319.45KTPM,7RPD;3.8=1RPM,67TPM,4RPD.
3.7 перевищивTPM історично;3.8 нижче показаних лімітів,тому зображення не доводить причини його503.
Billing screenshot вибраний My First Project з inactive/unsupported billing,це ІНШИЙ проєкт;не переносити на VoiceBridge.
Production key→VoiceBridge mapping залишається НЕПІДТВЕРДЖЕНИМ.

Публічні правила,перевірені16.10:
Gemini3.8 має Free Tier;YouTube URL preview/public-only,free allowance8h/day;RPM/TPM/RPD залежать від проєкту,RPD reset midnight Pacific.
AssemblyAI Universal-2$0.15/h;стартовий grant$50 непоновлюваний,не нескінченні безкоштовні хвилини.
Для Facebook167.28s base-rate estimate≈$0.00697 спожитого балансу,не invoice. KRCcredits0 не означає відсутність provider consumption.
Cobalt self-hosted не має окремого metered retrieval API у нашому маршруті;витрати інфраструктури окремі.

## Борги реалізації — НЕ виконані
P0.Y1:окремий Gemini limiter5RPM і20RPD замість лише загального60RPM/1sec. Durable counters,atomic reservations,переживання restart,multi-instance contention;правильний Pacific day та DST. Ліміти configurable і conservative;account-specific shared usage може бути поза KRC.
P0.Y2:контроль250KTPM і8h/day public YouTube;визначити надійний спосіб оцінювання/резервування вхідних video tokens та duration ДО generate;невідомі duration/tokens не вважати0. Один довгий request може перевищитиTPM. Локальний estimator не гарантує відповідності Google.
P0.Y3:тести меж5/6RPM,20/21RPD,token budget,Pacific midnight/DST,restart і конкурентних reserve;dedup/reuse не повинен витрачати новий provider call. Жодних paid чи login fallback.
P0.A1:звірити Google deployed key→Free VoiceBridge project без розкриття ключа.
P0.A2:звірити AssemblyAI deployed workspace,залишок grant,Auto-pay/payment state;не купувати кредити,не upgrade.
P1.Y4:bounded retry/cooldown з Retry-After/backoff;не автоматизувати множинні starts після503/429;зберігати quota consumption помилкових спроб консервативно.
P1.Y5:model Free Tier allowlist/перевірка змін тарифів;прапорець environment не є entitlement.
P1.O1:provider token/financial usage accounting і client-visible пояснення legacy credits;нові unknown billing fields уже зроблені,але не invoice integration.
P1.O2:process-local admission не distributed,можливі restart/multi-instance обходи;потрібен durable job lease. inFlight process-local.
P1.O3:логування Gemini:чому порожні Render logs,і безпечна telemetry без ключів,transcript,raw media URLs.
P1.D1:після окремого deployment-допуску розгорнути точний tested SHA,read-only smoke;лише після account/quota gates один короткий YouTube контрольний запуск.
P2.T1:Telegram нове live-приймання тільки після зняття власником LIVE BLOCKED.
P2.I1:Instagram лише dormant backlog;ніякого розвитку з credentials. Research fallback candidate/mock10tests архівовано,production adapter не змінений. Exact Docker image/digest та production adapter file hash не підтверджені;root directory access не розширювати.

## Доступ та обмеження
krc-cobalt RDC device71b80124-ac49-4899-828f-930b2249c509,userkrcopsUID1002. Немаєdocker group/unrestricted sudo. Не обходити заборони і не змінювати привілеї.
Вузькі root-owned helpers systemctl start krc-cobalt-diag@{summary,logs,probe,instagram}.service → /run/krc-cobalt-diag/{mode}.json. RuntimeDirectoryPreserve=yes.
Helperv3 installed owner,hash306c49816b384385c38b3d54fcbd8741f5f19bd1a65088fb9f7ec3953477193b;production container unchanged.
Cobalt root endpoint reports11.7.1/gitSHAa636575b09de1fc55d9b8cd98cac88f5f2f16b42;не називати independently verified image digest.
Credentials/cookies не запитувати й не архівувати. GitHub remote commits авторитетні;локальніscratch файли не є довговічним єдиним джерелом.

## Документація для читання
Усі нижче у docs/media/ тієї ж KRC-гілки:
- KRC_ANONYMOUS_PUBLIC_VIDEO_FEASIBILITY_2026-10-16.md
- KRC_ANONYMOUS_LIVE_RECHECK_2026-10-16.md
- KRC_YOUTUBE_503_DIAGNOSTIC_2026-10-16.md
- KRC_FREE_ONLY_TARIFF_AND_IMPLEMENTATION_AUDIT_2026-10-16.md
- KRC_FREE_ONLY_REMEDIATION_TESTED_2026-10-16.md
- KRC_OWNER_BILLING_SCREENSHOT_EVIDENCE_2026-10-16.md
- KRC_INSTAGRAM_CONTAINER_LOGIN_THROTTLE_CONFIRMED_2026-10-16.md
- KRC_INSTAGRAM_AUTH_SESSION_ISOLATED_TEST_PLAN_2026-10-16.md (CANCELLED)

## Старт нового чату
Прочитати цей checkpoint і підтвердити remote HEAD/production SHA. Продовжувати зP0.Y1–Y3 у test-only checkoutc9f5ee7. Не припускати,що реалізація5RPM/20RPD/token guards уже існує:це наступна робота,лише план була надана у№82.
Account gatesA1/A2 не оголошуватиPASS лише за screenshot.
Зберігати українську,наскрізну нумерацію відповідей. Не вимагати повторно вже надану згодуGemini Free;але не виконуватиstart,доки чинна пауза account/quota acceptance.
