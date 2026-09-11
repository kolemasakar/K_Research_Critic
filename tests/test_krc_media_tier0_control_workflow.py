from pathlib import Path


WORKFLOW = Path(".github/workflows/krc-media-tier0-control.yml")
PINNED_TAILSCALE_ACTION = (
    "tailscale/github-action@306e68a486fd2350f2bfc3b19fcd143891a4a2d8"
)


def _text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def test_krc_control_workflow_is_manual_main_only_and_fails_closed() -> None:
    text = _text()
    assert "on:\n  workflow_dispatch:\n" in text
    assert "push:" not in text
    assert "pull_request:" not in text
    assert "schedule:" not in text
    assert "test \"$GITHUB_REPOSITORY\" = 'kolemasakar/K_Research_Critic'" in text
    assert "test \"$GITHUB_REF\" = 'refs/heads/main'" in text
    assert "if: github.repository" not in text


def test_krc_control_workflow_exposes_only_bounded_authorized_modes() -> None:
    text = _text()
    assert "operation:" in text
    assert "default: tier0" in text
    assert "type: choice" in text
    assert "- tier0" in text
    assert "- tier1" in text
    assert "- tier2_restart" in text
    assert "Unauthorized operation" in text


def test_krc_control_workflow_preserves_trusted_oidc_identity_path() -> None:
    text = _text()
    assert WORKFLOW.as_posix() == ".github/workflows/krc-media-tier0-control.yml"
    assert "name: KRC MEDIA Tier-0 Tailscale Control" in text
    assert "permissions:\n  id-token: write\n" in text
    assert "contents: read" not in text
    assert "actions/checkout" not in text
    assert "TS_KRC_OAUTH_CLIENT_ID" in text
    assert "TS_KRC_AUDIENCE" in text
    assert "tags: tag:krc-media-github-actions" in text
    assert "tags: tag:github-actions" not in text
    assert PINNED_TAILSCALE_ACTION in text
    assert "tailscale/github-action@v4" not in text


def test_krc_control_workflow_targets_exact_node_and_bounded_helpers() -> None:
    text = _text()
    assert "expected_host='krc-media-node1'" in text
    assert "expected_ip='100.118.132.8'" in text
    assert '"krcops@$KRC_TS_IP"' in text
    assert "sudo -n /usr/local/sbin/krc-tier0-status" in text
    assert "sudo -n /usr/local/sbin/krc-tier1-media-status" in text
    assert "sudo -n /usr/local/sbin/krc-tier2-media-restart" in text
    assert "KRC_TIER0_STATUS_VERSION=1" in text
    assert "backend_type" in text
    assert "tier1_backend_status" in text
    assert "P8_C_RESTART_VERSION" in text
    assert "tier2_restart_status" in text


def test_krc_tier0_path_retains_sanitized_allowlist_and_phase6_markers() -> None:
    text = _text()
    assert "Unexpected Tier-0 output key(s)" in text
    for key in (
        "KRC_TIER0_STATUS_VERSION",
        "timestamp_utc",
        "hostname",
        "kernel",
        "architecture",
        "cpu_count",
        "loadavg",
        "mem_total_kib",
        "mem_available_kib",
        "swap_total_kib",
        "root_fs",
        "tailscaled",
        "ssh",
        "docker",
        "rpcbind",
        "tailscale_ipv4",
        "tcp_listeners",
    ):
        assert key in text

    required = (
        "KRC_PHASE_6_REPOSITORY_BOUNDARY=PASS",
        "KRC_PHASE_6_NODE_IDENTITY=PASS",
        "KRC_PHASE_6_TIER0_OBSERVATION=PASS",
        "KRC_PHASE_6_ARBITRARY_ROOT=DENIED",
        "KRC_PHASE_6_HELPER_ARGUMENT_INJECTION=DENIED",
        "KRC_PHASE_6_DOCKER_ACCESS=DENIED",
        "KRC_PHASE_6_OWNER_USER=DENIED",
        "KRC_PHASE_6_ROOT_USER=DENIED",
        "KRC_PHASE_6_KGM_TCP22_ISOLATION=PASS",
        "KRC_PHASE_6_PROJECT_ISOLATED_OIDC_CONTROL=PASS",
        "KRC_PHASE_6_OPERATION=TIER0_READ_ONLY",
    )
    for marker in required:
        assert marker in text


