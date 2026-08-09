import os

import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.exceptions import RedisObjectCacheNotInstalledError
from cyberfusion.WordPressSupport.redis_object_cache import RedisObjectCache


def get_drop_in_path(installation: Installation) -> str:
    return os.path.join(installation.command.path, "wp-content", "object-cache.php")


def test_redis_object_cache_enable_plugin_not_activated(
    installation_installed: Installation,
) -> None:
    with pytest.raises(RedisObjectCacheNotInstalledError):
        RedisObjectCache(installation_installed).enable()


def test_redis_object_cache_disable_plugin_not_activated(
    installation_installed: Installation,
) -> None:
    with pytest.raises(RedisObjectCacheNotInstalledError):
        RedisObjectCache(installation_installed).disable()


def test_redis_object_cache_enable(
    installation_installed_with_activated_redis_cache_plugin: Installation,
) -> None:
    installation = installation_installed_with_activated_redis_cache_plugin

    RedisObjectCache(installation).enable()

    assert os.path.isfile(get_drop_in_path(installation))


def test_redis_object_cache_disable(
    installation_installed_with_activated_redis_cache_plugin: Installation,
) -> None:
    installation = installation_installed_with_activated_redis_cache_plugin

    RedisObjectCache(installation).enable()
    RedisObjectCache(installation).disable()

    assert not os.path.isfile(get_drop_in_path(installation))
