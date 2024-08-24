import os
from typing import Generator

import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.config import Config, Pair, PairType
from cyberfusion.WordPressSupport.core import Core
from cyberfusion.WordPressSupport.exceptions import (
    CommandFailedError,
    PairNotExists,
)


def test_installation_uninstalled_config_create(
    installation_uninstalled: Installation,
    database: Generator[None, None, None],
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


def test_installation_installed_config_create(
    installation_installed: Installation,
    database: Generator[None, None, None],
    database_name: str,
    database_username: str,
    database_password: str,
    database_host: str,
) -> None:
    config = Config(installation_installed)

    with pytest.raises(CommandFailedError):
        config.create(
            database_name=database_name,
            database_username=database_username,
            database_user_password=database_password,
            database_host=database_host,
        )


def test_installation_uninstalled_config_create_tmp_file_removed(
    installation_uninstalled: Installation,
    database: Generator[None, None, None],
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

    assert not os.path.isfile(config._tmp_file_path)


def test_get_pairs(
    installation_installed: Installation,
) -> None:
    pairs = Config(installation_installed).get_pairs()

    assert len(pairs) >= 16  # Differs per environment

    assert pairs[0].name == "table_prefix"
    assert pairs[0].value == "wp_"
    assert pairs[0].type == PairType.VARIABLE


def test_get_pair(
    installation_installed: Installation,
) -> None:
    assert Config(installation_installed).get_pair("DB_CHARSET").name == "DB_CHARSET"


def test_get_pair_not_exists(
    installation_installed: Installation,
) -> None:
    with pytest.raises(PairNotExists):
        Config(installation_installed).get_pair("doesntexist")


def test_update_pair(
    installation_installed: Installation,
) -> None:
    assert Config(installation_installed).get_pair("DB_CHARSET").value == "utf8"

    pair = Pair(
        installation_installed,
        name="DB_CHARSET",
        value="latin1",
        type_=PairType.CONSTANT,
    )
    pair.update()

    assert Config(installation_installed).get_pair("DB_CHARSET").value == "latin1"


def test_shuffle_salts(
    installation_installed: Installation,
) -> None:
    def get_auth_key_value() -> str:
        return Config(installation_installed).get_pair("AUTH_KEY").value

    original_auth_key = get_auth_key_value()

    Config(installation_installed).shuffle_salts()

    new_auth_key = get_auth_key_value()

    assert original_auth_key != new_auth_key
