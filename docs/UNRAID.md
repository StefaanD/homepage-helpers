## Unraid

As stated in Readme file, i use Unraid OS to run my Homepage docker and also here the default widget didn't provide my what i actually wanted to show on my homepage.

This provider makes use of the Unraid API, for more information see the [Using the Unraid API](https://docs.unraid.net/API/how-to-use-the-api/) documentation.

This provider actually serves two endpoints;
* `/unraid/stats` (Basic hardware stats for the machine)
* `/unraid/updates` (Checks if there are Docker container updates)

### 1. Unraid stats

Endpoint for this is `/unraid/stats` and expects the following input parameters to work;
* `url` the host IP address of FQDN
* `apikey` the Unraid API key
* `token` the Unraid CSRF token

This endpoint uses the `/queries/unraid_stats.json` file to set the query executed against Unraid's API

In my configuration the Unraid GraphQL query looks like
```
{
  "query": "query { array { state capacity { kilobytes { total free } } disks { name size status temp } } metrics { cpu { percentTotal } memory { total percentTotal } } info { baseboard { manufacturer model } cpu { brand cores vendor } os { release distro } system { manufacturer model } } internalBootContext { poolNames shareNames } }"
}
```

So it gets information about the motherboard, CPU, memory, OS and version and the array size and free space.

### 2. Unraid updates

Currently there is only an Unraid API endpoint to get information about Docker containers amongst those which have an update, but not yet for the plugins which will come in a later version, according to the Unraid roadmap. Whenever that happens it will also be implemented into the `unraid.py` provider.

Endpoint for this is `/unraid/updates` and much like the /unraid/stats endpoint it expects the following input parameters; and expects the following input to work;
* `url` which is the host IP address of FQDN
* `apikey` which is the Unraid API key
* `token` which is the Unraid CSRF token

This endpoint also uses a configuration file under `/queries/unraid_updates.json` and is a simply GraphQL query
```
{
  "query": "query ContainerUpdateStatuses { docker { containerUpdateStatuses { name updateStatus } } }"
}
```

### 3. Examples

- [Examples](/docs/EXAMPLES.md)