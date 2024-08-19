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
Import list exclusions settings configuration.
"""

from __future__ import annotations

from logging import getLogger
from typing import Dict, List, Set

import sonarr

from buildarr.config import RemoteMapEntry
from buildarr.types import NonEmptyStr
from pydantic import PositiveInt
from typing_extensions import Self

from ....api import sonarr_api_client
from ....secrets import SonarrSecrets
from ...types import SonarrConfigBase

logger = getLogger(__name__)


class ListExclusion(SonarrConfigBase):
    """ """

    tmdb_id: PositiveInt
    """ """

    title: NonEmptyStr
    """ """

    year: PositiveInt
    """ """

    _remote_map: List[RemoteMapEntry] = [
        ("tmdb_id", "tmdbId", {}),
        ("title", "movieTitle", {}),
        ("year", "movieYear", {}),
    ]

    @classmethod
    def _from_remote(cls, api_listexclusion: sonarr.ImportExclusionsResource) -> Self:
        return cls(**cls.get_local_attrs(cls._remote_map, api_listexclusion.to_dict()))

    def _create_remote(self, tree: str, secrets: SonarrSecrets) -> None:
        with sonarr_api_client(secrets=secrets) as api_client:
            sonarr.ImportExclusionsApi(api_client).create_exclusions(
                import_exclusions_resource=sonarr.ImportExclusionsResource.from_dict(
                    self.get_create_remote_attrs(tree=tree, remote_map=self._remote_map),
                ),
            )

    def _update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        api_listexclusion: sonarr.ImportExclusionsResource,
    ) -> bool:
        updated, updated_attrs = self.get_update_remote_attrs(
            tree=tree,
            remote=remote,
            remote_map=self._remote_map,
            set_unchanged=True,
        )
        if updated:
            with sonarr_api_client(secrets=secrets) as api_client:
                sonarr.ImportExclusionsApi(api_client).update_exclusions(
                    id=str(api_listexclusion.id),
                    import_exclusions_resource=sonarr.ImportExclusionsResource.from_dict(
                        {**api_listexclusion.to_dict(), **updated_attrs},
                    ),
                )
            return True
        return False

    def _delete_remote(self, secrets: SonarrSecrets, listexclusion_id: int) -> None:
        with sonarr_api_client(secrets=secrets) as api_client:
            sonarr.ImportExclusionsApi(api_client).delete_exclusions(id=listexclusion_id)


class ListExclusionsSettings(SonarrConfigBase):
    """
    Using import lists, Sonarr can monitor and import episodes from external sources.

    ```yaml
    sonarr:
      settings:
        import_lists:
          delete_unmanaged: False # Default is `false`
          delete_unmanaged_exclusions: true # Default is `false`
          definitions:
            Plex: # Name of import list definition
              type: "plex-watchlist" # Type of import list to use
              # Attributes common to all watch list types
              enable_automatic_add: true
              monitor: "all-episodes"
              series_type: "standard"
              season_folder: true
              tags:
                - "example"
              # Plex-specific attributes
              access_token: "..."
            # Add more import lists here.
          exclusions:
            72662: "Teletubbies" # TVDB ID is key, set an artibrary title as value
    ```

    Media can be queued on the source, and Sonarr will automatically import them,
    look for suitable releases, and download them.

    Media that you don't want to import can be ignored using the `exclusions`
    attribute.
    """

    delete_unmanaged: bool = False
    """
    Automatically delete import lists not defined in Buildarr.
    """

    definitions: Set[ListExclusion] = set()
    """
    Import list definitions go here.
    """

    @classmethod
    def from_remote(cls, secrets: SonarrSecrets) -> Self:
        with sonarr_api_client(secrets=secrets) as api_client:
            api_listexclusions = sonarr.ImportExclusionsApi(api_client).list_exclusions()
        return cls(
            definitions=set(
                ListExclusion._from_remote(api_listexclusion)
                for api_listexclusion in api_listexclusions
            ),
        )

    def update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        changed = False
        with sonarr_api_client(secrets=secrets) as api_client:
            api_listexclusions: Dict[int, sonarr.ImportExclusionsResource] = {
                api_listexclusion.tmdb_id: api_listexclusion
                for api_listexclusion in sonarr.ImportExclusionsApi(api_client).list_exclusions()
            }
        local_listexclusions = {
            listexclusion.tmdb_id: listexclusion for listexclusion in self.definitions
        }
        remote_listexclusions = {
            listexclusion.tmdb_id: listexclusion for listexclusion in remote.definitions
        }
        for i, listexclusion in enumerate(local_listexclusions.values()):
            listexclusion_tree = f"{tree}.definitions[{i}]"
            if listexclusion.tmdb_id not in remote_listexclusions:
                listexclusion._create_remote(tree=listexclusion_tree, secrets=secrets)
                changed = True
            elif listexclusion._update_remote(
                tree=listexclusion_tree,
                secrets=secrets,
                remote=remote_listexclusions[listexclusion.tmdb_id],
                api_listexclusion=api_listexclusions[listexclusion.tmdb_id],
            ):
                changed = True
        return changed

    def delete_remote(self, tree: str, secrets: SonarrSecrets, remote: Self) -> bool:
        changed = False
        with sonarr_api_client(secrets=secrets) as api_client:
            api_listexclusions: Dict[int, sonarr.ImportExclusionsResource] = {
                api_listexclusion.tmdb_id: api_listexclusion
                for api_listexclusion in sonarr.ImportExclusionsApi(api_client).list_exclusions()
            }
        local_listexclusions = {
            listexclusion.tmdb_id: listexclusion for listexclusion in self.definitions
        }
        remote_listexclusions = {
            listexclusion.tmdb_id: listexclusion for listexclusion in remote.definitions
        }
        i = -1
        for listexclusion in remote_listexclusions.values():
            if listexclusion.tmdb_id not in local_listexclusions:
                listexclusion_tree = f"{tree}.definitions[{i}]"
                if self.delete_unmanaged:
                    logger.info("%s: (...) -> (deleted)", listexclusion_tree)
                    listexclusion._delete_remote(
                        secrets=secrets,
                        listexclusion_id=api_listexclusions[listexclusion.tmdb_id].id,
                    )
                    changed = True
                else:
                    logger.debug("%s: (...) (unmanaged)", listexclusion_tree)
                i -= -1
        return changed
