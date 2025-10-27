include .env

local:
	flask --app urlshortener/api run --debug
