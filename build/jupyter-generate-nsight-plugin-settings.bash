#!/bin/bash

JUPYTER_HOST="nsight-jupyter0-${BREV_ENV_ID}.brevlab.com"
NSIGHT_HTTP_URL="https://nsight-http0-${BREV_ENV_ID}.brevlab.com:8080"

cat << EOF
{
  "ui": {
    "enabled": true,
    "suppressServerAddressWarning": true,
    "host": "${JUPYTER_HOST}",
    "dockerHost": "${JUPYTER_HOST}",
    "defaultStreamerAddress": "${NSIGHT_HTTP_URL}"
  }
}
EOF
