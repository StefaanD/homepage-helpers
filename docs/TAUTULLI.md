## Tautulli providers

Although Homepage has a great Tautulli widget which provides more information than the Plex widget, that widget has no configurable fields.
So I first tried the API route in Tautulli, but in my setup with nearly 1,000 movies and 1,000 TV series, it took almost 10 seconds to load the information into the widget, even though both Plex and Tautulli are running on the same machine and that server is certainly no slouch.

Didn’t actually investigate further what was causing this delay. So in the end another approach was taken and that was to get the information directly from the Tautulli database which gives near instant results. This finding actually sparked the beginning of the Homepage Helpers docker container.

### 1. Provider - Tautulli stats

* This provider currently serves a single endpoint `/tautulli/stats`
* The endpoint takes one input parameter `aggregate` with value **on** or **off** and when the parameter is not provided it defaults to **on**.

The actual SQL query used against the Tautulli database is;
```
SELECT
	section_name,
	section_type,
	count,
	parent_count,
	child_count
FROM library_sections
```

This query simply gets the library name, the type and the count of the different media types in the library. The type is used to calculate a total for Movies, TV Shows in case the input parameter `aggregate` is on. The JSON output looks like this;
```
{
   "albums": 1260,
   "artists": 348,
   "movies": 955,
   "tracks": 20141,
   "tvshows": 810
}
```

### 2. Examples

- [Examples](/docs/EXAMPLES_TAUTULLI.md)