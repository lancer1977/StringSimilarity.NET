#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

configuration="${CONFIGURATION:-Release}"
target="${VALIDATION_TARGET:-F23.StringSimilarity.sln}"

cd "${repo_root}"

dotnet test "${target}" --configuration "${configuration}" "$@"
