# Homepage Helpers

![Release](https://img.shields.io/github/v/release/StefaanD/homepage-helpers)
![Docker Pulls](https://img.shields.io/badge/docker-ghcr.io-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/github/license/StefaanD/homepage-helpers)

This is a simple repo with helper scripts written for Homepage (https://gethomepage.dev/).

## 1. Preface

Some remarks and warnings upfront to make some things clear;

* English is not my mother language, so bear with me and you can always contact me when you see obvious faults/spelling mistakes/issues in the text.
* Yes big parts are written with the help of AI, i'm no developer so needed some help to get this project of the ground. Off course i don't take what AI suggests blindly and always check the code it has written.
* The main reason this project ever came to life was that some application API's are good but don't always provided me with the endpoint(s) i needed or gave such a vast output, looking at you Sonarr /api/v3/series 😉
* I'm not a programmer or at least i will not call myself one not even by a long shot. I do dabble in scripting from time to time but not more than that. Having said that it should be clear that great parts of the code in this project has been created with the help of AI.
* If you find issues in the code, or want to make feature requests then be patient with me as I might be slow to respond, all-in-all this is a hobby project so please treat it as such.
* I know this homepage helper scripts is something very niche, so interest might be very low and i have no problems with that.

## 2. Project intro

This project provides custom Homepage helper APIs for Unraid homelabs, but can be used on other platforms as well.

## 3. Features

- Tautulli statistics
- Tracearr statistics
- Unraid GraphQL helpers
- IPMI sensor monitoring
- Docker healthchecks
- Homepage customapi support

## 4. Structure

So basically at the heart of the Homepage Helpers is Python and the whole project is structured as follows;
```
homepage-helpers/
├── app.py
├── config_manager.py
├── config/
│   ├── ipmi_sensors.json±
│   ├── unraid_stats.json
│   ├── unraid_updates.json
│   └── tracearr_configuration.json
├── providers/
│   ├── ipmi.py
│   ├── tautulli.py
│   ├── tracearr.py
│   ├── unraid.py
│   └── ...
├── requirements.txt
├── Dockerfile
└── README.md
```

1. The main script is `app.py` and there are provider scripts for several tools or Docker containers under `providers`.

2. The `providers` folder—as said under point 1—contains Python scripts and provide one or more endpoints and are bound to a specific OS (in my case Unraid) or Docker container.

3. The `queries` folder is where json files are stored and are used by the provider script to read what needs to be fetched, so basically these are configuration files. As such these json files should provide some flexibility if one wants to use different fields or get more statistics from the provider.

4. The script `config_manager.py` ensures the configuration files for the providers are available.

## 5. Endpoints

| Endpoint | Description |
|---|---|
| /health | Container health |
| /ipmi/sensors | IPMI sensor readings |
| /tautulli/stats | Tautulli library statistics |
| /tracearr/resolutions/movies | Movies resolution breakdown, fetched from Plex, Emby or Jellyfin |
| /tracearr/resolutions/tv | TV resolution breakdown |
| /tracearr/video_codecs | Video codecs breakdown for all movie and TV libraries |
| /tracearr/audio_codecs | Audio codecs breakdown for all movie and TV libraries |
| /tracearr/audio_channels | Audio channels breakdown for all movie and TV libraries |
| /tracearr/stats | General statistics as shown Library -> Overview in the Tracearr dashboard |
| /tracearr/history/countries | Breakdown on country leve used to play media files |
| /tracearr/history/devices | Breakdown on device level used to play media files |
| /tracearr/history/platforms | Breakdown on platform level used to play media files |
| /tracearr/history/users | Breakdown on user level used to play media files |
| /tracearr/history/stats | Watch statistics as shown under Library -> Watch in the Tracearr dashboard |
| /unraid/stats | Unraid GraphQL stats |
| /unraid/updates | Docker update status |

## 6. Main script

The main script `app.py` just register the blueprint for all available providers and only has one route itself under `\`

So each provider handles it's own routes to provide the endpoints as described under 5. Endpoints

The docker container which is created uses the port 8383 for it's own API endpoints, but you can use an .env file, see [.env.example](docs/.env.example) to set some standard values like the port, Tautulli database location or caching duration. Or in case of using the container on Unraid, edit the template values.

## 9. Installation

Installation on system other than Unraid can be done with the following docker run command;
```
docker run -d \
  --name homepage-helpers \
  --restart unless-stopped \
  -p 8383:8383 \
  -e PORT=8383 \
  -e CACHE_TTL=120 \
  -v /mnt/user/appdata/tautulli:/config \
  -e TAUTULLI_DB=/config/tautulli.db \
  -v /mnt/user/appdata/homepage-helpers:/config \
  -e TRACEARR_CONFIG=/config/tracearr_configuration.json \
  -e TRACEARR_DB_HOST=tracearr-db \
  -e TRACEARR_DB_PORT=5432 \
  -e TRACEARR_DB_NAME=tracearr \
  -e TRACEARR_DB_USER=tracearr \
  -e TRACEARR_DB_PASSWORD=tracearr \
  -e UNRAID_URL=http://192.168.1.1/graphql \
  -e UNRAID_API_KEY=[YOUR_UNRAID_API_KEY] \
  -e UNRAID_CSRF_TOKEN=[YOUR_UNRAID_CSRF_KEY] \
  -e IPMI_SENSOR_HOST=192.168.1.5 \
  -e IPMI_SENSOR_USERNAME=[YOUR_IPMI_USERNAME] \
  -e IPMI_SENSOR_PASSWORD=[YOUR_IPMI_PASSWORD] \
  -e LOG_LEVEL=INFO \
  -e LOG_MAX_SIZE=10485760 \
  -e LOG_BACKUP_COUNT=5 \
  ghcr.io/stefaand/homepage-helpers:latest
```

## 8. Available providers

- [IPMI](docs/IPMI.md)
- [Tautulli](docs/TAUTULLI.md)
- [Tracearr](docs/TRACEARR.md)
- [Unraid](docs/UNRAID.md)

## 9. Examples

Examples are divided per provider
- [Examples IPMI](docs/EXAMPLES_IPMI.md)
- [Examples Tautulli](docs/EXAMPLES_TAUTULLI.md)
- [Examples Tracearr](docs/EXAMPLES_TRACEARR.md)
- [Examples Unraid](docs/EXAMPLES_UNRAID.md)

## 10. Planned providers

### High priority

* ~~Vaultwarden~~ (unfortunaly no public API, only a CLI API)
* Firefly III
* Zerobyte (Restic frontend)
* Tracearr **(implemented in 0.2.0)**

### Existing provider enhancements

* Clean up of IPMI provider and more statistics
* Unraid disk statistics
* Unraid VM statistics
* Unraid Docker statistics
* Tautulli library breakdown
* Tracearr status, storage, weekly/daily breakdown and growth 

### Future providers

* Authelia
* Additional backup solutions
* Additional self-hosted finance solutions