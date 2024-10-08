# Copyright (C) 2023 Callum Dickinson
#
# Buildarr is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# Buildarr is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with Buildarr.
# If not, see <https://www.gnu.org/licenses/>.


"""
Configuration utility classes and functions.
"""

from __future__ import annotations

from datetime import datetime, timezone


def language_parse(value: str) -> str:
    """
    Parse a language name into a more standardised format.

    Args:
        value (str): Language name to parse

    Returns:

    Parsed language name string.

    * `English` -> `english`
    * `english` -> `english`
    * `ENGLISH` -> `english`
    * `Portuguese (Brazil)` -> `portuguese-brazil`
    * `portuguese_brazil` -> `portuguese-brazil`
    * `PORTUGUESE-BRAZIL` -> `portuguese-brazil`
    """
    return "-".join(value.lower().replace("_", "-").replace("()", "").split(" "))


def trakt_expires_encoder(dt: datetime) -> str:
    """
    Trakt OAuth token `expires` field API value encoder.

    Converts a naive or timezone-aware `datetime` object to a ISO-8601 string
    in UTC time with a Zulu timezone marker.

    If the original `datetime` object is naive, assume it is already in UTC
    and do not convert.

    Args:
        dt (datetime): Object to encode

    Returns:
        ISO-8601 date-time string in UTC with Zulu timezone marker
    """

    if dt.tzinfo == timezone.utc:
        dt_aware = dt
    elif dt.tzinfo is not None:
        dt_aware = dt.astimezone(timezone.utc)
    else:
        dt_aware = dt.replace(tzinfo=timezone.utc)

    return dt_aware.isoformat().replace("+00:00", "Z")
