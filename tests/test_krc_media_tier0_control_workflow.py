from hashlib import sha256
from pathlib import Path


WORKFLOW = Path(".github/workflows/krc-media-tier0-control.yml")
PHASE8C = Path("ops/krc-media/phase8c")
HELPER = PHASE8C / "krc-tier2-cobalt-restart"
SUDOERS = PHASE8C / "92-krcops-tier2-cobalt-restart"
BOOTSTRAP = PHASE8C / "bootstrap-tier2-restart.sh"
PINNED_TAILSCALE_ACTION = (
    "tailscale/github-action@306e68a486fd2350f2bfc3b19fcd143891a4a2d8"
)
EXPECTED_IMAGE_DIGEST = (
    "sha256:63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62"
)


def _text(path: Path = WORKFLOW) -> str:
    return path.read_text(encoding="utf-8")


def test_krc_control_workflow_is_manual_main_only_and_fails_closed() -> None:
    text = _text()
    assert "on:\n  workflow_dispatch:\n" in text
    assert "push:" not in text
    assert "pull_request:" not in text
    assert "schedule:" not in text
    assert 'test "$GITHUB_REPOSITORY" = \'kolemasakar/K_Research_Critic\'' in text
    assert 'test "$GITHUB_REF" = \'refs/heads/main\'' in text
    assert "Unauthorized operation" in text


def test_krc_control_workflow_exposes_only_three_explicit_modes() -> None:
    text = _text()
    assert "default: tier0" in text
    assert "type: choice" in text
    choices = [
        line.strip()
        for line in text.splitlines()
        if line.strip() in {"- tier0", "- tier1", "- tier2-restart"}
    ]
    assert choices[:3] == ["- tier0", "- tier1", "- tier2-restart"]


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


def test_krc_control_workflow_targets_exact_node_and_only_bounded_helpers() -> None:
    text = _text()
    assert "expected_host='krc-media-node1'" in text
    assert "expected_ip='100.118.132.8'" in text
    assert '"krcops@$KRC_TS_IP"' in text
    assert "sudo -n /usr/local/sbin/krc-tier0-status" in text
    assert "sudo -n /usr/local/sbin/krc-tier1-media-status" in text
    assert "sudo -n /usr/local/sbin/krc-tier2-cobalt-restart" in text


def test_krc_tier0_and_tier1_accepted_markers_are_retained() -> None:
    text = _text()
    for marker in (
        "KRC_PHASE_6_REPOSITORY_BOUNDARY=PASS",
        "KRC_PHASE_6_NODE_IDENTITY=PASS",
        "KRC_PHASE_6_TIER0_OBSERVATION=PASS",
        "KRC_PHASE_6_PROJECT_ISOLATED_OIDC_CONTROL=PASS",
        "KRC_PHASE_6_OPERATION=TIER0_READ_ONLY",
        "P8_B_REPOSITORY_BOUNDARY=PASS",
        "P8_B_NODE_IDENTITY=PASS",
        "P8_B_TIER1_STATUS=PASS",
        "P8_B_SECRET_VALUES=NOT_EXPOSED",
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
    ):
        assert marker in text


def test_krc_tier2_path_is_restart_only_and_regression_checked() -> None:
    text = _text()
    for marker in (
        "P8_C_REPOSITORY_BOUNDARY=PASS",
        "P8_C_NODE_IDENTITY=PASS",
        "P8_C_TIER1_PREFLIGHT=PASS",
        "P8_C_TIER2_RESTART=PASS",
        "P8_C_TIER1_REGRESSION=PASS",
        "P8_C_TIER0_REGRESSION=PASS",
        "P8_C_SECRET_VALUES=NOT_EXPOSED",
        "P8_C_ARBITRARY_ROOT=DENIED",
        "P8_C_TIER2_ARGUMENTS=DENIED",
        "P8_C_DIRECT_DOCKER_ACCESS=DENIED",
        "P8_C_OWNER_USER=DENIED",
        "P8_C_ROOT_USER=DENIED",
        "P8_C_KGM_ISOLATION=PASS",
        "KRC_PHASE_8_P8_C_BOUNDED_RESTART=PASS",
        "KRC_PHASE_8_OPERATION=TIER2_COBALT_RESTART_ONLY",
    ):
        assert marker in text
    assert text.count(
        "'sudo -n /usr/local/sbin/krc-tier2-cobalt-restart'"
    ) == 1


def test_workflow_contains_no_direct_backend_mutation_commands() -> None:
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
        "sudo -n bash",
        "sudo -n sh",
    )
    for token in forbidden:
        assert token not in text


def test_phase8c_helper_pins_exact_backend_and_single_restart_mutation() -> None:
    text = _text(HELPER)
    assert "CONTAINER='krc-cobalt'" in text
    assert EXPECTED_IMAGE_DIGEST in text
    assert "ghcr.io/imputnet/cobalt@" + EXPECTED_IMAGE_DIGEST in text
    exact_restart = '"$DOCKER" restart --time 10 "$CONTAINER" >/dev/null'
    assert text.count(exact_restart) == 1
    for token in ("docker exec", "docker pull", "docker rm", "docker stop"):
        assert token not in text.lower()
    assert "arguments are not accepted" in text
    assert "backend_loopback_only_after=yes" in text
    assert "backend_read_only_rootfs_after=true" in text
    assert "backend_privileged_after=false" in text
    assert "tier2_restart_status=PASS" in text


def test_phase8c_sudoers_is_digest_pinned_and_no_argument_only() -> None:
    helper_bytes = HELPER.read_bytes()
    digest = sha256(helper_bytes).hexdigest()
    rule = _text(SUDOERS).strip()
    assert rule == (
        "krcops ALL=(root) NOPASSWD: "
        f"sha256:{digest} /usr/local/sbin/krc-tier2-cobalt-restart \"\""
    )


def test_phase8c_bootstrap_installs_capability_without_triggering_restart() -> None:
    text = _text(BOOTSTRAP)
    assert "visudo -cf" in text
    assert "visudo -c" in text
    assert "install -o root -g root -m 0755" in text
    assert "install -o root -g root -m 0440" in text
    assert "unexpected-argument" in text
    assert "sudo -n /usr/bin/id -u" in text
    assert "docker restart" not in text.lower()
    assert "KRC_PHASE_8_P8_C_HOST_BOOTSTRAP=APPLIED" in text