def test_krc_tier1_path_validates_before_emit_and_rejects_duplicate_keys() -> None:
    text = _text()
    assert "expected_keys=(" in text
    assert "declare -A seen=()" in text
    assert "Malformed Tier-1 output" in text
    assert "Unexpected Tier-1 output key" in text
    assert "Duplicate Tier-1 output key" in text
    assert "Missing Tier-1 output key" in text
    assert "P8_B_SECRET_VALUES=NOT_EXPOSED" in text

    validate_pos = text.index("expected_keys=(")
    emit_pos = text.index("printf '%s\\n' \"$out\"", validate_pos)
    assert validate_pos < emit_pos


def test_krc_tier1_path_pins_current_backend_identity_and_boundaries() -> None:
    text = _text()
    assert (
        "backend_image_digest]}\" = 'sha256:"
        "63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62'"
    ) in text
    assert "backend_loopback_only]}\" = 'yes'" in text
    assert "backend_port]}\" = '9000'" in text
    assert "backend_user]}\" = 'node'" in text
    assert "backend_read_only_rootfs]}\" = 'true'" in text
    assert "backend_privileged]}\" = 'false'" in text

    required = (
        "P8_B_REPOSITORY_BOUNDARY=PASS",
        "P8_B_NODE_IDENTITY=PASS",
        "P8_B_TIER1_STATUS=PASS",
        "P8_B_ARBITRARY_ROOT=DENIED",
        "P8_B_TIER1_ARGUMENTS=DENIED",
        "P8_B_DIRECT_DOCKER_ACCESS=DENIED",
        "P8_B_OWNER_USER=DENIED",
        "P8_B_ROOT_USER=DENIED",
        "P8_B_KGM_ISOLATION=PASS",
        "P8_B_TIER0_REGRESSION=PASS",
        "P8_B_BACKEND_MUTATION=DENIED",
        "KRC_PHASE_8_P8_B_TIER1_OBSERVATION=PASS",
        "KRC_PHASE_8_OPERATION=TIER1_READ_ONLY",
    )
    for marker in required:
        assert marker in text


def test_krc_tier2_restart_is_exact_bounded_and_regression_checked() -> None:
    text = _text()
    required = (
        "P8_C_REPOSITORY_BOUNDARY=PASS",
        "P8_C_NODE_IDENTITY=PASS",
        "P8_C_PRECHECK=PASS",
        "P8_C_BACKEND_IDENTITY=PASS",
        "P8_C_RESTART=PASS",
        "P8_C_SECRET_VALUES=NOT_EXPOSED",
        "P8_C_POSTCHECK=PASS",
        "P8_C_TIER1_REGRESSION=PASS",
        "P8_C_ARBITRARY_ROOT=DENIED",
        "P8_C_ARGUMENTS=DENIED",
        "P8_C_DIRECT_DOCKER_ACCESS=DENIED",
        "P8_C_OWNER_USER=DENIED",
        "P8_C_ROOT_USER=DENIED",
        "P8_C_KGM_ISOLATION=PASS",
        "P8_C_TIER0_REGRESSION=PASS",
        "KRC_PHASE_8_P8_C_RESTART_ONLY=PASS",
        "KRC_PHASE_8_OPERATION=TIER2_RESTART_ONLY",
    )
    for marker in required:
        assert marker in text

    assert "expected_restart_keys=(" in text
    assert "Duplicate Tier-2 restart output key" in text
    assert "Missing Tier-2 restart output key" in text
    assert "backend_identity_verified" in text
    assert "pre_restart_running" in text
    assert "post_restart_running" in text
    assert "post_restart_identity_verified" in text
    assert "restart_requested" in text


def test_krc_workflow_has_no_direct_mutation_surface() -> None:
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
