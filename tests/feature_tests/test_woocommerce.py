import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import WoocommerceNotInstalledError
from cyberfusion.WordPressSupport.woocommerce import Woocommerce


def test_woocommerce_is_hpos_enabled_woocommerce_not_installed(
    installation_installed: Installation,
) -> None:
    with pytest.raises(WoocommerceNotInstalledError):
        Woocommerce(installation_installed).is_hpos_enabled


def test_woocommerce_is_hpos_enabled(
    installation_installed_with_activated_woocommerce_plugin: Installation,
) -> None:
    installation = installation_installed_with_activated_woocommerce_plugin

    installation.command.execute(["wc", "hpos", "enable"])

    assert Woocommerce(installation).is_hpos_enabled


def test_woocommerce_is_hpos_disabled(
    installation_installed_with_activated_woocommerce_plugin: Installation,
) -> None:
    installation = installation_installed_with_activated_woocommerce_plugin

    installation.command.execute(["wc", "hpos", "disable"])

    assert not Woocommerce(installation).is_hpos_enabled
