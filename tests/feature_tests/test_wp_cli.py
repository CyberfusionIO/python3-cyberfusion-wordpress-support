from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.plugins import Plugin


def test_get_plugin_names(installation_installed: Installation) -> None:
    Plugin(installation_installed, "classic-editor").install()

    names = installation_installed.command._get_plugin_names()

    assert "classic-editor" in names


def test_command_include_plugins_excludes_other_plugins(
    installation_installed: Installation,
) -> None:
    Plugin(installation_installed, "classic-editor").install()

    installation_installed.command.execute(
        ["--info"], include_plugins=["classic-editor"]
    )

    skip_plugins_argument = next(
        argument
        for argument in installation_installed.command.command
        if argument.startswith("--skip-plugins=")
    )

    assert "classic-editor" not in skip_plugins_argument
    assert "akismet" in skip_plugins_argument
    assert "hello" in skip_plugins_argument
