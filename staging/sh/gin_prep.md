#!/usr/bin/env bash

set -eu

if [ $(getent group gindeploy) ]; then
  echo "group gindeploy already exists."
else
  groupadd gindeploy
fi

if id gin >/dev/null 2>&1; then
    echo "user gin already exists"
else
    useradd -M -G docker,gindeploy gin
    # Disable login for user gin
    usermod -L gin
fi

