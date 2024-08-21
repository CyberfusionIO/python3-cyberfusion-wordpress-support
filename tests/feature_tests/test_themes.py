import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import (
    ThemeAlreadyActivatedError,
    ThemeNotInstalledError,
    URLMissesThemeError,
)
from cyberfusion.WordPressSupport.themes import Theme


def test_theme_uninstalled_attributes(
    installation_installed: Installation,
) -> None:
    theme = Theme(installation_installed, "twentynineteen")

    assert not theme.is_installed
    assert not theme.is_activated

    with pytest.raises(ThemeNotInstalledError):
        theme.version


def test_theme_install_from_repository_not_installed(
    installation_installed: Installation,
) -> None:
    theme = Theme(installation_installed, "twentynineteen")

    theme.install_from_repository()


def test_theme_install_from_repository_installed(
    installation_installed_with_activated_theme: Installation,
) -> None:
    theme = Theme(
        installation_installed_with_activated_theme, "twentynineteen"
    )

    theme.install_from_repository()


def test_theme_install_from_repository_with_version(
    installation_installed_with_activated_theme: Installation,
) -> None:
    theme = Theme(
        installation_installed_with_activated_theme, "twentynineteen"
    )

    assert theme.version != "2.3"

    theme.install_from_repository(version="2.3")

    assert theme.version == "2.3"


def test_get_theme_name_by_zip_file(
    installation_installed: Installation,
):
    assert (
        Theme.get_theme_name_by_zip_file(
            "https://downloads.wordpress.org/theme/neve.3.4.9.zip"
        )
        == "neve"
    )


def test_theme_install_from_url_wrong_name(
    installation_installed_with_activated_theme: Installation,
) -> None:
    theme = Theme(
        installation_installed_with_activated_theme, "twentynineteen"
    )

    with pytest.raises(URLMissesThemeError):
        theme.install_from_url(
            url="https://downloads.wordpress.org/theme/neve.3.4.9.zip"
        )


def test_theme_install_from_url_not_installed(
    installation_installed: Installation,
) -> None:
    theme = Theme(installation_installed, "twentynineteen")

    theme.install_from_url(
        url="https://downloads.wordpress.org/theme/twentynineteen.2.4.zip"
    )


def test_theme_install_from_url_installed(
    installation_installed_with_activated_theme: Installation,
) -> None:
    theme = Theme(
        installation_installed_with_activated_theme, "twentynineteen"
    )

    assert theme.version != "2.3"

    theme.install_from_url(
        url="https://downloads.wordpress.org/theme/twentynineteen.2.3.zip"
    )

    assert theme.version == "2.3"


def test_theme_activate(
    installation_installed_with_unactivated_theme: Installation,
) -> None:
    theme = Theme(
        installation_installed_with_unactivated_theme, "twentynineteen"
    )

    theme.activate()


def test_theme_installed_and_activated_attributes(
    installation_installed_with_activated_theme: Installation,
) -> None:
    theme = Theme(
        installation_installed_with_activated_theme, "twentynineteen"
    )

    assert theme.is_installed
    assert theme.is_activated

    with pytest.raises(ThemeAlreadyActivatedError):
        theme.activate()

    assert theme.version
