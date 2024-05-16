.PHONY: venv
venv:
	python -m venv .venv
	. .venv/bin/activate
	direnv allow

.PHONY: install
install: venv
	pip install uv
	pip install -r requirements.txt
