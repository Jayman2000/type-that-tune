<!--
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
-->

# Type That Tune

Type That Tune is a typing game for crazy people.

## Building and running the game from source

1. Make sure that you have a copy of this repo on your computer. If you
aren’t sure how to do this, then please click [here].

2. Open a terminal.

3. Change directory to the root of this repo by running this command:

    ```bash
    cd <path-to-repo>
    ```

4. Make sure that you have the following installed:

    - [uv](https://docs.astral.sh/uv/)
    - [FFmpeg](https://www.ffmpeg.org)

    If you use [the Nix package manager], then you may want to use this
    repo’s flake in order to ensure that you have all of those
    dependencies installed. To do so, run this command:

    ```bash
    nix \
        --extra-experimental-features nix-command \
        --extra-experimental-features flakes \
        develop
    ```

5. Prepare the Godot project folder and open it in the Godot Engine
editor:

    - If you ran the `nix` command from the previous step, then run this
    command:

        ```bash
        uv run ttt-build-tool \
            --godot-editor-path "$GODOT_EDITOR_PATH" \
            open_project_in_editor
        ```

    - Otherwise, run this command:

        ```bash
        uv run ttt-build-tool open_project_in_editor
        ```

    **Warning:** This step will take a really long time. Please be
    patient.

6. Press <kbd>F5</kbd> to run the game.

<!-- editorconfig-checker-disable -->
[here]: https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository
[the Nix package manager]: https://nix.dev
<!-- editorconfig-checker-enable -->

## Hints for Contributors

- If you use [the Nix package manager], then you might want to read
through [`flake.nix`](./flake.nix). Take a look at some of the packages
that I use when developing Type That Tune. They might be helpful to you
when you’re working on contributing to Type That Tune.
- You can use [pre-commit][1] to automatically check your contributions.
Follow [these instructions][2] to get started. Skip [the part about
creating a pre-commit configuration][3].
- Try to keep lines shorter than seventy-three characters.
- This repo uses an [EditorConfig](https://editorconfig.org) file.
- Use [CommonMark](https://commonmark.org) for Markdown files.
- If you’re using [NixOS](https://nixos.org), then the
[ruff](https://docs.astral.sh/ruff/) pre-commit hook probably won’t
work. Here’s how you fix it:

    1. Set the `PIP_NO_BINARY` environment variable to “ruff”.
    2. Run `pre-commit clean`
    3. Run `pre-commit install-hooks`

[1]: https://pre-commit.com
[2]: https://pre-commit.com/#quick-start
[3]: https://pre-commit.com/#2-add-a-pre-commit-configuration

## Copying

See [`copying.md`](./copying.md).
