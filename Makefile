VENV=.venv
PY=python

.PHONY: venv install test lint validate infra-deploy infra-teardown

venv:
	$(PY) -m venv $(VENV)

install: venv
	$(VENV)/Scripts/activate && $(PY) -m pip install --upgrade pip
	$(VENV)/Scripts/activate && $(PY) -m pip install -r requirements-dev.txt

test:
	$(VENV)/Scripts/activate && $(PY) -m pytest src/shared/tests -q

lint:
	$(VENV)/Scripts/activate && echo "Run ruff/black/yamllint here"

validate:
	$(VENV)/Scripts/activate && $(PY) -m src.shared.scripts.validate_gate2_artifacts .

infra-deploy:
	@echo "Deploy infra via Azure CLI (bicep). Example: az deployment group create --resource-group <rg> --template-file infra/test-environment.bicep --parameters prefix=dmftest"

infra-teardown:
	@echo "Tear down resources created by infra-deploy"
