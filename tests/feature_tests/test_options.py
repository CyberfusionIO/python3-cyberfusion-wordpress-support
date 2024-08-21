import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import OptionNotExists
from cyberfusion.WordPressSupport.options import Option, Options


def test_get_options(
    installation_installed: Installation,
) -> None:
    options = Options(installation_installed).get()

    assert (
        len(options) > 117
    )  # At the time of writing, increases with WordPress updates


def test_get_single_option(
    installation_installed: Installation,
) -> None:
    assert (
        Options(installation_installed).get_single("default_role").name
        == "default_role"
    )


def test_get_single_option_not_exists(
    installation_installed: Installation,
) -> None:
    with pytest.raises(OptionNotExists):
        Options(installation_installed).get_single("doesntexist")


def test_get_option_with_string_value(
    installation_installed: Installation,
) -> None:
    assert (
        Options(installation_installed).get_single("default_role").value
        == "subscriber"
    )


def test_get_option_with_integer_value(
    installation_installed: Installation,
) -> None:
    assert (
        Options(installation_installed).get_single("use_trackback").value == 0
    )


def test_update_option(
    installation_installed: Installation,
) -> None:
    assert (
        Options(installation_installed).get_single("comment_moderation").value
        == 0
    )

    option = Option(installation_installed, name="comment_moderation", value=1)
    option.update()

    assert (
        Options(installation_installed).get_single("comment_moderation").value
        == 1
    )
