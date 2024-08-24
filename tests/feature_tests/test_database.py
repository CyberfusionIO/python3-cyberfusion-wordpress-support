from cyberfusion.Common import generate_random_string
from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.database import Database


def test_search_replace(
    installation_installed: Installation,
) -> None:
    database = Database(installation_installed)

    assert (
        database.search_replace(
            search_string="wp", replace_string=generate_random_string()
        )
        == 17
    )  # Replaced

    assert (
        database.search_replace(
            search_string=generate_random_string(),
            replace_string=generate_random_string(),
        )
        == 0
    )  # Nothing to replace
