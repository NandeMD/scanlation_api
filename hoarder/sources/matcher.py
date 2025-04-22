from . import BaseSource
from .all_sources import ALL_SOURCES


def match_manga_source(url: str) -> type[BaseSource] | None:
    """
    Match the given URL to a manga source class.

    Args:
        url (str): The URL to match.

    Returns:
        type[BaseSource] | None: The matched manga source class or None if no match is found.
    """
    for source in ALL_SOURCES:
        for identifier in source.identifiers:
            if identifier in url:
                return source
    return None
