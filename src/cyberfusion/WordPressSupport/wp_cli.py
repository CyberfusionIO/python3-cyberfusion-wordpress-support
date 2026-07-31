"""Classes for interaction with WP-CLI."""

import json
import os
import subprocess
from importlib.resources import as_file, files
from typing import List, Optional, Union, cast

from _io import TextIOWrapper

from cyberfusion.Common import find_executable
from cyberfusion.WordPressSupport.exceptions import CommandFailedError

RESOURCE_PHP_LOCALE_FORCE = files(__package__) / "force_locale.php"


class WPCLICommand:
    """Abstract WP-CLI implementation for use in scripts."""

    def __init__(
        self,
        path: str,
        *,
        binary_path: Optional[str] = None,
    ) -> None:
        """Construct, execute and validate command execute."""
        self.path = path
        self._binary_path = binary_path

    @property
    def binary_path(self) -> str:
        """Get path to WP-CLI."""
        if self._binary_path:
            return self._binary_path

        return find_executable("wp")

    def execute(
        self,
        command: List[str],
        json_format: bool = False,
        stdin: Optional[TextIOWrapper] = None,
        skip_plugins: Union[bool, List[str]] = True,
        skip_themes: bool = True,
        include_plugins: Optional[List[str]] = None,
    ) -> None:
        """Set attributes and execute command.

        Plugins and themes are skipped by default: their load-time code (e.g.
        a redirect on a login-gated environment) can interfere with the
        command, and most WP-CLI commands do not need them. Skipping is applied
        with WP-CLI's '--skip-plugins' and '--skip-themes' global flags.

        Override this only for commands that need plugins or themes loaded (e.g.
        a plugin-provided command, or activating a plugin so its hooks run):

        - 'include_plugins=[<names>]' loads only the named plugins and skips
          every other one, so a command provided by those plugins works while
          no other plugin can interfere.
        - 'skip_plugins=True' (default) skips all plugins ('--skip-plugins').
        - 'skip_plugins=False' loads all plugins (no flag).
        - 'skip_plugins=[<names>]' skips the named plugins ('--skip-plugins=
          <names>'), i.e. keeps every other plugin loaded. An empty list loads
          all plugins.
        - 'skip_themes' toggles '--skip-themes' the same way (all or nothing).
        """
        if include_plugins is not None:
            skip_plugins = [
                name for name in self._get_plugin_names() if name not in include_plugins
            ]

        # Build and run the command inside 'as_file' so the '--require' file is
        # guaranteed to exist on disk for the duration of the WP-CLI call.

        with as_file(RESOURCE_PHP_LOCALE_FORCE) as locale_force_path:
            self.command = [self.binary_path]
            self.command.append(f"--require={locale_force_path}")
            self.command.extend(command)
            self.command.append(f"--path={self.path}")

            # Add --format if JSON

            if json_format:
                self.command.append("--format=json")

            # Skip plugins and themes

            if skip_plugins is True:
                self.command.append("--skip-plugins")
            elif isinstance(skip_plugins, list) and skip_plugins:
                self.command.append("--skip-plugins=" + ",".join(skip_plugins))

            if skip_themes:
                self.command.append("--skip-themes")

            # Execute command

            try:
                output = subprocess.run(
                    self.command,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=self.path,
                    env=os.environ.copy()
                    | {
                        "PWD": self.path,
                    },
                    stdin=stdin,
                )
            except subprocess.CalledProcessError as e:
                raise CommandFailedError(
                    command=self.command,
                    return_code=e.returncode,
                    stdout=e.stdout,
                    stderr=e.stderr,
                )

        # Set attributes

        self.stdout = output.stdout.rstrip("\n")

        # Cast if JSON

        if json_format:
            self.stdout = json.loads(self.stdout)

    def _get_plugin_names(self) -> List[str]:
        """Get names of all plugins.

        Listing skips all plugins (the default), so their load-time code cannot
        interfere. Despite skipping them, WP-CLI still reports every plugin.
        """
        self.execute(["plugin", "list", "--field=name"], json_format=True)

        return cast(List[str], self.stdout)
