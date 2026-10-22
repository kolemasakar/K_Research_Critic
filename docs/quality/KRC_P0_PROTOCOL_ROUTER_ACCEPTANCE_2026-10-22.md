# KRC P0 — Protocol Router Acceptance Cases (design/static checks)

Status: SPEC IMPLEMENTED IN CANONICAL PROMPT; BEHAVIORAL TESTS NOT RUN.
Scope: private KRC Core only; NO_MCP; no deployment.

## Routing fixtures
| ID | Ukrainian user request | Expected «Наукова робота» | Reason | Protocol |
|---|---|---|---|---|
| R01 | Напиши наукову статтю про фотограмметрію з бібліографією | ТАК | Пряма вказівка | Scholarly Research |
| R02 | Підготуй дисертаційне дослідження з відтворюваною методологією | ТАК | Пряма вказівка | Scholarly Research |
| R03 | Сформулюй гіпотезу і план статті для рецензованого наукового журналу | ТАК | Контекстний зміст | Scholarly Research |
| R04 | Перевір правдивість тверджень у науковій статті | НІ | Не виявлено | KRC Core |
| R05 | Досліди новини про наукові відкриття | НІ | Не виявлено | KRC Core |
| R06 | Порівняй два смартфони за характеристиками | НІ | Не виявлено | KRC Core |
| R07 | Проаналізуй дослідження та перевір методологію | НІ | Не виявлено | KRC Core |
| R08 | Знайди статті про геодезичні вимірювання | НІ | Не виявлено | KRC Core |
| R09 | Створи систематичний огляд літератури для наукової публікації | ТАК | Пряма вказівка | Scholarly Research |
| R10 | Досліди можливість застосування методу | НІ | Не виявлено | KRC Core |

## Profile acceptance
- After profile creation, preserve pre-existing approval menu; no automatic research.
- When CriticProfile is shown or revised, show all three fields: «Наукова робота», «Підстава визначення», «Обраний протокол».
- User override ТАК→НІ or НІ→ТАК updates all three fields consistently; route does not change silently.
- Any material route change after approval returns profile to REVIEW_REQUIRED.
- Standard CORE reports preserve source accounting, cross-check floors, Critic ledger and review protocol.
- Scholarly manuscript integrity includes actual detector outputs only when accessible, permitted and authorized; otherwise NOT_TESTED/UNAVAILABLE, never fabricated results.
- No deployment, release, server writes, or public/MEDIA flows under this change.

## Acceptance state
- Repository prompt static presence check: PASS at commit 8c14295a85f2b81a8150902a71bd0ff0a230c848.
- Runtime routing / regression fixture execution: NOT_RUN.
- Private plugin released-version parity: NOT_VERIFIED.

## 2026-10-22 verification update
- Original tar.gz archive and alternative ZIP both passed local archive readability checks and contain `skills/instructions/SKILL.md` at the archive root. The original file is 10,931 UTF-8 bytes. Thus structural absence cannot be confirmed as the cause of rejection.
- Plugin Creator update attempts using a local path, sandbox URI and uploaded file IDs all returned `INVALID_ARGUMENT: Plugin package must contain ... skills/*/SKILL.md`. This suggests an unresolved upload/attachment resolution issue, not established malformed SKILL.md content. No release update succeeded.
- Installed plugin remains private release 0.19.8, `pluginrel_6ad64530575c8191872f3280de9181bd`; deployed skill lacks router. Parity FAIL.
- Prior fixture result 10/10 was a deterministic mock-only routing check, **not** an installed-plugin behavioral test. Full gate override and runtime regression remain NOT_RUN.
- P0.3 design file committed separately, no production changes.
