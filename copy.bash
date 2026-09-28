#!/bin/bash

source .env

BACKUP_FILE="$1"

scp -i "$SSH_KEY" "$BACKUP_FILE" "$SSH_USER@$SSH_HOST:$REMOTE_BACKUP_DIR"

