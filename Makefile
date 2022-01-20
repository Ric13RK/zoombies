# Project
NAME = zoombies-p2
PACKAGE = src/pkg

# Docker
IMAGE_NAME = qna-ml-algo-x
LATEST_TAG = latest
DEPLOY_TAG := $(shell git rev-parse HEAD)
TAG = $(DEPLOY_TAG)
HOME_DIR = $(shell echo $$HOME)
PWD = $(shell pwd)

# AWS
AWS_PROFILE = AWS-Hackathon-2021
ACCOUNT_NO = 571747411449
REGION = ap-southeast-2
ECR_URL = $(ACCOUNT_NO).dkr.ecr.$(REGION).amazonaws.com
ECR_IMAGE = $(ECR_URL)/$(IMAGE_NAME)

# Doc
.PHONY: docs
.DEFAULT_GOAL := help


help:				## Show the help.
	@echo "Usage: make <target>"
	@echo "********************"
	@echo "***** Targets: *****"
	@echo "********************"
	@fgrep "##" Makefile | fgrep -v fgrep


## DOCKER COMMAND
build:				## Build the Docker image
	docker build \
	-t $(IMAGE_NAME):$(LATEST_TAG) \
	-t $(IMAGE_NAME):$(DEPLOY_TAG) \
	-f Dockerfile \
	.

# TODO: add volume to test python script without building new docker image
run:				## Run the Docker image
	docker run $(IMAGE_NAME):$(LATEST_TAG)
	docker run \
	-v ~/.aws:/root/.aws:ro \
	-v "$(PWD)/$(PACKAGE):/$(NAME)/$(PACKAGE)/" \
	$(IMAGE_NAME):$(LATEST_TAG)

bash:				## Run the Docker image
	docker run \
	-it \
	--rm \
	-v "$(HOME_DIR)/.aws:/root/.aws:ro" \
	-v "$(PWD)/$(PACKAGE):/$(NAME)/$(PACKAGE)/" \
	$(IMAGE_NAME):$(LATEST_TAG) \
	bash

prune:				## Prune docker container, volumes, networks, and images
	docker container prune -f && \
	docker volume prune -f && \
	docker network prune -f && \
	docker image prune -f


## ECR COMMAND
ecr-login:			## Login to AWS ECR repo
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(ECR_URL)

push: 				## Push build docker image to AWS ECR repo
	docker tag $(IMAGE_NAME):$(Lmake buildATEST_TAG) $(ECR_IMAGE):$(LATEST_TAG) && \
	docker tag $(IMAGE_NAME):$(DEPLOY_TAG) $(ECR_IMAGE):$(DEPLOY_TAG) && \
	docker push $(ECR_IMAGE):$(LATEST_TAG) && \
	docker push $(ECR_IMAGE):$(DEPLOY_TAG)

## TERRAFORM COMMANDS
tf_plan: 			## Create terraform infrastructure plan
	cd tf_resource && \
	tf init -upgrade && \
	tf plan -out=tfplan -no-color > plan.txt && \
	cat plan.txt

tf_apply: 			## Create infrastructure resources using terraform script
	cd tf_resource && \
	tf init -upgrade && \
	tf apply --auto-approve tfplan

tf_state: 			## List out terraform created infrastructure state
	cd tf_resource && \
	tf init -upgrade && \
	tf state list

tf_destroy:			## delete terraform created infrastructure
	cd tf_resource && \
	tf init -upgrade && \
	tf destroy --auto-approve

## CLOUDFORMATION COMMANDS
create-stake:			## Crete cloudformation stack
	aws cloudformation create-stack --stack-name  zoombies-p2-stack --template-body templates/aws_cf.yaml

create-change-set:		## Crete cloudformation create change-set
	aws cloudformation create-change-set --stack-name zoombies-p2-stack --change-set-name zoombies-p2-changeSet --template-body templates/aws_cf.yaml

execute-change-set:		## Crete cloudformation execute change-set
	aws cloudformation execute-change-set --stack-name zoombies-p2-stack --change-set-name zoombies-p2-changeSet

delete-stack:			## delete cloudformation stack
	aws cloudformation delete-stack --stack-name zoombies-p2-stack