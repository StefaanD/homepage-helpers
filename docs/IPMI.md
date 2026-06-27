## IPMI

As i'm lucky enough to have an Unraid server which uses a Supermicro motherboard i also have access to IPMI to remotely manage it. But the ipmi also provide statistics like temperatures, voltage, fan speeds and so on through the ipmi-sensors command.

If IMPI is not used in your setup, then the line below can be removed from the Dockerfile.
```
RUN apk add --no-cache freeipmi
```
### 1. Provider - IPMI stats

The endpoint is `/ipmi/sensors` and expects the following input parameters to work;
* `host` the host IP address of FQDN
* `username` the username used to log into the IPMI interface
* `password` the password used to log into the IPMI interface

This endpoint also uses a configuration file found under `/queries/ipmi_sensors.json` and sets which fields to present in the output from the ipmi-sensors commands output. An example could be like this.
```
{
  "temperatures": [
    "CPU Temp",
    "System Temp",
    "Peripheral Temp"
  ],
  "fans": [
    "FAN2",
    "FAN3",
    "FAN4",
    "FAN5",
    "FANB"
  ]
}
```

### 2. Examples

- [Examples](/docs/EXAMPLES_IPMI.md)