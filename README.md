<!--
SPDX-License-Identifier: CC0-1.0
SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
-->

# Type That Tune

## Building and running the game from source

1. Make sure that you have a copy of this repo on your computer. If you
aren’t sure how to do this, then please click [here].

2. Make sure that you have [Godot] v4.2.2 installed.

    If you use [the Nix package manager], then you may want to use this
    repo’s flake in order to ensure that you have the right version of
    Godot. Here’s what you need to do in order to use this repo’s flake:

    1. Open a terminal.

    2. Change directory to the root of this repo by running this
    command:

        ```bash
        cd <path-to-repo>
        ```

    3. Activate the flake’s `devShell` by running this command:

        ```bash
        nix \
            --extra-experimental-features nix-command \
            --extra-experimental-features flakes \
            develop
        ```

3. Open Godot.

    If you’re using the Nix flake that I mentioned earlier, then you can
    open the correct version of Godot by running this command:

    ```bash
    godot4
    ```

4. Click “Import”.

5. In the “Open a File or Directory” window, navigate to the root of
this repo.

6. Click on the `project/` folder.

7. Click “Select This Folder”.

8. Click “Import &amp; Edit”.

9. Press <kbd>F5</kbd> to run the game.

<!-- editorconfig-checker-disable -->
[Godot]: https://godotengine.org
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

[1]: https://pre-commit.com
[2]: https://pre-commit.com/#quick-start
[3]: https://pre-commit.com/#2-add-a-pre-commit-configuration

## Copying

See [`copying.md`](./copying.md).
