.PHONY: venv
venv:
	python -m venv .venv
	. .venv/bin/activate && pip install --upgrade pip

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
	mkdir -p gen/protos
	find protos -name "*.proto" -type f -exec python -m grpc_tools.protoc -I./protos --python_out=./gen/protos {} +

.PHONY: run
run:
	@echo "Add run command here"
