#!/usr/bin/env bash

set -eu

echo "Removing gin user from groups"
usermod -G "" gin
echo "Removing user 'gin'"
userdel gin

echo "Removing group 'gindeploy'"
groupdel gindeploy
