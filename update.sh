#!/bin/bash
cd /mnt/user/appdata/homepage-helpers
git pull
docker build -t homepage-helpers .
docker rm -f homepage-helpers
docker run -d \
  --name homepage-helpers \
  --restart unless-stopped \
  -p 8383:8383 \
  -v /mnt/user/appdata/tautulli:/config \
  -e TAUTULLI_DB=/config/tautulli.db \
  homepage-helpers