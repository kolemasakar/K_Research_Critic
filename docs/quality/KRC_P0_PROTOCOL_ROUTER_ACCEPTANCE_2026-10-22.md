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
