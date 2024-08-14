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
Indexer configuration utility classes and functions.
"""


from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, cast

from buildarr.types import BaseEnum

if TYPE_CHECKING:
    from typing import Union

    from typing_extensions import Self

logger = getLogger(__name__)


class NabCategory(BaseEnum):
    # https://github.com/Prowlarr/Prowlarr/blob/develop/src/NzbDrone.Core/Indexers/NewznabStandardCategory.cs
    TV = (5000, "TV")
    TV_WEBDL = (5010, "TV/WEB-DL")
    TV_FOREIGN = (5020, "TV/Foreign")
    TV_SD = (5030, "TV/SD")
    TV_HD = (5040, "TV/HD")
    TV_UHD = (5045, "TV/UHD")
    TV_OTHER = (5050, "TV/Other")
    TV_SPORT = (5060, "TV/Sport", "TV/Sports")
    TV_ANIME = (5070, "TV/Anime")
    TV_DOCUMENTARY = (5080, "TV/Documentary")
    TV_X265 = (5090, "TV/x265")

    @classmethod
    def decode(cls, value: int) -> Union[Self, int]:
        try:
            return cls(value)
        except ValueError:
            return value

    @classmethod
    def encode(cls, value: Union[Self, int]) -> int:
        return value if isinstance(value, int) else cast(int, value.value)

class FilelistCategory(BaseEnum):
    """
    Filelist category enumeration.
    """

    ANIME = "Anime"
    ANIMATION = "Animation"
    TV_4K = "TV 4K"
    TV_HD = "TV HD"
    TV_SD = "TV SD"
    SPORT = "Sport"
