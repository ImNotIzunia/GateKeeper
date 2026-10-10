#!/bin/bash

set -euo pipefail

DEST="$REMOTE_BASE_DIR/$(date +%Y)/$(date +%m)"

ASKPASS=$(mktemp); chmod 700 "$ASKPASS"
echo 'echo "$SSH_PASSPHRASE"' > "$ASKPASS"
eval "$(ssh-agent -s)" >/dev/null
trap 'ssh-agent -k >/dev/null; rm -f "$ASKPASS"' EXIT
SSH_ASKPASS="$ASKPASS" SSH_ASKPASS_REQUIRE=force DISPLAY=:0 ssh-add "$SSH_KEY" </dev/null

ssh -o StrictHostKeyChecking=accept-new "$SSH_USER@$REMOTE_HOST" "mkdir -p '$DEST'"
scp -o StrictHostKeyChecking=accept-new "$@" "$SSH_USER@$REMOTE_HOST:$DEST/"

