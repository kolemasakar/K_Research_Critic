# PROJECT_FILE_STANDARD
Універсальний стандарт назв, форматів, кодування, версійності та розміщення файлів у GitHub-проєктах.

Standard: PROJECT_FILE_STANDARD
Version: 1.0
Status: ACTIVE

## 1. Purpose

This document defines a reusable file and directory standard for software, AI, automation, research, and related GitHub projects.

The standard defines:
- file naming conventions;
- directory naming conventions;
- reserved project files;
- documentation encoding rules;
- report and analysis encoding rules;
- versioning rules;
- date and identifier formats;
- generated and temporary file rules;
- Git tracking rules.

## 2. Scope

This standard is intended for reuse across multiple projects.

Project-specific rules may extend this document but should not contradict it unless the exception is explicitly documented.

## 3. General Naming Rules

File and directory names must:
- use English words;
- use ASCII characters only;
- contain no spaces;
- avoid non-portable special characters;
- use only letters, digits, underscore, hyphen, and period where applicable;
- clearly describe the file purpose without opening the file.

One file should have one primary responsibility.

## 4. File Naming Convention

### 4.1 Project documentation

Project documentation uses UPPER_SNAKE_CASE names with the `.md` extension.

Examples:

```text
README.md
ROADMAP.md
ARCHITECTURE.md
PROJECT_HISTORY.md
PROJECT_FILE_STANDARD.md
API_CONTRACTS.md
TEST_PLAN.md
```

README.md is a conventional exception to strict UPPER_SNAKE_CASE wording.

### 4.2 Python source files

Python modules use snake_case.

Examples:

```text
supervisor.py
research_agent.py
critic_agent.py
state_machine.py
source_validator.py
```

### 4.3 Configuration files

Configuration filenames use lowercase or snake_case unless a tool requires another convention.

Examples:

```text
settings.yaml
logging.yaml
.env.example
```

### 4.4 Generated task artifacts

Generated artifacts should include a stable task or run identifier when multiple results may coexist.

Pattern:

```text
<TASK_ID>_<ARTIFACT>.md
```

Examples:

```text
R_000001_FINAL_REPORT.md
R_000001_REVIEW_PROTOCOL.md
```

## 5. Directory Naming Convention

Directories use lowercase_snake_case or a single lowercase word.

Examples:

```text
agents/
supervisor/
tools/
models/
prompts/
config/
tests/
scripts/
output/
logs/
docs/
```

A project may use a domain-specific structure instead of a generic `src/` directory.

## 6. Reserved Project Files

The following names are reserved for common project purposes:

```text
README.md
ROADMAP.md
ARCHITECTURE.md
PROJECT_HISTORY.md
PROJECT_FILE_STANDARD.md
CHANGELOG.md
CONTRIBUTING.md
LICENSE
.env.example
.gitignore
```

These files should keep stable names across projects when used.

## 7. Documentation Encoding Rules

### 7.1 Project documentation

Project documentation files are ASCII by default.

After the document title or top-level heading, each documentation file must contain exactly one short Ukrainian description line explaining the document purpose.

This Ukrainian description line is the only mandatory non-ASCII line in otherwise ASCII documentation.

Example:

```text
# ARCHITECTURE
Короткий опис архітектури, компонентів та їх взаємодії.

Version: 1.0
Status: ACTIVE
```

After this Ukrainian description line, the remaining documentation content must use ASCII unless a project-specific exception is explicitly approved.

### 7.2 Reports, analyses, and work results

Reports, analyses, generated research results, and other user-facing work products use UTF-8 by default.

Examples:

```text
FINAL_REPORT.md
REVIEW_PROTOCOL.md
ANALYSIS.md
RESEARCH_RESULT.md
```

These files may freely contain Ukrainian and other Unicode text.

### 7.3 Filenames

All filenames remain ASCII regardless of file content encoding.

## 8. File Format Rules

Recommended formats:

| Purpose | Format |
|---|---|
| Human-readable documentation | `.md` |
| Python source | `.py` |
| Configuration | `.yaml` |
| Machine exchange | `.json` |
| Tabular data | `.csv` |
| Environment configuration | `.env` |
| Database schema and migrations | `.sql` |
| Runtime logs | `.log` |

Guiding rule:

```text
Markdown for humans.
JSON for machines.
```

JSON should not be used as the primary format for human documentation.

## 9. Versioning Rules

Stable project documents should normally keep one filename and rely on Git history.

Preferred:

```text
ARCHITECTURE.md
ROADMAP.md
PROJECT_HISTORY.md
```

Avoid:

```text
ARCHITECTURE_v1.md
ARCHITECTURE_v2.md
ARCHITECTURE_FINAL.md
ARCHITECTURE_FINAL_2.md
```

Explicit versions are used only when multiple protocol or specification versions must coexist.

Pattern:

