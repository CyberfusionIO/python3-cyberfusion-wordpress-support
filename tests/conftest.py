import os
import shutil
from pathlib import Path
from typing import Generator

import pytest
from _pytest.config.argparsing import Parser
from sqlalchemy_utils import create_database, database_exists, drop_database

from cyberfusion.Common import download_from_url, generate_random_string
from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.config import Config
from cyberfusion.WordPressSupport.core import Core
from cyberfusion.WordPressSupport.plugins import Plugin
from cyberfusion.WordPressSupport.themes import Theme
from cyberfusion.WordPressSupport.wp_cli import WPCLICommand


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--database-username", action="store", required=True)
    parser.addoption("--database-password", action="store", required=True)
    parser.addoption("--database-host", action="store", required=True)


@pytest.fixture
def database_username(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--database-username")


@pytest.fixture
def database_password(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--database-password")


@pytest.fixture
def database_host(request: pytest.FixtureRequest) -> str:
    return request.config.getoption("--database-host")


@pytest.fixture(scope="session")
def wp_cli_binary_path() -> Generator[str, None, None]:
    path = download_from_url(
        "https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar"
    )

    os.chmod(path, 0o755)

    yield path

    os.unlink(path)


@pytest.fixture
def workspace_directory() -> Generator[str, None, None]:
    path = os.path.join(
        os.path.sep, "tmp", "wordpress-" + generate_random_string().lower()
    )

    os.mkdir(path)

    yield path

    shutil.rmtree(path)


@pytest.fixture
def database(
    database_name: str,
    database_username: str,
    database_password: str,
    database_host: str,
) -> Generator[None, None, None]:
    url = (
        "mysql+pymysql://"
        + database_username
        + ":"
        + database_password
        + "@"
        + database_host
        + "/"
        + database_name
    )

    if not database_exists(url):
        create_database(url)

    yield

    drop_database(url)


@pytest.fixture
def wp_cli_command(
    workspace_directory: Generator[str, None, None],
    wp_cli_binary_path: Generator[str, None, None],
) -> WPCLICommand:
    return WPCLICommand(
        workspace_directory,
        workspace_directory,
        binary_path=wp_cli_binary_path,
    )


@pytest.fixture
def installation_uninstalled(
    workspace_directory: Generator[str, None, None],
    database: Generator[None, None, None],
    wp_cli_binary_path: Generator[str, None, None],
) -> Installation:
    return Installation(
        workspace_directory,
        workspace_directory,
        wp_cli_binary_path=wp_cli_binary_path,
    )


@pytest.fixture
def database_name() -> str:
    return generate_random_string()


@pytest.fixture
def installation_installed(
    request,
    workspace_directory: Generator[str, None, None],
    database: Generator[None, None, None],
    database_name: str,
    wp_cli_binary_path: Generator[str, None, None],
    database_username: str,
    database_password: str,
    database_host: str,
) -> Installation:
    if hasattr(request, "param"):
        version = request.param
    else:
        version = "latest"

    installation = Installation(
        workspace_directory,
        workspace_directory,
        wp_cli_binary_path=wp_cli_binary_path,
    )

    core = Core(installation)
    core.download(version=version, locale="nl_NL")

    config = Config(installation)
    config.create(
        database_name=database_name,
        database_username=database_username,
        database_user_password=database_password,
        database_host=database_host,
    )

    core.install(
        url="https://test.nl",
        site_title="Test",
        admin_username="admin",
        admin_password="sqGQNvHZaHxgGzWRnZcLCgLY",
        admin_email_address="example@example.com",
    )

    return installation


@pytest.fixture
def installation_installed_with_unactivated_plugin(
    installation_installed: Installation,
) -> Installation:
    plugin = Plugin(installation_installed, "classic-editor")
    plugin.install()

    return installation_installed


@pytest.fixture
def installation_installed_with_activated_plugin(
    installation_installed: Installation,
) -> Installation:
    plugin = Plugin(installation_installed, "classic-editor")
    plugin.install()
    plugin.activate()

    return installation_installed


@pytest.fixture
def installation_installed_with_activated_elementor_plugin(
    installation_installed: Installation,
) -> Installation:
    plugin = Plugin(installation_installed, "elementor")
    plugin.install()
    plugin.activate()

    return installation_installed


@pytest.fixture
def installation_installed_with_unactivated_theme(
    installation_installed: Installation,
) -> Installation:
    theme = Theme(installation_installed, "twentynineteen")
    theme.install_from_repository()

    return installation_installed


@pytest.fixture
def installation_installed_with_activated_theme(
    installation_installed: Installation,
) -> Installation:
    theme = Theme(installation_installed, "twentynineteen")
    theme.install_from_repository()
    theme.activate()

    return installation_installed
