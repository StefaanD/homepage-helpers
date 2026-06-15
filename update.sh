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
  -e PORT=8383 \
  -e CACHE_TTL=120 \
  -v /mnt/user/appdata/tautulli:/config \
  -e TAUTULLI_DB=/config/tautulli.db \
  -e TRACEARR_DB_HOST=192.168.66.5 \
  -e TRACEARR_DB_PORT=5432 \
  -e TRACEARR_DB_NAME=tracearr \
  -e TRACEARR_DB_USER=tracearr \
  -e TRACEARR_DB_PASSWORD=tracearr \
  -l homepage.group="Containers Rocinante" \
  -l homepage.icon="/icons/homepage-light.svg" \
  -l homepage.name="Homepage helpers" \
  -l homepage.description="Helper scripts for Homepage" \
  ghcr.io/stefaand/homepage-helpers:latest

echo "Done."