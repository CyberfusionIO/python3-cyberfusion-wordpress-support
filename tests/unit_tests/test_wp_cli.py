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
