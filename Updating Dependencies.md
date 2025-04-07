<!--
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
-->

# Updating Type That Tune’s Pinned Dependencies

Type That Tune has a lot of dependencies, and many of them are pinned
for the sake of reproducibility. Here’s what you need to do if you want
to update all of Type That Tune’s pinned dependencies:

1. Open a terminal.

1. Make sure that you have [the Nix package manager](https://nix.dev)
installed by running this command:

    ```bash
    nix-env --version
    ```

    If that command finishes successfully, then you have the Nix package
    manager installed. If that command gives you an error, then you need
    to install the Nix package manager.

    Some of the dependencies in this repository can be updated without
    using the Nix package manager, but you need to Nix package manager
    in order to update all of the dependencies in this repository. In
    some situations, it may make sense to skip the Nix-related parts of
    this guide. If you skip the Nix-related parts of this guide, then
    you won’t be able to update all of this repository’s pinned
    dependencies, but it’ll be better than nothing.

1. Make sure that you have a copy of this repository on your computer.

1. Change directory into the root of this repository by running this
command:

    ```bash
    cd <path-to-repository>
    ```

1. Update the `flake.lock` file by running this command:

    ```bash
    nix --extra-experimental-features 'nix-command flakes' flake update
    ```

1. Check this repository’s flake for errors by running this command:

    ```bash
    nix --extra-experimental-features 'nix-command flakes' flake check
    ```

    If this command reports any warnings or errors, then you should
    probably fix those warnings or errors before continuing.

1. Activate this repository’s dev shell by runing this command:

    ```bash
    nix --extra-experimental-features 'nix-command flakes' develop
    ```

1. Update the [pre-commit](https://pre-commit.com) hook repos by running
this command:

    ```bash
    pre-commit autoupdate
    ```

1. Update the `uv.lock` file by running this command:

    ```bash
    uv lock --upgrade
    ```

1. Synchronize any existing [uv](https://docs.astral.sh/uv) project
environments with the new `uv.lock` file by running this command:

    ```bash
    uv sync
    ```

1. Update the expected versions of the game’s dependencies by running
this command:

    ```bash
    uv run ttt-build-tool \
        build_configuration.toml \
        update_expected_versions
    ```

1. Update the versions of any dependencies that the `ttt-build-tool`
might download by following this procedure:

    1. Check for any potential download errors by running this command:

        <!-- editorconfig-checker-disable -->

        ```bash
        uv run ttt-build-tool \
            build_configuration.toml \
            check_downloadables
        ```

        <!-- editorconfig-checker-enable -->

    1. If there were any errors, then fix them.

    1. Keep repeating those previous two steps until there are no more
    errors.

1. Test the game by following the instructions in [the
README](./README.md). Look out for any new errors or warnings that may
have resulted from any of the dependency updates.

## Sample commit message

You may want to follow the above procedure and then commit the changes.
If you do so, then use this commit message:

<pre>Update pinned dependencies

This commit was created by following the instructions in
Updating Dependencies.md.
</pre>
