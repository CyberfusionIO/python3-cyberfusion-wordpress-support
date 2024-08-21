import os

import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.config import Config
from cyberfusion.WordPressSupport.core import Core
from cyberfusion.WordPressSupport.exceptions import (
    CommandFailedError,
    CoreAlreadyInstalledError,
)
from tests.conftest import database_host, database_name

VERSION = "6.4.2"


def test_uninstalled_core_attributes(
    installation_uninstalled: Installation,
) -> None:
    core = Core(installation_uninstalled)

    assert not core.is_installed


def test_installed_core_attributes(
    installation_installed: Installation,
) -> None:
    core = Core(installation_installed)

    assert core.is_installed
    assert core.version.count(".") == 2


@pytest.mark.parametrize("installation_installed", [(VERSION,)], indirect=True)
def test_installed_core_update_latest(
    installation_installed: Installation,
) -> None:
    core = Core(installation_installed)

    assert core.version == VERSION

    core.update()

    assert core.version != VERSION


@pytest.mark.parametrize("installation_installed", [(VERSION,)], indirect=True)
def test_installed_core_update_minor(
    installation_installed: Installation,
) -> None:
    core = Core(installation_installed)

    assert core.version == VERSION

    core.update(only_update_minor=True)

    assert core.version != VERSION
    assert core.version.startswith("6.")


@pytest.mark.parametrize("installation_installed", [(VERSION,)], indirect=True)
def test_installed_core_update_specific(
    installation_installed: Installation,
) -> None:
    NEW_VERSION = "6.4.3"

    core = Core(installation_installed)

    assert core.version == VERSION

    core.update(version=NEW_VERSION)

    assert core.version == NEW_VERSION


def test_uninstalled_core_download(
    installation_uninstalled: Installation,
) -> None:
    core = Core(installation_uninstalled)

    core.download(version="latest", locale="nl_NL")


def test_uninstalled_core_install(
    installation_uninstalled: Installation,
    database_name: str,
    database_username: str,
    database_password: str,
    database_host: str,
) -> None:
    core = Core(installation_uninstalled)
    core.download(version="latest", locale="nl_NL")

    config = Config(installation_uninstalled)
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


def test_installed_core_install(
    installation_installed: Installation,
) -> None:
    core = Core(installation_installed)

    with pytest.raises(CoreAlreadyInstalledError):
        core.install(
            url="https://test.nl",
            site_title="Test",
            admin_username="admin",
            admin_password="sqGQNvHZaHxgGzWRnZcLCgLY",
            admin_email_address="example@example.com",
        )


def test_uninstalled_core_install_tmp_file_removed(
    installation_uninstalled: Installation,
    database_name: str,
    database_username: str,
    database_password: str,
    database_host: str,
) -> None:
    core = Core(installation_uninstalled)
    core.download(version="latest", locale="nl_NL")

    config = Config(installation_uninstalled)
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

    assert not os.path.isfile(core._tmp_file_path)


def test_installed_core_download_existing_files_force(
    installation_installed: Installation,
) -> None:
    core = Core(installation_installed)

    assert os.listdir(installation_installed.command.path)

    core.download(version="latest", locale="nl_NL", force=True)
