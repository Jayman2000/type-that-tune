# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024 Jason Yundt <jason@jasonyundt.email>
{
  description = "A shell for working on Type That Tune";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    nixpkgsUnstable.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    {
      self,
      nixpkgs,
      nixpkgsUnstable,
    }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      unstablePkgs = import nixpkgsUnstable { inherit system; };
    in
    {
      devShell.x86_64-linux = pkgs.mkShellNoCC {
        name = "dev-shell-for-reflecting-on-life";
        packages =
          let
            # One of this repo’s pre-commit hooks requires Python
            # 3.12. Unfortunately, the version of pre-commit in
            # nixpkgs defaults to using an older version of Python.
            # That’s why we have to do an override here.
            customPre-commit = pkgs.pre-commit.override {
              python3Packages = pkgs.python312Packages;
            };
          in
          [
            pkgs.git
            pkgs.nodePackages_latest.livedown
            pkgs.godot_4
            pkgs.ffmpeg
            # Unfortunately, the version of uv that’s in pkgs isn’t
            # new enough, so we have to use unstablePkgs here.
            unstablePkgs.uv

            customPre-commit
            # Dependencies for pre-commit hooks:
            pkgs.go
            pkgs.rustc
          ];
      };
    };
}
