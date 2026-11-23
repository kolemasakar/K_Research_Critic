# Owner storage and local-disk access policy

Effective date: 2026-11-23
Owner directive: NO_LOCAL_DISK_WITHOUT_EXPLICIT_OWNER_INSTRUCTION
Scope: K-Research & Critic, K_Science and K_Sentinel cross-project research workflows.

## Non-negotiable rule

DO NOT use the local disk of the owner's computers, including HP-OMEN,
Windows drives (C:, D:, etc.), desktop, Downloads, local project folders,
temporary directories, caches, or attached storage, unless the owner
directly and explicitly authorizes local-disk use for the specific task.

This prohibition includes:
- Reading, scanning, listing or searching local folders or files.
- Writing, modifying, downloading, staging, caching, exporting or saving
  project documents, source code, reports, registries, scripts or results.
- Copying, moving or deleting local files, or generating temporary files.
- Launching tests or tools which implicitly read/write local owner disks.
- Treating an online remote desktop connection as authorization to access
  the connected computer's filesystem.
- Reusing a past local-access approval as standing permission for another task.

## Approved working location

- GitHub repositories and explicitly authorized branches are the default
  canonical location for source code, research registries, documentation,
  test fixtures, non-sensitive machine-readable results, and checkpoints.
- Before any transfer to PUBLIC GitHub, verify that the file contains no
  restricted copyrighted full texts, unpublished manuscripts, credentials,
  personal information, or other non-public material. Do not publish such
  content without a separate explicit owner instruction and suitable rights.
- Use a private GitHub repository only where the owner has specifically
  approved that repository and the intended content. Otherwise stop and
  request permission rather than falling back to local disk.
- An authorized server/VM runtime is NOT an owner's local laptop/desktop
  disk. Existing KRC/Sentinel service state and VM storage remain governed
  by separate service, retention, access and deployment approvals. This
  policy does not create a new authorization to change server storage.

## Per-task exception

Only a direct owner instruction specifying local use for an identified
task may authorize it. Confine any permitted read/write/migration to the
minimum necessary paths and operations, and record the scope and evidence
in the project log. Permission for one migration or troubleshooting task
does not grant continuing access to local disks.

If a task is impossible without local access, do not silently use the
disk. Explain the blocker and ask for direct authorization. Prefer a
GitHub-only or tool-supported repository workflow.

## Stage134 correction and historical boundary

On 2026-11-23, the owner directed migration of three assistant-generated
Stage134 artifacts out of the HP-OMEN project audit directory to GitHub:
- stage134_verify_local_pdfs_20261123.py
- stage134_real_pdf_manifest_20261123.json
- stage134_real_pdf_validation_20261123.json

The corresponding authoritative repository paths are:
- K_Science/tools/stage134_verify_local_pdf_manifest.py
- K_Science/literature/source_register/STAGE134_REAL_PDF_CORPUS_2026-11-23.json
- K_Science/literature/reviews/STAGE134_REAL_PDF_VALIDATION_2026-11-23.json

The original research PDFs and pre-existing local research corpus are
NOT part of this migration. They must not be read, removed, recopied
or republished without a separate, explicit owner instruction.
Historical reports of earlier local-disk work do NOT grant future access.

## Audit requirement

Before touching any owner-computer disk, confirm and document the
specific owner instruction, authorized paths and intended read/write.
The default is DENY. Repository availability or an online Desktop
Commander agent is not a substitute for user approval.
