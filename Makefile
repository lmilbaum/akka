.PHONY: up down

up:
	docker build -t ghcr.io/platform-engineering-org/akka-manager:latest -f manager/Dockerfile .
	kind create cluster
	kind load docker-image ghcr.io/platform-engineering-org/akka-manager:latest
	kubectl apply -f manager/deploy/manager.yaml
	sleep 20
	kubectl port-forward service/manager 5000:5000 &

down:
	kind delete cluster
