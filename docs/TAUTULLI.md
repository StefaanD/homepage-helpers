## Tautulli providers

Although Homepage has a great Tautulli widget which provides more information than the Plex widget, in my setup with close to a 1000 movies and 1000 tv shows, it took almost 10 seconds to get the information into the widget although both Plex and Tautulli run on the same machine. 

Didn’t actually investigate further what was causing this delay. But instead of investing too much time in figuring this out, another approach was taken and that was to get the information directly from the Tautulli database which gives near instant results. This finding actually sparked the beginning of the Homepage Helpers docker container.

### 1. Tautulli stats

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

This query simply gets the library name, the type and the count of the titles in the library. The type is used to calculate a total for Movies, TV Shows in case the input parameter `aggregate` is on.

### 2. Examples

- [Examples](/docs/EXAMPLES.md)