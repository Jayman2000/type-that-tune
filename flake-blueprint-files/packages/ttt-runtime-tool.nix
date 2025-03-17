# SPDX-License-Identifier: CC0-1.0
# SPDX-FileCopyrightText: 2025 Jason Yundt <jason@jasonyundt.email>
{
  flake,
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
  src = "${flake}/python_distribution_packages/ttt-runtime-tool";
  pyproject = true;

  build-system = [ pkgs.python3Packages.setuptools ];

  meta.mainProgram = "ttt-runtime-tool";
}
