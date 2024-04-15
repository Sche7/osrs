zip-file:
	mkdir -p python
	pip install . -t python
	zip -r osrs.zip python
	rm -rf python

test-unit:
	poetry run pytest tests/

test-aws:
	poetry run pytest tests/ -m aws

apply-discord-webhook-infra:
	terraform -chdir="terraform/" apply -var-file="setup.tfvars"

apply-discord-webhook-infra-replace-zip-file:
	$(MAKE) zip-file
	terraform -chdir="terraform/" apply -var-file="setup.tfvars" -replace="module.discord_webhook.aws_lambda_layer_version.osrs_layer"

destroy-discord-webhook-infra:
	terraform -chdir="terraform/" destroy -var-file="setup.tfvars"

init-terraform:
	terraform -chdir="terraform/" init

setup-discord-webhook-infra:
	$(MAKE) zip-file
	$(MAKE) init-terraform
	terraform -chdir="terraform/" apply -var-file="setup.tfvars"
