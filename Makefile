# If there is a file/folder with the same name as a make command,
# add the command name to .PHONY (separated by spaces)
# so make will ignore the file/folder and always run the command
.PHONY: tests

# In alphabetical order, with help at the bottom
db-downgrade:
	pipenv run flask db downgrade

db-history:
	pipenv run flask db history

db-migrate:
	pipenv run flask db migrate

db-upgrade:
	pipenv run flask db upgrade

fix-subdependencies:
	pipenv lock --pre --clear

lint:
	pipenv run black ./ibackend ./tests

local-server:
	pipenv run uvicorn ibackend:app --reload

tests:
	pipenv run black --check ./ibackend ./tests
	TESTING=1 pipenv run pytest -s --disable-warnings tests/unit_test.py
	TESTING=1 pipenv run pytest -s --disable-warnings tests/integration_test.py
	#TESTING=1 pipenv run pytest --disable-warnings tests/test.py

