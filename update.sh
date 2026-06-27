#!/bin/bash
set -e

echo "Building Docker image..."
docker build -t homepage-helpers .

echo "Stopping old container..."
docker rm -f homepage-helpers 2>/dev/null || true

echo "Starting new container..."
docker run -d \
  --name homepage-helpers \
  --restart unless-stopped \
  --net "tracearr-stack_tracearr-network" \
  -p 8383:8383 \
  -e PORT=8383 \
  -e CACHE_TTL=120 \
  -v /Users/stefaan/docker/appdata/homepage-helpers:/config \
  -e TRACEARR_CONFIG=/config/tracearr_configuration.json \
  -e TRACEARR_DB_HOST=tracearr-db \
  -e TRACEARR_DB_PORT=5432 \
  -e TRACEARR_DB_NAME=tracearr \
  -e TRACEARR_DB_USER=tracearr \
  -e TRACEARR_DB_PASSWORD=tracearr \
  -e UNRAID_URL=http://192.168.66.5/graphql \
  -e UNRAID_API_KEY=bd22d43bb07eaaa6b0960c859d7eb390b60e5f7dd9dadfdfeb6c384aae284ad8 \
  -e UNRAID_CSRF_TOKEN=BFA408151DE138A7 \
  -e IPMI_SENSOR_HOST=192.168.66.35 \
  -e IPMI_SENSOR_USERNAME=ADMIN \
  -e IPMI_SENSOR_PASSWORD=QENETJNRES \
  -e LOG_LEVEL=INFO \
  -e LOG_MAX_SIZE=10485760 \
  -e LOG_BACKUP_COUNT=5 \
  -l homepage.group="Containers Rocinante" \
  -l homepage.icon="/icons/homepage-light.svg" \
  -l homepage.name="Homepage helpers" \
  -l homepage.description="Helper scripts for Homepage" \
  homepage-helpers

echo "Done."