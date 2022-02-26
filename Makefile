.PHONY: notebook
.EXPORT_ALL_VARIABLES:

PREFECT__FLOWS__CHECKPOINTING = true

install: 
	@echo "Installing..."
	poetry install

activate:
	@echo "Activating virtual environment"
	poetry shell


pull_data:
	@echo "Pulling data..."
	poetry run dvc pull -r origin

setup: activate 
install_all: install pull_data

test:
	pytest

clean: 
	@echo "Deleting log files..."
	find . -name "*.log" -type f -not -path "./wandb/*" -delete

dvc_add:
	dvc add data 
	dvc add model
	dvc add image 
	dvc add metrics.csv

dvc_push:
	dvc push -r origin

git_add:
	git add .
	git status

add: dvc_add dvc_push git_add