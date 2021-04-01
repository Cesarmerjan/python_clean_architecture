install-dev:
	pip3 install -e .['dev']

install-prod:
	pip3 install -e .

uninstall:
	pip3 uninstall make_a_comment

utests:
	pytest tests/unit

itests:
	pytest tests/integration

e2etests:
	pytest tests/e2e

alltests:
	pytest