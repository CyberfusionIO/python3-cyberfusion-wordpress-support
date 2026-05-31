"""Classes for managing plugins."""

from typing import Optional
from enum import StrEnum
from typing import List
from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import (
    CommandFailedError,
    PluginAlreadyActivatedError,
    PluginAlreadyInstalledError,
)


class PluginStatus(StrEnum):
    ACTIVE = "active"
    ACTIVE_NETWORK = "active-network"
    DROPIN = "dropin"
    INACTIVE = "inactive"
    MUST_USE = "must-use"


class Plugin:
    """Abstraction of WordPress plugin."""

    NAME_COMMAND = "plugin"

    def __init__(self, installation: Installation, name: str) -> None:
        """Set attributes and call functions."""
        self.installation = installation
        self.name = name

    @property
    def is_installed(self) -> bool:
        """Set if is installed."""
        try:
            self.installation.command.execute(
                [self.NAME_COMMAND, "is-installed", self.name]
            )
        except CommandFailedError:
            return False

        return True

    @property
    def is_activated(self) -> bool:
        """Set if is activated."""
        try:
            self.installation.command.execute(
                [self.NAME_COMMAND, "is-active", self.name]
            )
        except CommandFailedError:
            return False

        return True

    def install(self) -> None:
        """Install plugin."""
        if self.is_installed:
            raise PluginAlreadyInstalledError

        self.installation.command.execute([self.NAME_COMMAND, "install", self.name])

    def activate(self) -> None:
        """Activate plugin."""
        if self.is_activated:
            raise PluginAlreadyActivatedError

        self.installation.command.execute([self.NAME_COMMAND, "activate", self.name])


class Plugins:
    """Abstraction of WordPress plugins."""

    NAME_COMMAND = "plugin"

    def __init__(self, installation: Installation) -> None:
        """Set attributes and call functions."""
        self.installation = installation

    def get(self, status: Optional[PluginStatus] = None) -> List[Plugin]:
        """Get plugins."""
        results: List[Plugin] = []

        # Construct command

        command = [self.NAME_COMMAND, "list"]

        if status:
            command.append(f"--status={status}")

        # Execute command

        self.installation.command.execute(
            command,
            json_format=True,
        )

        # Iterate over results

        for plugin in self.installation.command.stdout:
            results.append(Plugin(self.installation, plugin["name"]))

        return results
