# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2024–2025 Jason Yundt <jason@jasonyundt.email>
{
  perSystem,
  pkgs,
}:
pkgs.mkShell {
  name = "dev-shell-for-type-that-tune";
  packages = [
    pkgs.git
    pkgs.nodePackages_latest.livedown
    perSystem.nixpkgsOldStable.godot_4
    pkgs.ffmpeg
    pkgs.uv

    # Dependencies for ttt-build-tool
    pkgs.pkg-config

    pkgs.pre-commit
    # Dependencies for pre-commit hooks:
    pkgs.go
    perSystem.nixpkgsUnstable.rustc
    pkgs.cabal-install
    pkgs.ghc
  ];
}
