.PHONY: venv
venv:
	python -m venv .venv
	. .venv/bin/activate
	direnv allow

.PHONY: install
install: venv
	pip install -r requirements-dev.txt
	pip install -r requirements.txt

.PHONY: compile
compile: venv
	uv pip compile requirements.in -o requirements.txt
	uv pip compile requirements-dev.in -o requirements-dev.txt

.PHONY: run
run:
	@echo "Add run command here"

.PHONY: temporal-server
temporal-server:
	temporal server start-dev

.PHONY: temporal-worker
temporal-worker:
	python -m worker

.PHONY: run-workflow
run-workflow:
	python -m run_workflow
