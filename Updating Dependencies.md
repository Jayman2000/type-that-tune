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

1. Update the version of the Godot Engine that Type That Tune uses by
following this procedure:

    1. Determine the correct version of the Godot Engine by running this
    command:

        ```bash
        godot4 --version
        ```

        This should display the version of Godot that’s used by this
        repopository’s flake. That version of Godot might not be the
        latest stable upstream version of Godot. Personally, I choose to
        use a potentially outdated version of Godot because it’s more
        convenient to do so. I could have chosen to just use the latest
        stable upstream version of Godot, but then I would have to
        constantly mess with this repository’s flake’s Nix expression in
        order to make it use the right version.

        The version number will end with `nixpkgs.<hash>`. Please ignore
        that part of the version number.

        Write this version number down somewhere so that you don’t
        forget it part way through this process.

    1. Update the URL for the version of the Godot Engine editor that
    the `ttt-build-tool` downloads by following this proceedure:

        1. Open <!-- editorconfig-checker-disable -->
        `python_distribution_packages/ttt-build-tool/ttt_build_tool/common.py`
        in a text editor. <!-- editorconfig-checker-enable -->

        1. Find the `GodotEditorSearchTuple` class definition.

        1. Find that class definition’s `downloaded_godot_editor_path`
        method definition.

        1. Find that method definition’s `download_if_needed` function
        call.

        1. The first argument that’s passed to that function is a URL.
        Change that URL so that it downloads the correct version of
        the Godot editor.

        1. The third argument that’s passed to that function is a hash.
        Change the hash to `"Hash to be determined"`. We’ll figure out
        what the actual hash is in another step.

        1. Trigger a download error by running this command:

            ```bash
            uv run ttt-build-tool \
                build_configuration.toml \
                open_in_editor
            ```

            The error message that that command produces should contain
            the actual hash for the file that was downloaded.

        1. Go back to where you wrote `"Hash to be determined"`, and
        replace it with the actual hash from the error message.

    1. Update the URL for the version of the Godot Engine export
    templates that the `ttt-build-tool` downloads by following this
    proceedure:

        1. If you don’t still have it open,
        open <!-- editorconfig-checker-disable -->
        `python_distribution_packages/ttt-build-tool/ttt_build_tool/common.py`
        in a text editor. <!-- editorconfig-checker-enable -->

        1. Find the `GodotExportTemplatesSearchTuple` class definition.

        1. Find that class definition’s
        `downloaded_godot_export_templates_path` method definition.

        1. Find that method definition’s `download_if_needed` function
        call.

        1. The first argument that’s passed to that function is a URL.
        Change that URL so that it downloads the correct version of
        the Godot export templates.

        1. The third argument that’s passed to that function is a hash.
        Change the hash to `"Hash to be determined"`. We’ll figure out
        what the actual hash is in another step.

        1. Trigger a download error by running this command:

            ```bash
            uv run ttt-build-tool \
                build_configuration.toml \
                ensure_export_templates_symlink
            ```

            The error message that that command produces should contain
            the actual hash for the file that was downloaded.

        1. Go back to where you wrote `"Hash to be determined"`, and
        replace it with the actual hash from the error message.

    1. Update the version of the Godot Engine that the Godot project
    expects by following this procedure:

        1. Open
        `godot_project/scenes_and_scripts/autoload/startup_checker.gd`
        in a text editor.

        1. Find the `_init` function definition.

        1. Find that function definition’s `EXPECTED_GODOT_VERSION`
        constant definition.

        1. Change that constant’s value so that so that it matches the
        correct Godot Engine version.

1. Test the game by following the instructions in [the
README](./README.md). Look out for any new errors or warnings that may
have resulted from any of the dependency updates.

## Sample commit message

You may want to follow the above procedure and then commit the changes.
If you do so, then use this commit message:

<pre>Update pinned dependencies

This commit was created by following the instructions in
Updating Dependencies.md
</pre>
