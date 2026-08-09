"""Classes for managing Redis Object Cache."""

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import RedisObjectCacheNotInstalledError
from cyberfusion.WordPressSupport.plugins import Plugin

NAME_PLUGIN = "redis-cache"


class RedisObjectCache:
    """Abstraction of Redis Object Cache."""

    NAME_COMMAND = "redis"

    def __init__(self, installation: Installation) -> None:
        """Set attributes and call functions."""
        self.installation = installation

    def _ensure_activated(self) -> None:
        """Raise if plugin is not activated."""
        if not Plugin(self.installation, NAME_PLUGIN).is_activated:
            raise RedisObjectCacheNotInstalledError

    def enable(self) -> None:
        """Enable object cache."""
        self._ensure_activated()

        self.installation.command.execute(
            [self.NAME_COMMAND, "enable"],
            include_plugins=[NAME_PLUGIN],
        )

    def disable(self) -> None:
        """Disable object cache."""
        self._ensure_activated()

        self.installation.command.execute(
            [self.NAME_COMMAND, "disable"],
            include_plugins=[NAME_PLUGIN],
        )
