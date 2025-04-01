# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
{
  description = "A flake for working on Type That Tune";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    # This is the last commit in Nixpkgs release-24.11 branch that the
    # right version of Godot in it. Newer commits have newer versions of
    # Godot.
    #
    # editorconfig-checker-disable
    nixpkgsOldStable.url = "github:NixOS/nixpkgs/26eb674c5d0c0c9bb66b6836cc23805bacb532dc";
    # editorconfig-checker-enable
    nixpkgsUnstable.url = "github:NixOS/nixpkgs/nixos-unstable";
    blueprint.url = "github:numtide/blueprint";
  };

  outputs =
    inputs:
    inputs.blueprint {
      inherit inputs;
      prefix = "flake-blueprint-files";
      systems = [ "x86_64-linux" ];
    };
}
