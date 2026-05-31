import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import (
    PluginAlreadyActivatedError,
    PluginAlreadyInstalledError,
)
from cyberfusion.WordPressSupport.plugins import Plugin, Plugins, PluginStatus


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
    plugin = Plugin(installation_installed_with_unactivated_plugin, "classic-editor")

    plugin.activate()


def test_plugin_installed_and_activated_attributes(
    installation_installed_with_activated_plugin: Installation,
) -> None:
    plugin = Plugin(installation_installed_with_activated_plugin, "classic-editor")

    assert plugin.is_installed
    assert plugin.is_activated

    with pytest.raises(PluginAlreadyInstalledError):
        plugin.install()

    with pytest.raises(PluginAlreadyActivatedError):
        plugin.activate()


def test_get_plugins_without_status(
    installation_installed: Installation,
) -> None:
    plugin = Plugin(installation_installed, "classic-editor")

    plugin.install()

    plugins = Plugins(installation_installed).get()

    assert len(plugins) == 3

    assert any(plugin.name == "akismet" for plugin in plugins)
    assert any(plugin.name == "hello" for plugin in plugins)
    assert any(plugin.name == "classic-editor" for plugin in plugins)


def test_get_plugins_with_status(
    installation_installed: Installation,
) -> None:
    plugin = Plugin(installation_installed, "classic-editor")

    plugin.install()
    plugin.activate()

    plugins = Plugins(installation_installed).get(status=PluginStatus.ACTIVE)

    assert len(plugins) == 1

    assert plugins[0].name == "classic-editor"
