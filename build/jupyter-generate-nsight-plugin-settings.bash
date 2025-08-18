#!/bin/bash

EXTERNAL_IP=$(curl -sSL https://ipecho.net/plain)

cat << EOF
{
  "ui": {
    "enabled": true,
    "suppressServerAddressWarning": true,
    "host": "${EXTERNAL_IP}",
    "dockerHost": "${EXTERNAL_IP}",
    "defaultStreamerAddress": "http://${EXTERNAL_IP}:8080"
  }
}
EOF
