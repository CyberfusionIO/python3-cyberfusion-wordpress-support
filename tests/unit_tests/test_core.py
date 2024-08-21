import os
from typing import Generator

import pytest

from cyberfusion.WordPressSupport import Installation
from cyberfusion.WordPressSupport.core import Core
from cyberfusion.WordPressSupport.exceptions import DirectoryNotEmptyError


def test_instance_download_directory_not_empty(
    installation_uninstalled: Installation,
    workspace_directory: Generator[str, None, None],
) -> None:
    with open(os.path.join(workspace_directory, "test.txt"), "w"):
        pass

    with pytest.raises(DirectoryNotEmptyError):
        core = Core(installation_uninstalled)

        core.download(version="latest", locale="nl_NL")
