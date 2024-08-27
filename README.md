<!--
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
-->

# Type That Tune

## Hints for Contributors

- If you use [the Nix package manager](https://nix.dev), then you might
be interested in the flake that this repo provides. You can run the
following command in order to start a shell with all of the tools
that you need in order to work on this project:

    ```bash
    nix \
        --extra-experimental-features nix-command \
        --extra-experimental-features flakes \
        develop
    ```

- You can use [pre-commit][1] to automatically check your contributions.
Follow [these instructions][2] to get started. Skip [the part about
creating a pre-commit configuration][3].
- Try to keep lines shorter than seventy-three characters.
- This repo uses an [EditorConfig](https://editorconfig.org) file.
- Use [CommonMark](https://commonmark.org) for Markdown files.

[1]: https://pre-commit.com
[2]: https://pre-commit.com/#quick-start
[3]: https://pre-commit.com/#2-add-a-pre-commit-configuration

## Copying

See [`copying.md`](./copying.md).
