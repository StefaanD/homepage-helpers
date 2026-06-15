## Tracearr

Initially, the intention was to use Tracearr's internal API endpoints, but there were a number of issues that prevented me from following this route. First, the internal API logic does not use the public API key for authorization, but an internal Bearer token, and second, and more importantly, this token is rotated after a certain period.

### 1. Environment variables

The various Tracearr endpoints in the Homepage Helpers require the following environment variables:

```env
  TRACEARR_DB_HOST: tracearr-supervised
  TRACEARR_DB_PORT: 5432
  TRACEARR_DB_NAME: tracearr
  TRACEARR_DB_USER: tracearr
  TRACEARR_DB_PASSWORD: tracearr
```
For the Unraid docker container, these variables will be available in the template once the container is available in Community Apps.

There is also a configuration file `tracearr_configuration.json` where the default looks like this;
```
{
  "include_unknown": true,

  "sort_order": "count_desc",

  "audio_channel_mapping": {
    "0": "Unknown",
    "1": "1.0",
    "2": "2.0",
    "3": "2.1",
    "4": "4.0",
    "5": "5.0",
    "6": "5.1",
    "7": "6.1",
    "8": "7.1"
  },

  "codec_mapping": {
    "DCA-MA": "DTS-HD MA",
    "DCA": "DTS",
    "TRUEHD": "Dolby TrueHD",
    "EAC3": "Dolby Digital Plus",
    "AC3": "Dolby Digital",
    "HEVC": "H.265 / HEVC",
    "H264": "H.264 / AVC",
    "AV1": "AV1",
    "VP9": "VP9",
    "VC1": "VC-1",
    "WMV3": "VC-1 (WMV3)",
    "MPEG4": "MPEG-4",
    "MSMPEG4V3": "MPEG-4 (MSMPEG4V3)",
    "MPEG2VIDEO": "MPEG Video",
    "unknown": "Unknown"
  },

  "resolution_mapping": {
    "sd": "SD",
    "480p": "480p",
    "576p": "576p",
    "720p": "720p",
    "1080p": "1080p",
    "2k": "2K",
    "4k": "4K",
    "unknown": "Unknown"
  }
}
```
There is also a configuration file per endpoint available to override some of the defaults in the main `tracearr_configuration.json` configuration file

In the example above the following is provided;
* `include_unknown` which can be overrides by the endpoint configuration. An unknown value usually points to an issue where your media server can't get the information for the media file, in most cases—at least in my tests—means the file is corrupt. An endpoint which lists files with an unknown attribute might be implemented later.
* `sort_order` the order how the results returned by the endpoint are sorted which can be either numerical `count_desc` or alphabetical `alphabetical`.
* `audio_channel_mapping`, `codec_mapping` and `resolution_mapping` are self-explanatory and just maps the ouput of the database query to more human readable output for the Homepage widget.

The configuration per endpoint is named after it's endpoint so endpoint `/tracearr/resolutions/movies` has a configuration file named `tracearr_resolutions_movies.json`

The contents of the endpoint configuration file looks like this;
```
{
  "title": "Movie Resolutions",
  "sort": "count_desc",
  "include_unknown": true,
  "endpoint": "/tracearr/resolutions_movies",
  "display": "dynamic-list"
}
```
It's not advised to make any changes in this configuration file, except for the `sort` and `include_unknown` parameters which when changed override the values set in `tracearr_configuration.json` for the specific endpoint.

### 2. Available endpoints

There are several endpoints available;
* `/tracearr/resolutions/movies` Resolution report for movies aggregated over several movie type libraries so for example it will show a total report for libraries 'Movies', 'Anime movies', 'Anime shorts', ...
* `/tracearr/resolutions/tv` Resolution report for movies aggregated over several tv show type libraries so for example it will show a total report for libraries 'TV shows', 'Anime', ...
* `/tracearr/video_codecs` Report which shows video codecs across the whole of your media library where the media type is either movie or TV show epidose.
* `/tracearr/audio_codecs` Report which shows audio codecs across the whole of your media library where the media type is either movie or TV show epidose.
* `/tracearr/audio_channels` Report which shows audio channels across the whole of your media library where the media type is either movie or TV show epidose.
* `/tracearr/session_aggregates` To be implemented
* `/tracearr/platforms` To be implemented
* `/tracearr/devices` To be implemented
* `/tracearr/watch_history` To be implemented

All endpoints follow the same structure, the configuration is read from both the `tracearr_configuration.json` and the endpoints specific configuration file.

Also the output follow a structured way and outputs something like this;
```
```
So basically this output can then be used in a `customapi` Homepage widget where you use `display: dynamic-list` to display the contents of the array in the Homepage widget, also see the Examples.

### 3. Examples

- [Examples](/docs/EXAMPLES.md)