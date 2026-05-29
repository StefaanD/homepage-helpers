#!/bin/bash
set -e

cd /mnt/user/appdata/homepage-helpers

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
  -l homepage.group="Containers Rocinante" \
  -l homepage.icon="/icons/homepage-light.svg" \
  -l homepage.name="Homepage helpers" \
  -l homepage.description="Helper scripts for Homepage" \
  homepage-helpers

echo "Done."