import pytest

from cyberfusion.Common import generate_random_string
from cyberfusion.Common.exceptions import ExecutableNotFound
from cyberfusion.WordPressSupport.exceptions import CommandFailedError
from cyberfusion.WordPressSupport.wp_cli import WPCLICommand


def test_command_not_json(
    wp_cli_command: WPCLICommand,
) -> None:
    wp_cli_command.execute(["--info"])

    assert wp_cli_command.stdout.startswith("OS:")


def test_command_requires_locale_force_file(
    wp_cli_command: WPCLICommand,
) -> None:
    wp_cli_command.execute(["--info"])

    require_arguments = [
        argument
        for argument in wp_cli_command.command
        if argument.startswith("--require=")
    ]

    assert len(require_arguments) == 1
    assert require_arguments[0].endswith("/force_locale.php")


def test_command_json(wp_cli_command: WPCLICommand) -> None:
    wp_cli_command.execute(["--info"], json_format=True)

    assert "system_os" in wp_cli_command.stdout


def test_raises_exception(wp_cli_command: WPCLICommand) -> None:
    with pytest.raises(CommandFailedError) as e:
        wp_cli_command.execute(["doesntexist"])

    assert e.value.command is not None
    assert e.value.return_code is not None
    assert e.value.stdout is not None
    assert e.value.stderr is not None
    assert e.value.streams is not None


def test_binary_path_set(wp_cli_command: WPCLICommand) -> None:
    WP_CLI_PATH = generate_random_string()

    wp_cli_command = WPCLICommand(wp_cli_command.path, binary_path=WP_CLI_PATH)

    assert wp_cli_command.binary_path == WP_CLI_PATH


def test_binary_path_unset(wp_cli_command: WPCLICommand) -> None:
    wp_cli_command = WPCLICommand(wp_cli_command.path, binary_path=None)

    with pytest.raises(ExecutableNotFound):
        wp_cli_command.binary_path


def test_command_skips_plugins_and_themes_by_default(
    wp_cli_command: WPCLICommand,
) -> None:
    wp_cli_command.execute(["--info"])

    assert "--skip-plugins" in wp_cli_command.command
    assert "--skip-themes" in wp_cli_command.command


def test_command_skip_all_plugins(wp_cli_command: WPCLICommand) -> None:
    wp_cli_command.execute(["--info"], skip_plugins=True)

    assert "--skip-plugins" in wp_cli_command.command


def test_command_loads_plugins(wp_cli_command: WPCLICommand) -> None:
    wp_cli_command.execute(["--info"], skip_plugins=False)

    assert not any(
        argument.startswith("--skip-plugins") for argument in wp_cli_command.command
    )


def test_command_loads_themes(wp_cli_command: WPCLICommand) -> None:
    wp_cli_command.execute(["--info"], skip_themes=False)

    assert "--skip-themes" not in wp_cli_command.command


def test_command_skip_specific_plugins(wp_cli_command: WPCLICommand) -> None:
    wp_cli_command.execute(["--info"], skip_plugins=["foo", "bar"])

    assert "--skip-plugins=foo,bar" in wp_cli_command.command
    assert "--skip-plugins" not in wp_cli_command.command  # Not the bare flag


def test_command_skip_specific_plugins_empty_loads_all(
    wp_cli_command: WPCLICommand,
) -> None:
    wp_cli_command.execute(["--info"], skip_plugins=[])

    assert not any(
        argument.startswith("--skip-plugins") for argument in wp_cli_command.command
    )
