from cyberfusion.DatabaseSupport.tables import Table
from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.database import Database


def test_create_indexes_unrelated_index_exists(
    installation_installed: Installation,
) -> None:
    """Test that if a table has an index for another column, the index is created nonetheless."""
    database = Database(installation_installed)

    Table(database=database.get_database(), name="wp_postmeta").create_index(
        name="extra", columns=["post_id"]
    )

    assert database.create_indexes() == [("wp_postmeta", "meta_value")]

    support_database = database.get_database()

    assert Table(database=support_database, name="wp_postmeta").get_indexes_by_column(
        column="meta_value"
    )
