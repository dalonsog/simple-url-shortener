include .env

local:
	flask --app urlshortener/api run --debug

test-local:
	pytest test -v --disable-warnings
