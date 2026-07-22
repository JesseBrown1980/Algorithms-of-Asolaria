#!/usr/bin/env bash
set -euo pipefail

# Fetch the English-only 10,000,000,000-byte enwik10 archive through the
# stable Yandex public-resource API. The signed download URL is intentionally
# resolved at run time because it expires.

target_dir="${1:-/mnt/d/asolaria-e10-20260719/corpus}"
archive="${target_dir}/enwik10.7z"
partial="${archive}.part"
public_key="https://yadi.sk/d/2wVOWD7u3r1NRA"
api="https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key=${public_key}"
expected_size=1901467779
expected_sha256="7d2bcda3cbe1db6620b0e1bd6bb974c780de58c6a5770750ceb206b44e5b8b72"

mkdir -p "${target_dir}"

verify_archive() {
    local candidate="$1"
    local actual_size actual_sha256
    actual_size="$(stat -c %s "${candidate}")"
    actual_sha256="$(sha256sum "${candidate}" | awk '{print $1}')"
    printf 'E10_ARCHIVE|path=%s|bytes=%s|sha256=%s\n' \
        "${candidate}" "${actual_size}" "${actual_sha256}"
    [[ "${actual_size}" == "${expected_size}" && "${actual_sha256}" == "${expected_sha256}" ]]
}

if [[ -f "${archive}" ]] && verify_archive "${archive}"; then
    printf 'E10_FETCH|status=already-verified\n'
    exit 0
fi

download_url="$({
    curl --fail --silent --show-error --location --retry 5 --retry-all-errors "${api}"
} | python3 -c 'import json, sys; print(json.load(sys.stdin)["href"])')"

curl --fail --silent --show-error --location \
    --retry 10 --retry-all-errors --connect-timeout 30 \
    --continue-at - --output "${partial}" "${download_url}"

if ! verify_archive "${partial}"; then
    printf 'E10_FETCH|status=HOLD|reason=archive-size-or-sha256-mismatch\n' >&2
    exit 1
fi

mv -f "${partial}" "${archive}"
printf 'E10_FETCH|status=verified|path=%s\n' "${archive}"
