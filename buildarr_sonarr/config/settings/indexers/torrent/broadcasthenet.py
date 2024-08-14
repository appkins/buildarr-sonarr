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
BroacasTheNet indexer configuration.
"""


from __future__ import annotations

from typing import List, Literal, Set

from buildarr.config import RemoteMapEntry
from buildarr.types import BaseEnum, NonEmptyStr, Password
from pydantic import AnyHttpUrl

from .base import TorrentIndexer

class BroadcasthenetIndexer(TorrentIndexer):
    """
    Indexer for monitoring for new releases on BroacasTheNet.
    """

    type: Literal["broadcasthenet"] = "broadcasthenet"
    """
    Type value associated with this kind of indexer.
    """

    api_url: AnyHttpUrl = AnyHttpUrl("https://api.broadcasthe.net")
    """
    BroadcasTheNet API URL.
    """

    api_key: Password
    """
    BroadcasTheNet API key.
    """

    _implementation = "BroadcastheNet"
    _implementation_name = "BroadcasTheNet"
    _config_contract = "BroadcastheNetSettings"
    _remote_map: List[RemoteMapEntry] = [
        ("api_url", "apiUrl", {"is_field": True}),
        ("api_key", "apiKey", {"is_field": True}),
    ]