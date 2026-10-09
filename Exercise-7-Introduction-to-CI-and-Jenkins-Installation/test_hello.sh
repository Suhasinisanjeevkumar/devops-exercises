#!/bin/sh
set -eu

expected='Hello from Exercise 7 CI!'
actual=$(sh ./hello.sh)

if [ "$actual" = "$expected" ]; then
    printf '%s\n' 'PASS: hello.sh printed the expected message.'
else
    printf '%s\n' 'FAIL: hello.sh did not print the expected message.' >&2
    printf 'Expected: <%s>\n' "$expected" >&2
    printf 'Actual:   <%s>\n' "$actual" >&2
    exit 1
fi
