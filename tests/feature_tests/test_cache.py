from pytest_mock import MockerFixture  # type: ignore[attr-defined]

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.cache import Cache
from cyberfusion.WordPressSupport.wp_cli import WPCLICommand


def test_cache_flush(
    installation_installed: Installation,
) -> None:
    Cache(installation_installed).flush()


def test_cache_flush_regenerate_elementor_css(
    mocker: MockerFixture,
    installation_installed_with_activated_elementor_plugin: Installation,
) -> None:
    spy_execute = mocker.spy(WPCLICommand, "execute")

    Cache(installation_installed_with_activated_elementor_plugin).flush()

    elementor_call = next(
        call
        for call in spy_execute.call_args_list
        if call.args[1] == ["elementor", "flush-css"]
    )

    assert elementor_call.kwargs["include_plugins"] == ["elementor"]


def test_cache_flush_no_regenerate_elementor_css(
    mocker: MockerFixture,
    installation_installed: Installation,
) -> None:
    spy_execute = mocker.spy(WPCLICommand, "execute")

    Cache(installation_installed).flush()

    assert (
        mocker.call(mocker.ANY, ["elementor", "flush-css"])
        not in spy_execute.call_args_list
    )
