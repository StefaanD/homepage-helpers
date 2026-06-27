## Unraid

As stated in Readme file, i use Unraid OS to run my Homepage docker and also here the default widget didn't provide my what i actually wanted to show on my homepage.

This provider makes use of the Unraid API, for more information see the [Using the Unraid API](https://docs.unraid.net/API/how-to-use-the-api/) documentation.

This provider currently serves two endpoints;
* `/unraid/stats` (Basic hardware stats for the machine)
* `/unraid/updates` (Checks if there are Docker container updates)
And needs the following environment variables;
* `UNRAID_URL` the host IP address of FQDN
* `UNRAID_API_KEY` the Unraid API key
* `UNRAID_CSRF_TOKEN` the Unraid CSRF token

### 1. Provider - Unraid stats

Endpoint for this is `/unraid/stats`.

This endpoint uses the `/queries/unraid_stats.json` file to set the query executed against Unraid's API. The file can be found in the `config` folder.

In my configuration the Unraid GraphQL query looks like this;
```
{
  "query": "query { array { state capacity { kilobytes { total free } } disks { name size status temp } } metrics { cpu { percentTotal } memory { total percentTotal } } info { baseboard { manufacturer model } cpu { brand cores vendor } os { release distro } system { manufacturer model } } internalBootContext { poolNames shareNames } }"
}
```

So it gets information about the motherboard, CPU, memory, OS and version, disks in the array, pool names, shares and the array size and free space. For one of my Unraid servers the output looks like this;
```
{
   "data": {
      "array": {
         "capacity": {
            "kilobytes": {
               "free": "52824999568",
               "total": "89990354430"
            }
         },
         "disks": [
            {
               "name": "disk1",
               "size": 17578328012,
               "status": "DISK_OK",
               "temp": null
            },
            {
               "name": "disk2",
               "size": 17578328012,
               "status": "DISK_OK",
               "temp": 43
            },
            {
               "name": "disk3",
               "size": 17578328012,
               "status": "DISK_OK",
               "temp": null
            },
            {
               "name": "disk4",
               "size": 17578328012,
               "status": "DISK_OK",
               "temp": null
            },
            {
               "name": "disk5",
               "size": 17578328012,
               "status": "DISK_OK",
               "temp": null
            }
         ],
         "state": "STARTED"
      },
      "info": {
         "baseboard": {
            "manufacturer": "Supermicro",
            "model": "H11SSL-i"
         },
         "cpu": {
            "brand": "EPYC 7551P 32-Core Processor",
            "cores": 32,
            "vendor": "AMD"
         },
         "os": {
            "distro": "Unraid OS",
            "release": "7.3 x86_64"
         },
         "system": {
            "manufacturer": "Supermicro",
            "model": "Super Server"
         }
      },
      "internalBootContext": {
         "poolNames": [
            "backup_pool",
            "backup_pool2",
            "cache",
            "cache2"
         ],
         "shareNames": [
            "anime",
            "anime_movies",
            "anime_shorts",
            "appdata",
            "appdata_lwv",
            "backups",
            "datafiles",
            "domains",
            "downloads",
            "isos",
            "movies",
            "music",
            "rated",
            "system",
            "tv",
            "unraid-phoronix-benchmark",
            "unraidconfigbackup",
            "windowsdisk",
            "zerobyte"
         ]
      },
      "metrics": {
         "cpu": {
            "percentTotal": 5.087752627576002
         },
         "memory": {
            "percentTotal": 25.37404208881634,
            "total": 67373260800
         }
      }
   }
}
```

### 2. Provider - Unraid updates

Currently there is only an Unraid API endpoint to get information about Docker containers amongst those which have an update, but not yet for the plugins which will come in a later version, according to the [Unraid API roadmap](https://docs.unraid.net/API/upcoming-features/). Whenever that happens it will also be implemented into the `unraid.py` provider.

Endpoint for this is `/unraid/updates`.

This endpoint also uses a configuration file under `/queries/unraid_updates.json` and is a simply GraphQL query
```
{
  "query": "query ContainerUpdateStatuses { docker { containerUpdateStatuses { name updateStatus } } }"
}
```
Output for one of my servers delivers the following JSON;
```
{
   "count": 2,
   "text": "crosswatch • sabnzbd",
   "updates": [
      "crosswatch",
      "sabnzbd"
   ]
}
```

### 3. Examples

- [Examples](/docs/EXAMPLES_UNRAID.md)