from pathlib import Path


HELPER = Path("ops/krc_media/p8c/krc-tier2-media-restart")
SUDOERS = Path("ops/krc_media/p8c/92-krcops-tier2-media-restart")
PINNED_IMAGE = (
    "ghcr.io/imputnet/cobalt@sha256:"
    "63186dd68afd57ce3bb1f62cc4c139f5fa95b9c3e87a3cf5c6e4c7a570523f62"
)


def test_tier2_restart_helper_is_fail_closed_and_identity_pinned() -> None:
    text = HELPER.read_text(encoding="utf-8")
    assert "set -Eeuo pipefail" in text
    assert '[ "$#" -ne 0 ]' in text
    assert PINNED_IMAGE in text
    assert "9000/tcp -> 127.0.0.1:9000" in text
    assert "EXPECTED_USER='node'" in text
    assert "ReadonlyRootfs" in text
    assert "Privileged" in text
    assert '[ "${#matches[@]}" -eq 1 ]' in text
    assert "/usr/bin/docker" in text


def test_tier2_restart_helper_exposes_only_restart_mutation() -> None:
    text = HELPER.read_text(encoding="utf-8").lower()
    assert "$docker restart --time 10" in text
    forbidden = (
        "$docker start",
        "$docker stop",
        "$docker exec",
        "$docker pull",
        "$docker rm",
        "$docker run",
        "docker compose",
        "systemctl",
        "service ",
        "apt-get",
        "apt install",
        "chmod ",
        "chown ",
        "sed -i",
        "tee ",
        "rm -",
        "mv ",
        "cp ",
        ".env",
        "keys.json",
        "docker logs",
    )
    for token in forbidden:
        assert token not in text


def test_tier2_restart_helper_emits_only_sanitized_fixed_schema() -> None:
    text = HELPER.read_text(encoding="utf-8")
    for key in (
        "P8_C_RESTART_VERSION=1",
        "backend_type=cobalt",
        "backend_identity_verified=yes",
        "pre_restart_running=true",
        "restart_requested=yes",
        "post_restart_running=true",
        "post_restart_identity_verified=yes",
        "tier2_restart_status=PASS",
    ):
        assert key in text


def test_tier2_sudoers_allows_only_exact_no_argument_helper() -> None:
    text = SUDOERS.read_text(encoding="utf-8")
    assert text == (
        'krcops ALL=(root) NOPASSWD: '
        '/usr/local/sbin/krc-tier2-media-restart ""\n'
    )
