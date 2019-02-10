# libtvdb

A wrapper around the [TVDB API](https://api.thetvdb.com/swagger).

## Examples:

Searching for shows:

```
import libtvdb
client = libtvdb.TVDBClient(api_key="...", user_key="...", user_name="...")
shows = client.search_show("Doctor Who")

for show in shows:
    print(show.name)
```

## Advanced

You can set `libtvdb_api_key`, `libtvdb_user_key` and `libtvdb_user_name` in your OS X keychain if you don't want to supply these every time. If any of the values supplied to the `TVDBClient` constructor are `None`, it will look into your keychain and load the appropriate value. If it can't find them, it will throw an exception.
