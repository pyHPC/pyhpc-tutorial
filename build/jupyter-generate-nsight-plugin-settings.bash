#!/bin/bash

EXTERNAL_IP=$(curl https://ipecho.net/plain)

cat << EOF
{
  "ui": {
    "enabled": true,
    "suppressServerAddressWarning": true,
    "host": "${EXTERNAL_IP}",
    "dockerHost": "${EXTERNAL_IP}",
    "defaultStreamerAddress": "${EXTERNAL_IP}"
  },
  "nsys": {
    "installationPath": "/usr/local/cuda",
    "args": "--trace=cuda,nvtx,osrt --python-sampling=true --python-backtrace=cuda --cudabacktrace=all"
  },
  "ncu": {
    "installationPath": "/usr/local/cuda"
  }
}
EOF

