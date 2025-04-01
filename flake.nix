# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
{
  description = "A flake for working on Type That Tune";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
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
