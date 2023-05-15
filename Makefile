.DEFAULT_GOAL := build

IMAGE_NAME := prometheus_metrics_exporter
IMAGE_TAG := latest

.PHONY: build push clean

build:
	docker buildx build --load --platform=linux/amd64 -t $(IMAGE_NAME):$(IMAGE_TAG) .


clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG)
