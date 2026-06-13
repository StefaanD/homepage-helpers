## Tracearr

Required environment variables:

```env
TRACEARR_URL=http://tracearr:3002
TRACEARR_TOKEN=your_token
```

This provider serves two endpoints;
* `/tracearr/resolution` (Resolution report as also shown under Library -> Quality)
* `/tracearr/codecs` (Codecs report as also shown under Library -> Quality)

Both providers have their own query file containing the Tracearr internal API call so;
* `tracearr_resolution.json` for the `/tracearr/resolution` endpoint.
* `tracearr_codecs.json` for the `/tracearr/codecs` endpoint