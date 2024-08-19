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
Plugin and instance configuration.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Optional

from buildarr.config import ConfigPlugin
from buildarr.types import NonEmptyStr, Port
from pydantic import validator
from typing_extensions import Self

from ..types import ArrApiKey, SonarrProtocol
from .settings import SonarrSettings

if TYPE_CHECKING:
    from ..secrets import SonarrSecrets

    class _SonarrInstanceConfig(ConfigPlugin[SonarrSecrets]): ...

else:

    class _SonarrInstanceConfig(ConfigPlugin): ...


class SonarrInstanceConfig(_SonarrInstanceConfig):
    """
    By default, Buildarr will look for a single instance at `http://sonarr:8989`.
    Most configurations are different, and to accommodate those, you can configure
    how Buildarr connects to individual Sonarr instances.

    Configuration of a single Sonarr instance:

    ```yaml
    sonarr:
      hostname: "sonarr.example.com"
      port: 8989
      protocol: "http"
      settings:
        ...
    ```

    Configuration of multiple instances:

    ```yaml
    sonarr:
      # Configuration and settings common to all instances.
      port: 8989
      settings:
        ...
      instances:
        # Sonarr instance 1-specific configuration.
        sonarr1:
          hostname: "sonarr1.example.com"
          settings:
            ...
        # Sonarr instance 2-specific configuration.
        sonarr2:
          hostname: "sonarr2.example.com"
          api_key: "..." # Explicitly define API key
          settings:
            ...
    ```
    """

    hostname: NonEmptyStr = "sonarr"  # type: ignore[assignment]
    """
    Hostname of the Sonarr instance to connect to.

    When defining a single instance using the global `sonarr` configuration block,
    the default hostname is `sonarr`.

    When using multiple instance-specific configurations, the default hostname
    is the name given to the instance in the `instances` attribute.

    ```yaml
    sonarr:
      instances:
        sonarr1: # <--- This becomes the default hostname
          ...
    ```
    """

    port: Port = 8989  # type: ignore[assignment]
    """
    Port number of the Sonarr instance to connect to.
    """

    protocol: SonarrProtocol = "http"  # type: ignore[assignment]
    """
    Communication protocol to use to connect to Sonarr.

    Values:

    * `http`
    * `https`
    """

    url_base: Optional[str] = None
    """
    The URL path the Sonarr instance API is available under, if behind a reverse proxy.

    API URLs are rendered like this: `<protocol>://<hostname>:<port><url_base>/api/v3/...`

    When unset, the URL root will be used as the API endpoint
    (e.g. `<protocol>://<hostname>:<port>/api/v3/...`).

    *Added in version 0.2.3.*
    """

    api_key: Optional[ArrApiKey] = None
    """
    API key to use to authenticate with the Sonarr instance.

    If undefined or set to `null`, automatically retrieve the API key.
    This can only be done on Sonarr instances with authentication disabled.

    **If authentication is enabled on the Sonarr instance, this field is required.**
    """

    version: Optional[str] = None
    """
    The expected version of the Sonarr instance.
    If undefined or set to `null`, the version is auto-detected.

    This value is also used when generating a Docker Compose file.
    When undefined or set to `null`, the version tag will be set to `latest`.
    """

    image: NonEmptyStr = "lscr.io/linuxserver/sonarr"  # type: ignore[assignment]
    """
    The default Docker image URI to use when generating a Docker Compose file.
    """

    settings: SonarrSettings = SonarrSettings()
    """
    Sonarr application settings.

    Configuration options for Sonarr itself are set within this structure.
    """

    @validator("url_base")
    def validate_url_base(cls, value: Optional[str]) -> Optional[str]:
        return f"/{value.strip('/')}" if value and value.strip("/") else None

    def uses_trash_metadata(self) -> bool:
        if self.settings.quality.uses_trash_metadata():
            return True
        if self.settings.custom_formats.uses_trash_metadata():
            return True
        return False

    def post_init_render(self, secrets: SonarrSecrets) -> Self:
        copy = self.copy(deep=True)
        copy._post_init_render(secrets=secrets)
        return copy

    def _post_init_render(self, secrets: SonarrSecrets) -> None:
        if self.settings.quality.uses_trash_metadata():
            self.settings.quality._render()
        if self.settings.custom_formats.uses_trash_metadata():
            self.settings.custom_formats._post_init_render(secrets=secrets)
        self.settings.profiles.quality_profiles._render(
            custom_formats=self.settings.custom_formats.definitions,
        )

    @classmethod
    def from_remote(cls, secrets: SonarrSecrets) -> Self:
        return cls(
            hostname=secrets.hostname,
            port=secrets.port,
            protocol=secrets.protocol,
            api_key=secrets.api_key,
            version=secrets.version,
            settings=SonarrSettings.from_remote(secrets),
        )

    def to_compose_service(self, compose_version: str, service_name: str) -> Dict[str, Any]:
        return {
            "image": f"{self.image}:{self.version or 'latest'}",
            "volumes": {service_name: "/config"},
        }


class SonarrConfig(SonarrInstanceConfig):
    """
    Sonarr plugin global configuration class.
    """

    instances: Dict[str, SonarrInstanceConfig] = {}
    """
    Instance-specific Sonarr configuration.

    Can only be defined on the global `sonarr` configuration block.

    Globally specified configuration values apply to all instances.
    Configuration values specified on an instance-level take precedence at runtime.
    """
