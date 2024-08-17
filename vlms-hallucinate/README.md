# VLMs hallucinate

The project contains the code for [this blog post](https://github.com/danielcorin/blog/blob/main/content/posts/2024/vlms-hallucinate.md)

[Live article](https://www.danielcorin.com/posts/2024/vlms-hallucinate/)

## Setup

```sh
make install
```

This project used `typst` to generate the PDFs in the `docs` folder.
If you're using `nix` and `direnv`, it should automatically be installed for you from `flake.nix` as specificed in `.envrc`.
You don't need it to run the tests but you do if you want to change and regenerate the PDFs.
For example:

```sh
typst compile docs/receipt.typ docs/receipt.pdf
```

## Run

```sh
python main.py --proto protos/receipt.proto:Receipt --file_path docs/receipt-original.pdf --log_level INFO
```

## Add a new dependency

Add dependency to `requirements.in`.

Re-compile `requirements*.txt` files:

```sh
make compile
```

Reinstall dependencies

```sh
make install
```
