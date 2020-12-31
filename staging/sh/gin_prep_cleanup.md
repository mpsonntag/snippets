#!/usr/bin/env bash

set -eu

DIR_GINROOT=/home/sommer/Chaos/staging/gin

rm $DIR_GINROOT -r

echo "Removing gin user from groups"
usermod -G "" gin
echo "Removing user 'gin'"
userdel gin

echo "Removing group 'gindeploy'"
groupdel gindeploy
