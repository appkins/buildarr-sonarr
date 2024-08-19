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
from pydantic import AnyHttpUrl, validator

from ..util import NabCategory
from .base import UsenetIndexer


class NewznabIndexer(UsenetIndexer):
    """
    An indexer for monitoring a Newznab-compliant Usenet indexing site.

    Sonarr defines presets for several popular sites.
    """

    # Monitor for new releases using a Newznab-compatible Usenet indexer or site.

    type: Literal["newznab"] = "newznab"
    """
    Type value associated with this kind of indexer.
    """

    base_url: AnyHttpUrl
    """
    URL of the Newznab-compatible indexing site.
    """

    api_path: NonEmptyStr = "/api"  # type: ignore[assignment]
    """
    Newznab API endpoint. Usually `/api`.
    """

    api_key: Password
    """
    API key for use with the Newznab API.
    """

    categories: Set[Union[NabCategory, int]] = {NabCategory.TV_SD, NabCategory.TV_HD}
    """
    Categories to monitor for standard/daily shows.
    Define as empty to disable.

    Values:

    * `TV`
    * `TV/WEB-DL`
    * `TV/Foreign`
    * `TV/SD`
    * `TV/HD`
    * `TV/UHD`
    * `TV/Other`
    * `TV/Sport`
    * `TV/Anime`
    * `TV/Documentary`
    * `TV/x265`

    *Changed in version 0.6.1*: The Sonarr-native values for Newznab/Torznab categories
    (e.g. `TV/WEB-DL`) can now be specified, instead of the Buildarr-native values
    (e.g. `TV-WEBDL`). The old values can still be used.
    """

    anime_categories: Set[NabCategory] = set()
    """
    Categories to monitor for anime.
    Define as empty to disable.

    Values:

    * `TV`
    * `TV/WEB-DL`
    * `TV/Foreign`
    * `TV/SD`
    * `TV/HD`
    * `TV/UHD`
    * `TV/Other`
    * `TV/Sport`
    * `TV/Anime`
    * `TV/Documentary`
    * `TV/x265`

    *Changed in version 0.6.1*: The Sonarr-native values for Newznab/Torznab categories
    (e.g. `TV/WEB-DL`) can now be specified, instead of the Buildarr-native values
    (e.g. `TV-WEBDL`). The old values can still be used.
    """

    anime_standard_format_search: bool = False
    """
    Also search for anime using the standard numbering. Only applies for Anime series types.
    """

    additional_parameters: Optional[str] = None
    """
    Additional Newznab API parameters.
    """

    # TODO: Add support for presets.

    _implementation = "Newznab"
    _remote_map: List[RemoteMapEntry] = [
        ("base_url", "baseUrl", {"is_field": True}),
        ("api_path", "apiPath", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
        (
            "categories",
            "categories",
            {"is_field": True, "encoder": lambda v: sorted(NabCategory.encode(c) for c in v)},
        ),
        (
            "anime_categories",
            "animeCategories",
            {"is_field": True, "encoder": lambda v: sorted(NabCategory.encode(c) for c in v)},
        ),
        ("anime_standard_format_search", "animeStandardFormatSearch", {"is_field": True}),
        (
            "additional_parameters",
            "additionalParameters",
            {"is_field": True, "field_default": None, "decoder": lambda v: v or None},
        ),
    ]

    @validator("categories", "anime_categories")
    def validate_categories(
        cls,
        value: Iterable[Union[NabCategory, int]],
    ) -> Set[Union[NabCategory, int]]:
        return set(
            NabCategory.decode(category) if isinstance(category, int) else category
            for category in value
        )
