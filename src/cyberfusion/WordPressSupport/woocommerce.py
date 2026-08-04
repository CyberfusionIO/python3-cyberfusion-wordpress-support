"""Classes for managing WooCommerce."""

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import WoocommerceNotInstalledError
from cyberfusion.WordPressSupport.plugins import Plugin
from cyberfusion.WordPressSupport.version import Version

NAME_PLUGIN = "woocommerce"

VERSION_HPOS_SUBCOMMAND = Version("7.1.0")


class Woocommerce:
    """Abstraction of WooCommerce."""

    NAME_COMMAND = "wc"

    def __init__(self, installation: Installation) -> None:
        """Set attributes and call functions."""
        self.installation = installation

    @property
    def is_hpos_enabled(self) -> bool:
        """Set if HPOS is enabled."""
        plugin = Plugin(self.installation, NAME_PLUGIN)

        if not plugin.is_activated:
            raise WoocommerceNotInstalledError

        if plugin.version < VERSION_HPOS_SUBCOMMAND:
            return False

        self.installation.command.execute(
            [self.NAME_COMMAND, "hpos", "status"],
            include_plugins=[NAME_PLUGIN],
        )

        # Parse raw text, as command doesn't support JSON output:
        # https://github.com/woocommerce/woocommerce/issues/65303

        first_line = self.installation.command.stdout.splitlines()[0]

        return first_line.split("HPOS enabled?:", 1)[1].strip() == "yes"
