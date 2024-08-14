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
Newznab indexer configuration.
"""


from __future__ import annotations

from typing import Iterable, List, Literal, Optional, Set, Union

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr, Password
from pydantic import AnyHttpUrl, field_validator

from ..util import NabCategory
from .base import UsenetIndexer

class FanzubIndexer(UsenetIndexer):
    """
    An indexer which uses a Fanzub-compatible RSS feed to monitor for releases.
    """

    type: Literal["fanzub"] = "fanzub"
    """
    Type value associated with this kind of indexer.
    """

    rss_url: RssUrl
    """
    A URL to a Fanzub compatible RSS feed.
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    _implementation = "Fanzub"
    _implementation_name = "Fanzub"
    _config_contract = "FanzubSettings"
    _remote_map: ClassVar[List[RemoteMapEntry]] = [
        ("rss_url", "rssUrl", {"is_field": True}),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
    ]