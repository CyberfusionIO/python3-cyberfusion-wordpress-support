from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.config import PairType, Pair


def test_update_pair_not_exists(
    installation_installed: Installation,
) -> None:
    pair = Pair(
        installation_installed,
        name="doesntexist",
        value="value",
        type_=PairType.CONSTANT,
    )

    pair.update()
