"""Classes for managing database."""

from cyberfusion.DatabaseSupport import DatabaseSupport
from cyberfusion.DatabaseSupport.tables import Table

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.config import Config
from cyberfusion.DatabaseSupport.databases import Database as DatabaseSupportDatabase


class Database:
    """Abstraction of WordPress database."""

    NAME_COMMAND_SEARCH_REPLACE = "search-replace"
    NAME_COMMAND_DB = "db"

    def __init__(self, installation: Installation) -> None:
        """Set attributes and call functions."""
        self.installation = installation

    @property
    def prefix(self) -> str:
        """Get database prefix."""
        self.installation.command.execute(
            [self.NAME_COMMAND_DB, "prefix"],
        )

        return self.installation.command.stdout.rstrip()

    def create_indexes(self, *, dry_run: bool = False) -> list[tuple[str, str]]:
        """Create indexes (sane defaults).

        Returns created indexes. Already existent indexes are ignored.
        """
        database = self.get_database()

        prefix = self.prefix

        indexes_to_create = [
            (f"{prefix}options", "autoload", None),
            (f"{prefix}postmeta", "meta_value", 10),
        ]

        created_indexes = []

        for table_name, column_name, length in indexes_to_create:
            table = Table(database=database, name=table_name)

            existing_indexes = table.get_indexes_by_column(column=column_name)

            index_to_create_exists = any(
                [c.name for c in existing_index.columns] == [column_name]
                for existing_index in existing_indexes
            )

            if index_to_create_exists:
                continue

            lengths = {}

            if length:
                lengths[column_name] = length

            if not dry_run:
                table.create_index(
                    name=column_name, columns=[column_name], lengths=lengths
                )

            created_indexes.append((table_name, column_name))

        return created_indexes

    def get_database(self) -> DatabaseSupportDatabase:
        """Get DatabaseSupport database object."""
        host = Config(self.installation).get_pair("DB_HOST").value
        username = Config(self.installation).get_pair("DB_USER").value
        password = Config(self.installation).get_pair("DB_PASSWORD").value
        name = Config(self.installation).get_pair("DB_NAME").value

        support = DatabaseSupport(
            server_software_names=[DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME],
            server_password=password,
            mariadb_server_host=host,
            mariadb_server_username=username,
        )

        return DatabaseSupportDatabase(
            support=support,
            name=name,
            server_software_name=DatabaseSupport.MARIADB_SERVER_SOFTWARE_NAME,
        )

    def search_replace(self, *, search_string: str, replace_string: str) -> int:
        """Search and replace string in database."""
        self.installation.command.execute(
            [
                self.NAME_COMMAND_SEARCH_REPLACE,
                search_string,
                replace_string,
                "--format=count",
            ],
        )

        return int(self.installation.command.stdout)
