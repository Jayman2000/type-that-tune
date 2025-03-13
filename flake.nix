# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
{
  description = "A shell for working on Type That Tune";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    # This is the last commit in Nixpkgs release-24.11 branch that the
    # right version of Godot in it. Newer commits have newer versions of
    # Godot.
    nixpkgsOldStable.url = "github:NixOS/nixpkgs/26eb674c5d0c0c9bb66b6836cc23805bacb532dc";
  };

  outputs =
    {
      self,
      nixpkgs,
      nixpkgsOldStable,
    }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      oldStablePkgs = import nixpkgsOldStable { inherit system; };
    in
    {
      devShell.x86_64-linux = pkgs.mkShellNoCC {
        name = "dev-shell-for-reflecting-on-life";
        packages = [
          pkgs.git
          pkgs.nodePackages_latest.livedown
          oldStablePkgs.godot_4
          pkgs.ffmpeg
          pkgs.uv

          pkgs.pre-commit
          # Dependencies for pre-commit hooks:
          pkgs.go
          pkgs.rustc
          pkgs.cabal-install
          pkgs.ghc
        ];
      };
    };
}
