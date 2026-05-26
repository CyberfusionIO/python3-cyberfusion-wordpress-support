"""Classes for managing WooCommerce."""

from cyberfusion.WordPressSupport import Installation


class Woocommerce:
    """Abstraction of WooCommerce."""

    NAME_COMMAND = "wc"

    def __init__(self, installation: Installation) -> None:
        """Set attributes and call functions."""
        self.installation = installation

    @property
    def is_hpos_enabled(self) -> bool:
        """Set if HPOS is enabled."""
        self.installation.command.execute([self.NAME_COMMAND, "hpos", "status"])

        # Parse raw text, as command doesn't support JSON output:
        # https://github.com/woocommerce/woocommerce/issues/65303

        first_line = self.installation.command.stdout.splitlines()[0]

        return first_line.split("HPOS enabled?:", 1)[1].strip() == "yes"
