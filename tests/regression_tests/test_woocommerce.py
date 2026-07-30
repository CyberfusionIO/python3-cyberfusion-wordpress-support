from cyberfusion.WordPressSupport import Installation


def test_woocommerce_hpos_status_output_forced_to_english(
    installation_installed_with_activated_woocommerce_plugin: Installation,
) -> None:
    installation = installation_installed_with_activated_woocommerce_plugin

    # Configure the site in Dutch: the core is already downloaded as nl_NL by
    # the fixture, so set the site language and install the WooCommerce Dutch
    # translations. Without the forced en_US locale, 'wp wc hpos status' would
    # then print Dutch (e.g. 'HPOS ingeschakeld?') instead of English.

    installation.command.execute(["option", "update", "WPLANG", "nl_NL"])
    installation.command.execute(
        ["language", "plugin", "install", "woocommerce", "nl_NL"]
    )

    installation.command.execute(["wc", "hpos", "status"])

    first_line = installation.command.stdout.splitlines()[0]

    assert "HPOS enabled?" in first_line
    assert "HPOS ingeschakeld?" not in first_line
