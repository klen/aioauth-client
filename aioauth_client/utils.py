"""Helpers shared by the OAuth clients."""


def split_location(location: str | None, sep: str = ",") -> tuple[str, str]:
    """Split a free-form location into a city and a country."""
    city, _, country = (location or "").partition(sep)
    return city.strip(), country.strip()
