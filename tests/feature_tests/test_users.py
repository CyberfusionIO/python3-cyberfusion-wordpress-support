from cyberfusion.Common import generate_random_string
from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.users import User, Users


def test_get_users_without_role(
    installation_installed: Installation,
) -> None:
    users = Users(installation_installed).get()

    assert len(users) == 1

    assert users[0].id == 1


def test_get_users_with_role_present(
    installation_installed: Installation,
) -> None:
    users = Users(installation_installed).get(role="administrator")

    assert len(users) == 1

    assert users[0].id == 1


def test_get_users_with_role_absent(
    installation_installed: Installation,
) -> None:
    users = Users(installation_installed).get(role="subscriber")

    assert not users


def test_get_user_one_time_login_url(
    installation_installed: Installation,
) -> None:
    user = User(installation_installed, id_=1)

    assert (
        "/wp-login.php?user_id=1&one_time_login_token=" in user.get_one_time_login_url()
    )


def test_update_user_password(
    installation_installed: Installation,
) -> None:
    user = User(installation_installed, id_=1)

    user.update_password(generate_random_string())
