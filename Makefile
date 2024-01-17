zip-file:
	mkdir -p python
	pip install . -t python
	zip -r osrs.zip python
	rm -rf python

test-unit:
	poetry run pytest tests/

test-aws:
	poetry run pytest tests/ -m aws

discord-webhook-infra:
	terraform -chdir="terraform/" apply -var-file="setup.tfvars"
