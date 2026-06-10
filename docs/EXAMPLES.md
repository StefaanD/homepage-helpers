## Examples

This is a simple repo with helper scripts written for Homepage (https://gethomepage.dev/).

### 1. Tautulli

Below are two examples for the Tautulli stats, one with aggregated stats and once without aggregation, meaning amount per library.

For a description of the endpoint see [Tautulli provider](/docs/TAUTULLI.md).

An example Homepage widget with `aggregate=on` for this endpoint could look like shown below. In fact the call can have the `aggegrate=on` omitted since the default behaviour is that the result is returned aggregated.

```
- Plex statistics:
	icon: /icons/tautulli-light.svg
	href: https://plex.{{HOMEPAGE_VAR_DOMAIN_NAME_AND_PORT}}
	description: Media server
	siteMonitor: https://{{HOMEPAGE_VAR_SERVER_IP}}:32400
	widgets:
	- type: customapi
	  url: http://{{HOMEPAGE_VAR_SERVER_IP}}:8383/tautulli/stats?aggegrate=on
	  refreshInterval: 21600000 #6 hours
	  display: block
	  mappings:
		- label: Movies
		  field: movies
		- label: TV Shows
		  field: tvshows
		- label: Music albums
		  field: albums
```

![](/docs/images/tautulli_stats_aggregate_on.png)

And an example with `aggregate=off` could look like shown below. In this case we use `display=list` instead of `display=block` as the block setting for display has a limit of 4 fields in a widget.

```
    - Plex statistics aggregate=off:
        icon: /icons/tautulli-light.svg
        href: https://plex.{{HOMEPAGE_VAR_DOMAIN_NAME_AND_PORT}}
        description: Media server
        siteMonitor: https://{{HOMEPAGE_VAR_SERVER_IP}}:32400
        widgets:
        - type: customapi
          url: http://{{HOMEPAGE_VAR_SERVER_IP}}:8383/tautulli/stats?aggregate=off
          refreshInterval: 21600000 #6 hours
          display: list
          mappings:
            - field: "movies.Anime movies.movies"
              label: Anime movies
              format: number
            - field: "movies.Anime shorts.movies"
              label: Anime shorts
              format: number
            - field: movies.Movies.movies
              label: Movies
              format: number
            - field: shows.Anime.shows
              label: Anime shows
              format: number
            - field: shows.TV Shows.shows   
              label: TV shows
              format: number
            - field: music.Music.albums
              label: Music albums
              format: number
```

![](/docs/images/tautulli_stats_aggregate_off.png)

### 2. Unraid stats

The Unraid stats gets various statistics for an Unraid server, configured in the [Unraid stats configuration file](/queries/unraid_stats.json) configuration file.

For a description of the endpoint see [Unraid provider](/docs/UNRAID.md).

An example Homepage widget for the Unraid stats with the provided `/queries/unraid_stats.json` configuration file, could look like this;

```
Rocinante API:
  widget:
  type: customapi
  url: http://{{HOMEPAGE_VAR_SERVER_IP}}:8383/unraid/stats?url=http://{{HOMEPAGE_VAR_SERVER_IP}}/graphql&apikey={{HOMEPAGE_VAR_SERVER_API_KEY}}&csrftoken={{HOMEPAGE_VAR_SERVER_CSRF}}
  refreshInterval: 300000 #5 minutes
  display: list
  mappings:
- field: data.info.baseboard.manufacturer
  label: Motherboard manufacturer
- field: data.info.baseboard.model
  label: Motherboard model
- field: data.info.cpu.vendor
  label: CPU vendor
- field: data.info.cpu.brand
  label: CPU
  format: text
- field: data.info.cpu.cores
  label: CPU cores
- field: data.metrics.cpu.percentTotal
  label: CPU load
  format: float
  scale: 0.01
  suffix: "%"
- field: data.metrics.memory.total
  label: Memory total
  format: bytes
- field: data.metrics.memory.percentTotal
  label: Memory usage
  format: percent
- field: data.info.os.distro
  label: OS
- field: data.info.os.release
  label: OS version
- field: data.array.capacity.kilobytes.total
  label: Array total
  format: bytes
  scale: 1024
- field: data.array.capacity.kilobytes.free
  label: Array free
  format: bytes
  scale: 1024
```

![](/docs/images/unraid_stats.png)

As shown in the widget example the input parameters are stored in an environment file and are as follows;
* `HOMEPAGE_VAR_SERVER_IP` = IP adress or FQDN for the server to query
* `HOMEPAGE_VAR_SERVER_API_KEY` = the Unraid API key
* `HOMEPAGE_VAR_SERVER_CSRF` = the Unraid CSRF token

### 3. Unraid updates

The Unraid updates gets the availble Docker containers updates for the server and also uses a configuration file, see [Unraid updates configuration file](/queries/unraid_updates.json).

For a description of the endpoint see [Unraid provider](/docs/UNRAID.md).

An example Homepage widget for the Unraid stats could look like this;

```
- System:
    - Rocinante Docker updates status:
        icon: /icons/docker-light.svg
        widget:
          type: customapi
          url: http://{{HOMEPAGE_VAR_SERVER_IP}}:8383/unraid/updates?url=http://{{HOMEPAGE_VAR_SERVER_IP}}/graphql&apikey={{HOMEPAGE_VAR_SERVER_API_KEY}}&csrftoken={{HOMEPAGE_VAR_SERVER_CSRF}}
          refreshInterval: 3600000 #1 hour
          mappings:
            - field: count
              label: Updates
            - field: text
              label: Containers
```

![](/docs/images/unraid_updates.png)

As shown in the widget example the input parameters are stored in an environment file and are as follows;
* `HOMEPAGE_VAR_SERVER_IP` = IP adress or FQDN for the server to query
* `HOMEPAGE_VAR_SERVER_API_KEY` = the Unraid API key
* `HOMEPAGE_VAR_SERVER_CSRF` = the Unraid CSRF token

### 4. IPMI updates

The IPMI sensor statistics gets the values for the defined IPMI sensors as defined by it's configuration file, see [IPMI sensors configuration file](/queries/ipmi_sensors.json).

For a description of the endpoint see [Unraid provider](/docs/IPMI.md).

An example Homepage widget for the Unraid stats could look like this;

```
- Rocinante IPMI:
    icon: /icons/supermicro-light.svg
    href: http://{{HOMEPAGE_VAR_IPMI_IP}}
    widget:
        type: customapi
        url: http://{{HOMEPAGE_VAR_ROCINANTE_IP}}:8383/ipmi/sensors?host={{HOMEPAGE_VAR_IPMI_IP}}&username={{HOMEPAGE_VAR_IPMI_USER}}&password={{HOMEPAGE_VAR_IPMI_PASSWORD}}
        refreshInterval: 1800000 #0,5 hour
        display: list
        mappings:
            - field: temperatures.cpu
            label: CPU
            suffix: " °C"
            - field: temperatures.system
            label: System
            suffix: " °C"
            - field: fans.fan2
            label: FAN2
            suffix: " RPM"
            - field: fans.fan3
            label: FAN3
            suffix: " RPM"
            - field: fans.fan4
            label: FAN4
            suffix: " RPM"
            - field: fans.fan5
            label: FAN5
            suffix: " RPM"
```

![](/docs/images/ipmi_sensors.png)

As shown in the widget example the input parameters are stored in an environment file and are as follows;
* `HOMEPAGE_VAR_IPMI_IP` = IP adress where IPMI interface can be reached
* `HOMEPAGE_VAR_IPMI_USER` = username for the IPMI  interface
* `HOMEPAGE_VAR_IPMI_PASSWORD` = password for the IPMI interface
