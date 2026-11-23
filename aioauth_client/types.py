"""Type aliases for provider responses."""

TRes = dict[str, "TRes"] | list["TRes"] | str | int | float | bool | None
THeaders = dict[str, str]
TParams = dict[str, str | None]
