# Аудит opt-in 17/17: KRC ↔ VoiceBridge
Дата: 2026-10-10. Основа: tests/test_media_all_routes_voicebridge_integration.py.

## Чому 17 SKIPPED
У fixture є `pytest.skip("Opt-in cross-repository VoiceBridge integration")`, якщо не вказано `KRC_TEST_VOICEBRIDGE_ROOT`. Додаткова вимога — зібраний `dist/src/managed_server.js`. Вони не виконуються під час стандартного `pytest tests` за замовчуванням.

## 17 реальних сценаріїв
- 4 × start / status / pagination / reuse / local-wrapper restart: YouTube, Instagram, Facebook, Telegram;
- 3 × fail-closed security scopes: Instagram, Facebook, Telegram;
- 1 × read-only 65 requests without consuming socket legacy limiter;
- 1 × 429 diagnostic behavior across 5 dispatchers;
- 4 × 480–720 s multilingual transcripts, 57 segments, 9 pages;
- 4 × lost HTTPS start response, lookup-only recovery without second provider work.
Сума: **17**.

## Фактичне відтворення
1. Standard 482 PASS, 17 SKIP. 
2. Старий ізольований fixture f416d8c: 15 PASS, 2 FAIL (FB/TG recovery), бо route lookup не використовував нове `lookupFreeRoute`.
3. Повний production source branch 5293e4e вставлений як fixture: 4 PASS, 13 FAIL; fixture contracts/constructor setup не були адаптовані до production гілки. Цей прогін не є доказом несправності production.
4. Підготовлено відокремлений worktree старого fixture (не production): застосовано тільки актуальні `managed_media_http.ts` і `managed_media_service.ts`, `npm run build` PASS, opt-in тест **17/17 PASS, 35.31 s**.
5. Тести локальні й з фіктивними провайдерами; не перевіряють real STT, Render cold start або Postgres crash recovery.

## Висновок
SKIPPED з’ясовано й усунуто **для ізольованого контрольного прогону**. Наступне покращення відтворюваності: оформити сумісність fixture як окремий контрольований commit/patch і перевірити чисту збірку. Не змішувати fixture patch з продуктивним релізом без окремого review.
