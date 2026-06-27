## Tracearr

Initially, the intention was to use Tracearr's internal API endpoints, but there were a number of issues that prevented me from following this route. First, the internal API logic does not use the public API key for authorization, but an internal Bearer token, and second, and more importantly, this token is rotated after a certain period. This is off course all logical and good behaviour for an application but something i overlooked at first.

So next was to do some reverse engineering and check these internal API calls further to get the database queries out of the calls and use these as a starting point for the Homepage Helpers endpoints for Tracearr.
Future proof? No certainly not as much and this might break in the future if the Tracearr developers maje significant changes in their API structure and calls.

But nonetheless i really love this application as it supports multiple media servers and also has a great looking dashboard and has loads of statistics.

Some things the Homepage Helpers Tracearr endpoints don't support yet;
* Multiple media servers something which Tracearr has support for.
* Statistiscs broken down per media server library, currently the stats are for all libraries.

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
{
  "include_unknown": true,

  "sort_order": "count_desc",
  "top_n": 8,
  "group_other": true,

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

In the example above the following is provided;
* `include_unknown` An unknown value usually points to an issue where your media server couldn't get the technical information for the media file like video and audio codec and son on. In most cases—at least in my tests—means the file became corrupted. An endpoint which lists files with an unknown attribute might be implemented later.
* `sort_order` the order how the results returned by the endpoint are sorted which can be either numerical in descending order `count_desc`, numerical in ascending order `count_asc` or alphabetical `alphabetical`.
* `top_n` shows only the top number of entries and works together with the `group_other` setting and best used with either `count_desc` or `count_asc` setting under `sort_order`. For instance if you only want to show the first eight entries returned by the query and also to group all remaining values under a label 'Other' then set `top_n` to `7` and `group_other` to `true`.
* `audio_channel_mapping`, `codec_mapping` and `resolution_mapping` are self-explanatory and just maps the ouput of the database query to more human readable output for the Homepage widget.

### 2. Available endpoints

There are now already several endpoints available;
* `/tracearr/resolutions/movies` Resolution report for movies aggregated over several movie type libraries so for example it will show a total report for libraries 'Movies', 'Anime movies', 'Anime shorts', ...
* `/tracearr/resolutions/tv` Resolution report for movies aggregated over several tv show type libraries so for example it will show a total report for libraries 'TV shows', 'Anime', ...
* `/tracearr/video_codecs` Report which shows video codecs across the whole of your media library where the media type is either movie or TV show epidose.
* `/tracearr/audio_codecs` Report which shows audio codecs across the whole of your media library where the media type is either movie or TV show epidose.
* `/tracearr/audio_channels` Report which shows audio channels across the whole of your media library where the media type is either movie or TV show epidose.
* `/tracearr/stats` Shows general statistics for the media server like total items known to the media server, total size all libraries take on disk, breakdown number of movies, TV episodes and songs and then also a breakdown of resolution—4K, 1080p, 720p and Standard definition—for all libraries.
* `/history/countries` Report about the countries where media files have been played. Interesting if you have a server you share with family or friends.
* `/history/devices` Report about the devices used when media files have been played.
* `/history/platforms` Report about the platforms used when media files have been played.
* `/history/users` Report about the users who have played media files. Interesting if you have a server you share with family or friends.
* `/history/stats` Another statistics endpoint which shows how many plays have occurred, the total watch time, the unique users and unique titles.


All endpoints follow the same structure, the configuration is read from the `tracearr_configuration.json` configuration file how items should be sorted and how many should be returned.

<!--Also the output follow a structured way and outputs something like this;
```
```
So basically this output can then be used in a `customapi` Homepage widget where you use `display: dynamic-list` to display the contents of the array in the Homepage widget, also see the Examples.-->

### 3. Examples

- [Examples](/docs/EXAMPLES_TRACEARR.md)