# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
{
  flake,
  perSystem,
  pkgs,
  pname,
}:
pkgs.python3Packages.buildPythonApplication {
  inherit pname;
  version =
    let
      pyprojectContents = builtins.readFile "${flake}/pyproject.toml";
      parsedPyprojectContents = builtins.fromTOML pyprojectContents;
    in
    parsedPyprojectContents.project.version;
  src = "${flake}/python_distribution_packages/ttt-build-tool";
  pyproject = true;

  build-system = [ pkgs.python3Packages.setuptools ];
  dependencies = with pkgs.python3Packages; [
    appdirs
    pyyaml
    requests-cache
    reuse
    yt-dlp
    zstandard
  ];
}
