# Protobuf zip imports

Inspired by the [Protobuf docs](https://protobuf.dev/reference/python/python-generated/), we generate Python code from protobufs as a zip file, then import it with `zipimport`.

> ## Tip
> When outputting Python code, the protocol buffer compiler's ability to output directly to ZIP archives is particularly convenient, as the Python interpreter is able to read directly from these archives if placed in the PYTHONPATH. To output to a ZIP file, simply provide an output location ending in .zip.

With the approach in this project, we avoid several annoying parts of how `protoc` generates code.

1. The generated code is in a single zip at the root of the project, easily gitignored.
2. Because the code is at the root of the project, it is simply importable in the server and client code without there being issues with the internal imports of the generated code.
3. The code (zip) does not need to be explicitly added to the `PYTHONPATH` -- we can just reference it from the root of the project with `zipimport`.

An additional learning:

The code

```python
grpc.server(...).start()
```

does not raise an error if the port you've added is already in use.
This script's server, checks for port availability before starting the server and exits if the port is unavailable.
This lack of visibility wasted a bunch of my time.


Code for [this blog post](https://github.com/danielcorin/blog/blob/main/content/til/protobuf/zip-imports.md)

[Live article](https://danielcorin.com/til/protobuf/zip-imports/)

## Setup

```sh
make install
```

## Run

```sh
make serve

# separately
make client
# python -m src.client
# Greeter client received: Hello, World!
```

## Add a new dependency

Add dependency to `requirements.in`.

Re-compile `requirements*.txt` file:

```sh
make compile
```

Reinstall dependencies

```sh
make install
```