```text
vMAJOR_MINOR
```

Examples:

```text
API_PROTOCOL_v1_0.md
API_PROTOCOL_v1_1.md
API_PROTOCOL_v2_0.md
```

## 10. Status Naming Rules

Do not use ambiguous lifecycle suffixes such as:

```text
final2
new
latest
fixed
copy
new_final
```

Status should be represented by:
- Git history;
- project phase;
- explicit version;
- document metadata.

`FINAL` is allowed when it identifies the artifact type rather than a revision status.

Example:

```text
FINAL_REPORT.md
```

## 11. Checkpoint Files

Checkpoint filenames may include phase and status because each checkpoint is a separate historical artifact.

Pattern:

```text
PROJECT_CHECKPOINT_<PHASE>_<STATUS>.md
```

Examples:

```text
PROJECT_CHECKPOINT_PHASE_3_COMPLETE.md
PROJECT_CHECKPOINT_PHASE_4_2_COMPLETE.md
```

If multiple checkpoint protocol versions must coexist:

```text
PROJECT_CHECKPOINT_PHASE_4_2_v1_1.md
```

## 12. Technical Specification Files

Component specifications should use:

```text
<COMPONENT>_<DOCUMENT_TYPE>.md
```

Examples:

```text
SUPERVISOR_SPEC.md
AGENT_INTERFACE.md
DATABASE_SCHEMA.md
RESEARCH_WORKFLOW.md
API_CONTRACTS.md
```

## 13. Numeric Prefixes

New projects should not use numeric filename prefixes only to control display order.

Avoid:

```text
01_README.md
17_ROADMAP.md
42_BOOTSTRAP_GENERATOR.md
```

Prefer:

```text
README.md
ROADMAP.md
BOOTSTRAP_GENERATOR.md
```

If a documentation reading order is required, define it in README.md or DOCS_INDEX.md.

## 14. Date Format

Dates use ISO 8601 calendar format:

```text
YYYY-MM-DD
```

Example:

```text
2026-08-12
```

If a date is required in a filename:

```text
RESEARCH_SNAPSHOT_2026-08-12.md
```

Avoid ambiguous date formats.

## 15. Identifiers

Machine-generated artifacts should use stable identifiers.

Examples:

```text
TASK_000001
RUN_000001
REPORT_000001
R_000001
```

Related artifacts should reuse the same task identifier.

Example:

```text
R_000001_FINAL_REPORT.md
R_000001_REVIEW_PROTOCOL.md
```

## 16. Source-Controlled and Generated Files

Source-controlled content normally includes:

```text
README.md
ARCHITECTURE.md
ROADMAP.md
PROJECT_HISTORY.md
docs/
agents/
supervisor/
tools/
models/
prompts/
config/
tests/
scripts/
```

Generated or runtime content normally includes:

```text
output/
logs/
cache/
runtime/
```

Generated content should not be committed unless it is intentionally preserved as an approved project artifact.

## 17. Temporary Files

Temporary and local runtime files should normally be excluded from Git.

Typical exclusions:

```text
*.tmp
*.bak
*.log
__pycache__/
.env
cache/
runtime/
```

`output/` may be excluded when it contains only runtime results. Approved reference outputs may be committed intentionally.

## 18. Directory Placeholders

Git does not track empty directories.

When a required project directory must exist before it contains real files, an empty `.gitkeep` file may be used temporarily.

The `.gitkeep` file should be removed when the directory receives tracked content unless retaining it serves a clear purpose.

## 19. Exceptions

A project-specific exception is allowed only when required by:
- an external protocol;
- a framework or tool convention;
- compatibility constraints;
- an explicit project decision.

Exceptions should be documented in the project architecture, README, or another authoritative project document.

## 20. Standard Governance

The canonical reusable copy of this standard should be stored in a shared repository intended for cross-project standards.

Projects may copy PROJECT_FILE_STANDARD.md into their own `docs/` directory for local reference.

The canonical standard should be updated deliberately. Projects should not silently diverge from it.

## 21. Compliance Checklist

Before adding a new file, verify:
- filename is ASCII;
- filename follows the naming convention for its type;
- directory name follows the directory convention;
- documentation uses ASCII except for the required Ukrainian description line;
- reports and analyses use UTF-8 by default;
- version suffix is used only when multiple versions must coexist;
- date uses YYYY-MM-DD when needed;
- generated artifacts use stable IDs when appropriate;
- temporary or secret files are excluded from Git;
- no ambiguous suffix such as new, latest, fixed, or final2 is used.

## 22. Standard Metadata

```text
Name: PROJECT_FILE_STANDARD
Version: 1.0
Status: ACTIVE
Canonical repository: AI_general
Default documentation encoding: ASCII
Documentation description exception: one Ukrainian UTF-8 line after title
Reports and analyses encoding: UTF-8 by default
Filename character set: ASCII
```
