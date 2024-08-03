.PHONY: venv
venv:
	python -m venv .venv
	. .venv/bin/activate
	pip install --upgrade pip
	direnv allow

.PHONY: install
install: venv
	pip install -r requirements-dev.txt
	pip install -r requirements.txt

.PHONY: compile
compile: venv
	pip install uv
	uv pip compile requirements.in -o requirements.txt
	uv pip compile requirements-dev.in -o requirements-dev.txt

.PHONY: protos
protos:
	find protos -name "*.proto" -type f -exec python -m grpc_tools.protoc -I./protos --python_out=./gen.zip --grpc_python_out=./gen.zip {} +

.PHONY: serve
serve:
	python -m src.server

.PHONY: client
client:
	python -m src.client
