deps:
	docker compose run --rm web bash -c "pip-compile --strip-extras -q && pip-compile -q dev-requirements.in --strip-extras"
