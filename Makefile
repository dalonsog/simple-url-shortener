include .env

local:
	flask --app urlshortener/api run --debug

docker-build:
	docker image build . -t simple-url-shortener-app:latest

docker-run:
	docker compose up -d

docker-logs:
	docker compose logs app -f

kubernetes-deploy:
	kubectl apply -f ./k8s

kubernetes-delete:
	kubectl delete -f ./k8s

kubernetes-pods-app:
	kubectl get pods -l app=url-shortener-app

kubernetes-pods-mongo:
	kubectl get pods -l app=url-shortener-mongo

kubernetes-logs-app:
	kubectl logs deployment/url-shortener -f

kubernetes-logs-mongo:
	kubectl logs deployment/mongo -f

test-unit:
	pytest test -v --disable-warnings -m unit

test-integration:
	pytest test -v --disable-warnings -m integration

test-all:
	pytest test -v --disable-warnings -m unit
	pytest test -v --disable-warnings -m integration