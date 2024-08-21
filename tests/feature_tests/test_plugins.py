import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import (
    PluginAlreadyActivatedError,
    PluginAlreadyInstalledError,
)
from cyberfusion.WordPressSupport.plugins import Plugin


def test_plugin_uninstalled_attributes(
    installation_installed: Installation,
) -> None:
    plugin = Plugin(installation_installed, "classic-editor")

    assert not plugin.is_installed
    assert not plugin.is_activated


def test_plugin_install(installation_installed: Installation) -> None:
    plugin = Plugin(installation_installed, "classic-editor")

    plugin.install()


def test_plugin_activate(
    installation_installed_with_unactivated_plugin: Installation,
) -> None:
    plugin = Plugin(
        installation_installed_with_unactivated_plugin, "classic-editor"
    )

    plugin.activate()


def test_plugin_installed_and_activated_attributes(
    installation_installed_with_activated_plugin: Installation,
) -> None:
    plugin = Plugin(
        installation_installed_with_activated_plugin, "classic-editor"
    )

    assert plugin.is_installed
    assert plugin.is_activated

    with pytest.raises(PluginAlreadyInstalledError):
        plugin.install()

    with pytest.raises(PluginAlreadyActivatedError):
        plugin.activate()
