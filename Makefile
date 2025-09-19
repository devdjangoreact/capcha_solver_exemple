# Makefile for Windows Captcha Automation Project
SHELL = cmd

# Python executable in virtual environment
PYTHON = .\.venv\Scripts\python.exe
PIP = .\.venv\Scripts\pip.exe

# Default target
all: install run

# Create virtual environment
venv:
	@echo Creating virtual environment...
	python -m venv .venv
	@echo Virtual environment created.

# Install dependencies
install: venv
	@echo Installing dependencies...
	$(PIP) install -r requirements.txt
	$(PYTHON) -m playwright install chromium
	@echo Dependencies installed.

# Run the automation
run:
	@echo Running captcha automation...
	$(PYTHON) main.py
	@echo Automation completed.

# Clean the project
clean:
	@echo Cleaning up...
	rmdir /s /q .venv 2>nul || echo No virtual environment to remove
	rmdir /s /q __pycache__ 2>nul || echo No cache to remove
	del /q *.log 2>nul || echo No logs to remove
	@echo Cleanup completed.

# Show help
help:
	@echo Available commands:
	@echo   make install    - Create venv and install dependencies
	@echo   make run        - Run the automation
	@echo   make venv       - Create virtual environment only
	@echo   make clean      - Clean project files
	@echo   make help       - Show this help

.PHONY: all venv install run clean help