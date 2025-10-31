include .env

local:
	flask --app urlshortener/api run --debug

test-all:
	pytest test -v --disable-warnings

test-unit:
	pytest test -v --disable-warnings -m unit

test-integration:
	pytest test -v --disable-warnings -m integration
