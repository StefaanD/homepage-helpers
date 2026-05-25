#!/bin/bash
set -e

echo "Updating homepage-helpers..."

cd /mnt/user/appdata/homepage-helpers

echo "Pulling latest code..."
git pull

echo "Building Docker image..."
docker build -t homepage-helpers .

echo "Stopping old container..."
docker rm -f homepage-helpers 2>/dev/null || true

echo "Starting new container..."
docker run -d \
  --name homepage-helpers \
  --restart unless-stopped \
  -p 8383:8383 \
  -v /mnt/user/appdata/tautulli:/config \
  -e TAUTULLI_DB=/config/tautulli.db \
  -e REMOVED=REMOVED \
  -e REMOVED=REMOVED \
  -e REMOVED=REMOVED \
  homepage-helpers

echo "Done."