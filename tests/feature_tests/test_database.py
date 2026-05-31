from cyberfusion.Common import generate_random_string
from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.databases import Database as DatabaseSupportDatabase
from cyberfusion.DatabaseSupport.tables import Table
from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.database import Database


def test_search_replace(
    installation_installed: Installation,
) -> None:
    database = Database(installation_installed)

    assert database.search_replace(
        search_string="wp", replace_string=generate_random_string()
    )

    assert (
        database.search_replace(
            search_string=generate_random_string(),
            replace_string=generate_random_string(),
        )
        == 0
    )  # Nothing to replace


def test_prefix(installation_installed: Installation) -> None:
    database = Database(installation_installed)

    assert database.prefix == "wp_"


def test_get_database(
    installation_installed: Installation,
    database_name: str,
    database_username: str,
    database_password: str,
    database_host: str,
) -> None:
    database = Database(installation_installed)

    support_database = database.get_database()

    assert isinstance(support_database, DatabaseSupportDatabase)

    assert support_database.name == database_name
    assert (
        support_database.server_software_name
        == DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME
    )
    assert support_database.support.mariadb_server_host == database_host
    assert support_database.support.mariadb_server_username == database_username
    assert support_database.support.server_password == database_password


def test_create_indexes_autoload_created(
    installation_installed: Installation,
) -> None:
    """Verify the `wp_options.autoload` index is created.

    WordPress' default schema already adds `KEY autoload (autoload)`
    (https://github.com/WordPress/WordPress/commit/716958625410ff83a3ae4ff46bb74b2eebcf41a5),
    so we drop it first to test that our logic creates it.
    """
    database = Database(installation_installed)

    support_database = database.get_database()

    indexes = {
        index.name: index
        for index in Table(
            database=support_database, name="wp_options"
        ).reflection.indexes
    }

    indexes["autoload"].drop(bind=support_database.database_engine)

    assert ("wp_options", "autoload") in database.create_indexes()

    support_database = database.get_database()

    indexes = {
        index.name: index
        for index in Table(
            database=support_database, name="wp_options"
        ).reflection.indexes
    }

    assert "autoload" in indexes

    assert indexes["autoload"].dialect_options["mysql"]["length"] is None


def test_create_indexes_meta_value_created(
    installation_installed: Installation,
) -> None:
    """Verify the `wp_postmeta.meta_value` index is created (with prefix length)."""
    database = Database(installation_installed)

    assert ("wp_postmeta", "meta_value") in database.create_indexes()

    support_database = database.get_database()

    indexes = {
        index.name: index
        for index in Table(
            database=support_database, name="wp_postmeta"
        ).reflection.indexes
    }

    assert "meta_value" in indexes

    assert indexes["meta_value"].dialect_options["mysql"]["length"] == {
        "meta_value": 10
    }


def test_create_indexes_already_exist(installation_installed: Installation) -> None:
    database = Database(installation_installed)

    assert len(database.create_indexes()) > 0

    assert len(database.create_indexes()) == 0


def test_create_indexes_dry_run(installation_installed: Installation) -> None:
    """Verify that with `dry_run=True`, indexes to create are returned but not created."""

    def get_indexes() -> dict:
        return {
            (table.name, index.name)
            for table in database.get_database().metadata.tables.values()
            for index in table.indexes
        }

    database = Database(installation_installed)

    indexes_before = get_indexes()

    created_indexes = database.create_indexes(dry_run=True)

    assert len(created_indexes) > 0

    indexes_after = get_indexes()

    assert indexes_after == indexes_before
