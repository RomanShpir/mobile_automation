# Mobile Automation Makefile
.PHONY: help setup build start stop test test-smoke test-calculator clean logs

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Install Python dependencies
	pip install -r requirements.txt

build: ## Build Docker images
	docker-compose build --no-cache

start: ## Start Appium server and Android emulator
	docker-compose up -d
	@echo "Waiting for services to start..."
	@sleep 10
	@echo "Services should be running. Check with 'make logs'"

stop: ## Stop all services
	docker-compose down

restart: stop start ## Restart all services

test: ## Run all tests
	pytest tests/ -v --html=reports/report.html --self-contained-html

test-smoke: ## Run smoke tests only  
	pytest tests/test_smoke.py -v -m smoke --html=reports/smoke_report.html --self-contained-html

test-calculator: ## Run calculator tests only
	pytest tests/test_calculator.py -v --html=reports/calculator_report.html --self-contained-html

test-parallel: ## Run tests in parallel
	pytest tests/ -v -n auto --html=reports/parallel_report.html --self-contained-html

logs: ## Show Docker logs
	docker-compose logs -f

status: ## Show service status
	docker-compose ps

health-check: ## Run health check to verify setup
	python health_check.py

shell: ## Access Appium container shell
	docker-compose exec appium-server /bin/bash

clean: ## Clean up containers, images and reports
	docker-compose down -v --rmi all || true
	rm -rf reports/*.html reports/*.png reports/allure-results || true

vnc: ## Instructions for VNC connection
	@echo "Connect to VNC viewer at localhost:5900 to see the Android emulator"
	@echo "Default VNC password: secret"

dev-setup: setup build start ## Complete development setup
	@echo "Development environment setup complete!"
	@echo "Run 'make test-smoke' to verify everything works"
	@echo "Use 'make vnc' to connect to the emulator display"