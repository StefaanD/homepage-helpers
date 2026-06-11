# Homepage Helpers

![Release](https://img.shields.io/github/v/release/StefaanD/homepage-helpers)
![Docker Pulls](https://img.shields.io/badge/docker-ghcr.io-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/github/license/StefaanD/homepage-helpers)

This is a simple repo with helper scripts written for Homepage (https://gethomepage.dev/).

## 1. Preface

Some remarks and warnings upfront to make some things clear;

* English is not my mother language, so bear with me and you can always contact me when you see obvious faults/spelling mistakes/issues in the text.
* The main reason this project ever came to life was that some application API's are good but don't always provided me with the endpoint(s) i needed or gave such a vast output, looking at you Sonarr /api/v3/series :-)
* I'm not a programmer or at least i will not call myself one not even by a long shot. I do dabble in scripting from time to time but not more than that. Having said that it should be clear that great parts of the code in this project has been created with the help of AI.
* If you find issues in the code, or want to make feature requests then be patient with me as I might be slow to respond, all-in-all this is a hobby project so please treat it as such.
* I know this homepage helper scripts is something very niche, so interest might be very low and i have no problems with that.

## 2. Project intro

This project provides custom Homepage helper APIs for Unraid homelabs, but can be used on other platforms as well.

## 3. Features

- Tautulli statistics
- Unraid GraphQL helpers
- IPMI sensor monitoring
- Docker healthchecks
- Homepage customapi support

## 4. Structure

So basically at the heart of the Homepage Helpers is Python and the whole project is structured as follows;
```
homepage-helpers/
├── app.py
├── providers/
│   ├── tautulli.py
│   ├── unraid.py
│   ├── ipmi.py
│   └── ...
├── queries/
│   ├── unraid_stats.json
│   ├── unraid_updates.json
│   └── ipmi_sensors.json
├── requirements.txt
├── Dockerfile
├── update.sh
└── README.md
```

1. The main script is `app.py` and there are provider scripts for several tools or Docker containers under `providers`.

2. The `providers` folder—as said under point 1—contains Python scripts performing one or more tasks and are bound to a specific OS (in my case Unraid) or Docker container.

3. The `queries` folder is where json files are stored and are used by the provider script to read what needs to be fetched, so basically these are configuration files. As such these json files should provide some flexibility if one wants to use different fields or get more statistics from the provider.

## 5. Endpoints

| Endpoint | Description |
|---|---|
| /health | Container health |
| /tautulli/stats | Tautulli library statistics |
| /unraid/stats | Unraid GraphQL stats |
| /unraid/updates | Docker update status |
| /ipmi/sensors | IPMI sensor readings |

## 6. Main script

The main script `app.py` calls application routes to the available providers. So when adding a new provider also a call to that provider needs to be added, for example;
```
@app.route("/unraid/stats")
def unraid_stats():
    url = request.args.get("url")
    api_key = request.args.get("apikey")
    csrf_token = request.args.get("csrftoken")

    return jsonify(
        unraid.get_stats(url, api_key, csrf_token)
    )
```

The docker container which is created uses the port 8383 for well it's own API you might call it, but you can use an .env file, see [.env.example](docs/.env.example) to set some standard values like the port, Tautulli database location or caching duration. Or in case of using the container on Unraid, edit the template values.

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
  ghcr.io/stefaand/homepage-helpers:latest
```

## 8. Providers

- [Tautulli](docs/TAUTULLI.md)
- [Unraid](docs/UNRAID.md)
- [IPMI](docs/IPMI.md)

## 9. Examples

Examples can be found at [Examples](docs/EXAMPLES.md)

## 10. Planned providers

### High priority

* Vaultwarden
* Firefly III
* Zerobyte

### Existing provider enhancements

* Unraid disk statistics
* Unraid VM statistics
* Unraid Docker statistics
* Tautulli library breakdown

### Future providers

* Authelia
* Additional backup solutions
* Additional self-hosted finance solutions