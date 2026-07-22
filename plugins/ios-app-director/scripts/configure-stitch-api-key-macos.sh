#!/usr/bin/env bash

set -euo pipefail

usage() {
  printf 'Usage: %s [--clear]\n' "$(basename "$0")"
}

if [[ "$(uname -s)" != "Darwin" ]]; then
  printf 'This helper configures the environment inherited by macOS desktop apps.\n' >&2
  exit 1
fi

if [[ "${1:-}" == "--clear" ]]; then
  launchctl unsetenv STITCH_API_KEY
  printf 'Cleared STITCH_API_KEY for the current macOS login session.\n'
  printf 'Fully quit and reopen Codex Desktop before testing Stitch again.\n'
  exit 0
fi

if [[ $# -ne 0 ]]; then
  usage >&2
  exit 2
fi

printf 'Create a key first at https://stitch.withgoogle.com/settings\n'
printf 'Paste your Stitch API key (input is hidden): '
IFS= read -r -s stitch_api_key </dev/tty
printf '\n'

if [[ -z "$stitch_api_key" ]]; then
  printf 'No key was entered; nothing changed.\n' >&2
  exit 1
fi

if [[ "$stitch_api_key" =~ [[:space:]] ]]; then
  unset stitch_api_key
  printf 'The key contains whitespace; nothing changed. Copy it again from Stitch Settings.\n' >&2
  exit 1
fi

launchctl setenv STITCH_API_KEY "$stitch_api_key"
unset stitch_api_key

printf 'Configured STITCH_API_KEY for the current macOS login session.\n'
printf 'Fully quit and reopen Codex Desktop, then start a new task.\n'
printf 'Do not use the generic OAuth Authenticate action for Stitch.\n'
