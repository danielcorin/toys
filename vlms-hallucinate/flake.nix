{
  description = "VLMs are gullible";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages.default = pkgs.typst;

        apps.default = {
          type = "app";
          program = "${pkgs.typst}/bin/typst";
        };

        devShell = pkgs.mkShell {
          buildInputs = [ pkgs.typst ];
        };
      });
}

