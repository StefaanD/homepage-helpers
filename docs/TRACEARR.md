## Tracearr

Required environment variables:

```env
TRACEARR_URL=http://tracearr:3002
TRACEARR_TOKEN=your_token
```

This provider serves two endpoints;
* `/tracearr/session_aggregates` (Aggregate report for the whole period as can be seen on the Tracearr dashboard under the History section)
* `/tracearr/resolution` (Resolution report as also shown under Library -> Quality)
* `/tracearr/codecs` (Codecs report as also shown under Library -> Quality)

All providers have their own query file containing the Tracearr internal API call so;
* `tracearr_session_aggregates.json` for the `/tracearr/session_aggregates` endpoint.
* `tracearr_resolution.json` for the `/tracearr/resolution` endpoint.
* `tracearr_codecs.json` for the `/tracearr/codecs` endpoint