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
Instance settings configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from typing_extensions import Self

from ..types import SonarrConfigBase
from .custom_formats import SonarrCustomFormatsSettings
from .download_clients import SonarrDownloadClientsSettings
from .general import SonarrGeneralSettings
from .indexers import SonarrIndexersSettings
from .media_management import SonarrMediaManagementSettings
from .metadata import SonarrMetadataSettings
from .profiles import SonarrProfilesSettings
from .quality import SonarrQualitySettings
from .tags import SonarrTagsSettings
from .ui import SonarrUISettings

if TYPE_CHECKING:
    from ...secrets import SonarrSecrets


class SonarrSettings(SonarrConfigBase):
    media_management: SonarrMediaManagementSettings = (
        SonarrMediaManagementSettings()  # type: ignore[call-arg]
    )
    profiles: SonarrProfilesSettings = SonarrProfilesSettings()
    quality: SonarrQualitySettings = SonarrQualitySettings()
    custom_formats: SonarrCustomFormatsSettings = SonarrCustomFormatsSettings()
    indexers: SonarrIndexersSettings = SonarrIndexersSettings()  # type: ignore[call-arg]
    download_clients: SonarrDownloadClientsSettings = SonarrDownloadClientsSettings()
    # TODO: Enable import lists.
    # lists: SonarrListsSettings = SonarrListsSettings()
    metadata: SonarrMetadataSettings = SonarrMetadataSettings()
    tags: SonarrTagsSettings = SonarrTagsSettings()
    general: SonarrGeneralSettings = SonarrGeneralSettings()
    ui: SonarrUISettings = SonarrUISettings()

    def update_remote(
        self,
        tree: str,
        secrets: SonarrSecrets,
        remote: Self,
        check_unmanaged: bool = False,
    ) -> bool:
        # Overload base function to guarantee execution order of section updates.
        # 1. Tags must be created before everything else.
        # 2. Qualities must be updated before quality profiles.
        # 3. Download clients must be created before indexers.
        return any(
            [
                self.tags.update_remote(
                    tree=f"{tree}.tags",
                    secrets=secrets,
                    remote=remote.tags,
                    check_unmanaged=check_unmanaged,
                ),
                self.quality.update_remote(
                    tree=f"{tree}.quality",
                    secrets=secrets,
                    remote=remote.quality,
                    check_unmanaged=check_unmanaged,
                ),
                self.custom_formats.update_remote(
                    tree=f"{tree}.custom_formats",
                    secrets=secrets,
                    remote=remote.custom_formats,
                    check_unmanaged=check_unmanaged,
                ),
                self.download_clients.update_remote(
                    tree=f"{tree}.download_clients",
                    secrets=secrets,
                    remote=remote.download_clients,
                    check_unmanaged=check_unmanaged,
                ),
                self.indexers.update_remote(
                    tree=f"{tree}.indexers",
                    secrets=secrets,
                    remote=remote.indexers,
                    check_unmanaged=check_unmanaged,
                ),
                self.media_management.update_remote(
                    tree=f"{tree}.media_management",
                    secrets=secrets,
                    remote=remote.media_management,
                    check_unmanaged=check_unmanaged,
                ),
                self.profiles.update_remote(
                    tree=f"{tree}.profiles",
                    secrets=secrets,
                    remote=remote.profiles,
                    check_unmanaged=check_unmanaged,
                ),
                # self.lists.update_remote(
                #     tree=f"{tree}.lists",
                #     secrets=secrets,
                #     remote=remote.lists,
                #     check_unmanaged=check_unmanaged,
                # ),
                self.metadata.update_remote(
                    tree=f"{tree}.metadata",
                    secrets=secrets,
                    remote=remote.metadata,
                    check_unmanaged=check_unmanaged,
                ),
                self.general.update_remote(
                    tree=f"{tree}.general",
                    secrets=secrets,
                    remote=remote.general,
                    check_unmanaged=check_unmanaged,
                ),
                self.ui.update_remote(
                    tree=f"{tree}.ui",
                    secrets=secrets,
                    remote=remote.ui,
                    check_unmanaged=check_unmanaged,
                ),
            ],
        )

    def delete_remote(self, tree: str, secrets: SonarrSecrets, remote: Self) -> bool:
        # Overload base function to guarantee execution order of section deletions.
        # 1. Indexers must be deleted before download clients.
        return any(
            [
                self.profiles.delete_remote(f"{tree}.profiles", secrets, remote.profiles),
                self.indexers.delete_remote(f"{tree}.indexers", secrets, remote.indexers),
                self.download_clients.delete_remote(
                    tree=f"{tree}.download_clients",
                    secrets=secrets,
                    remote=remote.download_clients,
                ),
                self.media_management.delete_remote(
                    tree=f"{tree}.media_management",
                    secrets=secrets,
                    remote=remote.media_management,
                ),
                # self.lists.delete_remote(
                #     tree=f"{tree}.lists",
                #     secrets=secrets,
                #     remote=remote.lists,
                # ),
                self.tags.delete_remote(f"{tree}.tags", secrets, remote.tags),
                self.custom_formats.delete_remote(
                    tree=f"{tree}.custom_formats",
                    secrets=secrets,
                    remote=remote.custom_formats,
                ),
                self.quality.delete_remote(f"{tree}.quality", secrets, remote.quality),
                self.metadata.delete_remote(f"{tree}.metadata", secrets, remote.metadata),
                self.general.delete_remote(f"{tree}.general", secrets, remote.general),
                self.ui.delete_remote(f"{tree}.ui", secrets, remote.ui),
            ],
        )
