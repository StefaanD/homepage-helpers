#!/bin/bash
set -e

cd /mnt/user/appdata/homepage-helpers

echo "Pulling latest code..."
git pull

./update.sh