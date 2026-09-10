from pathlib import Path


WORKFLOW = Path(".github/workflows/krc-media-tier0-control.yml")


def _text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_krc_tier0_workflow_is_manual_main_only() -> None:
    text = _text()
    assert "on:\n  workflow_dispatch:\n" in text
    assert "push:" not in text
    assert "pull_request:" not in text
    assert "schedule:" not in text
    assert "github.repository == 'kolemasakar/K_Research_Critic'" in text
    assert "github.ref == 'refs/heads/main'" in text


def test_krc_tier0_workflow_uses_dedicated_oidc_identity() -> None:
    text = _text()
    assert "contents: read" in text
    assert "id-token: write" in text
    assert "TS_KRC_OAUTH_CLIENT_ID" in text
    assert "TS_KRC_AUDIENCE" in text
    assert "tags: tag:krc-media-github-actions" in text
    assert "tags: tag:github-actions" not in text


def test_krc_tier0_workflow_targets_exact_node_and_helper() -> None:
    text = _text()
    assert "expected_host='krc-media-node1'" in text
    assert "expected_ip='100.118.132.8'" in text
    assert '"krcops@$KRC_TS_IP"' in text
    assert "sudo -n /usr/local/sbin/krc-tier0-status" in text
    assert "KRC_TIER0_STATUS_VERSION=1" in text
    assert "hostname=krc-cobalt" in text
    assert "tailscale_ipv4=100.118.132.8" in text


def test_krc_tier0_workflow_contains_required_negative_boundaries() -> None:
    text = _text()
    required = (
        "KRC_PHASE_6_ARBITRARY_ROOT=DENIED",
        "KRC_PHASE_6_HELPER_ARGUMENT_INJECTION=DENIED",
        "KRC_PHASE_6_DOCKER_ACCESS=DENIED",
        "KRC_PHASE_6_OWNER_USER=DENIED",
        "KRC_PHASE_6_ROOT_USER=DENIED",
        "KRC_PHASE_6_KGM_TCP22_ISOLATION=PASS",
    )
    for marker in required:
        assert marker in text


def test_krc_tier0_workflow_has_no_mutation_surface() -> None:
    text = _text().lower()
    forbidden = (
        "systemctl restart",
        "systemctl stop",
        "systemctl start",
        "service restart",
        "docker restart",
        "docker exec",
        "docker compose",
        "apt-get",
        "apt install",
        "pip install",
        "sed -i",
        "chmod ",
        "chown ",
        "rm -",
        "mv ",
        "cp ",
        "tee ",
        "sudo -n bash",
        "sudo -n sh",
    )
    for token in forbidden:
        assert token not in text


def test_krc_tier0_workflow_records_terminal_gate() -> None:
    text = _text()
    assert "KRC_PHASE_6_PROJECT_ISOLATED_OIDC_CONTROL=PASS" in text
    assert "KRC_PHASE_6_OPERATION=TIER0_READ_ONLY" in text
