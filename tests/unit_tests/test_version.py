import pytest

from cyberfusion.WordPressSupport.version import Version


def test_version_parses_parts() -> None:
    assert Version("7.1.0").parts == (7, 1, 0)


def test_version_parses_suffix_without_error() -> None:
    assert Version("7.1.0-beta.1").parts == (7, 1, 0, 1)


def test_version_ordering() -> None:
    assert Version("7.0.0") < Version("7.1.0")
    assert Version("7.1.0") > Version("7.0.9")
    assert Version("7.1.0") <= Version("7.1.0")
    assert Version("7.1.0") >= Version("7.1.0")


def test_version_missing_trailing_parts_treated_as_zero() -> None:
    assert Version("7.1") == Version("7.1.0")
    assert not (Version("7.1") < Version("7.1.0"))


def test_version_equal_versions_hash_equal() -> None:
    assert hash(Version("7.1")) == hash(Version("7.1.0"))


def test_version_equality_with_non_version_is_not_equal() -> None:
    assert Version("7.1.0") != "7.1.0"
    assert Version("7.1.0") != 710


def test_version_ordering_with_non_version_is_not_implemented() -> None:
    with pytest.raises(TypeError):
        Version("7.1.0") < "7.1.0"  # type: ignore[operator]


def test_version_repr() -> None:
    assert repr(Version("7.1.0")) == "Version('7.1.0')"
