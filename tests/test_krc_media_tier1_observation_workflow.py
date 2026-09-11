from pathlib import Path


WORKFLOW = Path(".github/workflows/krc-media-tier1-observation.yml")
PINNED_TAILSCALE_ACTION = (
    "tailscale/github-action@306e68a486fd2350f2bfc3b19fcd143891a4a2d8"
)


def _text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_krc_tier1_workflow_is_manual_main_only_and_fails_closed() -> None:
    text = _text()
    assert "on:\n  workflow_dispatch:\n" in text
    assert "push:" not in text
    assert "pull_request:" not in text
    assert "schedule:" not in text
    assert "test \"$GITHUB_REPOSITORY\" = 'kolemasakar/K_Research_Critic'" in text
    assert "test \"$GITHUB_REF\" = 'refs/heads/main'" in text


def test_krc_tier1_workflow_reuses_minimal_dedicated_oidc_identity() -> None:
    text = _text()
    assert "permissions:\n  id-token: write\n" in text
    assert "contents: read" not in text
    assert "actions/checkout" not in text
    assert "TS_KRC_OAUTH_CLIENT_ID" in text
    assert "TS_KRC_AUDIENCE" in text
    assert "tags: tag:krc-media-github-actions" in text
    assert "tags: tag:github-actions" not in text
    assert PINNED_TAILSCALE_ACTION in text


def test_krc_tier1_workflow_targets_exact_node_and_exact_helper() -> None:
    text = _text()
    assert "expected_host='krc-media-node1'" in text
    assert "expected_ip='100.118.132.8'" in text
    assert '"krcops@$KRC_TS_IP"' in text
    assert "sudo -n /usr/local/sbin/krc-tier1-media-status" in text
    assert "backend_type" in text
    assert "tier1_backend_status" in text


def test_krc_tier1_workflow_pins_current_backend_identity() -> None:
    text = _text()
    assert (
        "sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62"
    ) in text
    assert "test \"${seen[backend_loopback_only]}\" = 'yes'" in text
    assert "test \"${seen[backend_port]}\" = '9000'" in text
    assert "test \"${seen[backend_user]}\" = 'node'" in text
    assert "test \"${seen[backend_read_only_rootfs]}\" = 'true'" in text
    assert "test \"${seen[backend_privileged]}\" = 'false'" in text


def test_krc_tier1_workflow_validates_before_emitting_remote_output() -> None:
    text = _text()
    capture = 'out="$(ssh "${ssh_opts[@]}" "krcops@$KRC_TS_IP"'
    emit = "printf '%s\\n' \"$out\""
    validation = "test \"${seen[tier1_backend_status]}\" = 'PASS'"
    assert capture in text
    assert emit in text
    assert validation in text
    assert text.index(capture) < text.index(validation) < text.index(emit)
    assert "printf '%s\\n' \"$unexpected\"" not in text


def test_krc_tier1_workflow_rejects_unknown_missing_and_duplicate_keys() -> None:
    text = _text()
    assert "Unexpected Tier-1 output key" in text
    assert "Missing Tier-1 output key" in text
    assert "Duplicate Tier-1 output key" in text
    assert 'declare -A allowed=()' in text
    assert 'declare -A seen=()' in text
    assert 'test "${#seen[@]}" -eq "${#expected_keys[@]}"' in text


def test_krc_tier1_workflow_strictly_allows_sanitized_output_keys() -> None:
    text = _text()
    assert "P8_B_SECRET_VALUES=NOT_EXPOSED" in text
    for key in (
        "backend_type",
        "backend_present",
        "backend_running",
        "backend_status",
        "backend_image_digest",
        "backend_restart_count",
        "backend_loopback_only",
        "backend_port",
        "backend_user",
        "backend_read_only_rootfs",
        "backend_privileged",
        "backend_healthcheck_configured",
        "backend_health_status",
        "backend_memory_limit_configured",
        "backend_pids_limit_configured",
        "backend_cap_drop_configured",
        "backend_security_opt_configured",
        "tier1_backend_status",
    ):
        assert key in text


def test_krc_tier1_workflow_validates_all_output_value_domains() -> None:
    text = _text()
    required_checks = (
        "test \"${seen[backend_type]}\" = 'cobalt'",
        "test \"${seen[backend_present]}\" = 'yes'",
        "test \"${seen[backend_running]}\" = 'true'",
        "test \"${seen[backend_status]}\" = 'running'",
        "[[ \"${seen[backend_restart_count]}\" =~ ^[0-9]+$ ]]",
        "[[ \"${seen[backend_healthcheck_configured]}\" =~ ^(yes|no)$ ]]",
        "[[ \"${seen[backend_health_status]}\" =~ ^(none|starting|healthy|unhealthy)$ ]]",
        "[[ \"${seen[backend_memory_limit_configured]}\" =~ ^(yes|no)$ ]]",
        "[[ \"${seen[backend_pids_limit_configured]}\" =~ ^(yes|no)$ ]]",
        "[[ \"${seen[backend_cap_drop_configured]}\" =~ ^(yes|no)$ ]]",
        "[[ \"${seen[backend_security_opt_configured]}\" =~ ^(yes|no)$ ]]",
        "test \"${seen[tier1_backend_status]}\" = 'PASS'",
    )
    for check in required_checks:
        assert check in text


def test_krc_tier1_workflow_contains_required_negative_boundaries() -> None:
    text = _text()
    required = (
        "P8_B_ARBITRARY_ROOT=DENIED",
        "P8_B_TIER1_ARGUMENTS=DENIED",
        "P8_B_DIRECT_DOCKER_ACCESS=DENIED",
        "P8_B_OWNER_USER=DENIED",
        "P8_B_ROOT_USER=DENIED",
        "P8_B_KGM_ISOLATION=PASS",
        "P8_B_BACKEND_MUTATION=DENIED",
        "P8_B_TIER0_REGRESSION=PASS",
    )
    for marker in required:
        assert marker in text


def test_krc_tier1_workflow_has_no_mutation_surface() -> None:
    text = _text().lower()
    forbidden = (
        "systemctl restart",
        "systemctl stop",
        "systemctl start",
        "service restart",
        "docker restart",
        "docker exec",
        "docker compose",
        "docker pull",
        "docker rm",
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


def test_krc_tier1_workflow_records_terminal_gate() -> None:
    text = _text()
    assert "KRC_PHASE_8_P8_B_TIER1_OBSERVATION=PASS" in text
    assert "KRC_PHASE_8_OPERATION=TIER1_READ_ONLY" in text
