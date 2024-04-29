deps:
	docker compose run --rm web bash -c "pip-compile -q && pip-compile -q dev-requirements.in"
