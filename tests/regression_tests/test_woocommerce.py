import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import CommandFailedError
from cyberfusion.WordPressSupport.woocommerce import Woocommerce


def test_woocommerce_is_hpos_enabled_returns_false_below_hpos_subcommand_version(
    installation_installed: Installation,
) -> None:
    installation = installation_installed

    # The 'hpos' subcommand was added in WooCommerce 8.2.0. Install an older
    # version, which does not have it.

    installation.command.execute(
        ["plugin", "install", "woocommerce", "--version=8.1.0", "--activate"],
    )

    # Prove the premise: the 'hpos' subcommand genuinely doesn't exist on this
    # version, so running it fails with WP-CLI's 'not a registered subcommand'
    # error (rather than failing for some unrelated reason).

    with pytest.raises(CommandFailedError) as excinfo:
        installation.command.execute(
            ["wc", "hpos", "status"],
            include_plugins=["woocommerce"],
        )

    assert "'hpos' is not a registered subcommand of 'wc'" in excinfo.value.stderr

    # is_hpos_enabled must not run into that failure: it returns False instead.

    assert Woocommerce(installation).is_hpos_enabled is False


def test_woocommerce_hpos_status_output_forced_to_english(
    installation_installed_with_activated_woocommerce_plugin: Installation,
) -> None:
    installation = installation_installed_with_activated_woocommerce_plugin

    # Configure the site in Dutch: the core is already downloaded as nl_NL by
    # the fixture, so set the site language and install the WooCommerce Dutch
    # translations. Without the forced en_US locale, 'wp wc hpos status' would
    # then print Dutch (e.g. 'HPOS ingeschakeld?') instead of English.

    installation.command.execute(
        ["option", "update", "WPLANG", "nl_NL"],
        skip_plugins=False,
        skip_themes=False,
    )
    installation.command.execute(
        ["language", "plugin", "install", "woocommerce", "nl_NL"],
        skip_plugins=False,
        skip_themes=False,
    )

    installation.command.execute(
        ["wc", "hpos", "status"],
        skip_plugins=False,
        skip_themes=False,
    )

    first_line = installation.command.stdout.splitlines()[0]

    assert "HPOS enabled?" in first_line
    assert "HPOS ingeschakeld?" not in first_line
