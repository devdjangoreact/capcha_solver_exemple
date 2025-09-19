markdown

# Captcha Automation with Playwright

Automation system for solving Incapsula/hCaptcha using various captcha solving services with anti-detection features.

## Supported Captcha Solving Services

- ✅ CapMonster
- ✅ SolveCaptcha
- ✅ Capsolver

## Prerequisites

- Windows OS
- Python 3.8+
- Git (optional)

## Installation

1. **Clone or download the project**
   ```bash
   git clone <your-repo-url>
   cd captcha-automation
   Configure environment variables
   ```

Copy .env.example to .env

Edit .env with your configuration:

env
SOLVER_TYPE=capmonster
API_KEY=your_actual_api_key
TARGET_URL=https://site-with-captcha.com
PROXY=http://user:pass@proxy.com:8080
HEADLESS=False
Run installation (double-click on Makefile.win or use command line)

bash
make -f Makefile.win install
Usage
Quick Start
Edit the .env file with your settings

Double-click on Makefile.win - it will automatically install and run

Or use command line:

bash
make -f Makefile.win run
Manual Commands
bash

# Install dependencies

make -f Makefile.win install

# Run automation

make -f Makefile.win run

# Clean project

make -f Makefile.win clean

# Show help

make -f Makefile.win help
Configuration (.env file)
Variable Description Example
SOLVER_TYPE Captcha solving service capmonster
API_KEY Your API key for the service abc123...
TARGET_URL URL of the protected page https://example.com
PROXY Optional proxy (HTTP/HTTPS) http://user:pass@host:port
HEADLESS Run browser in background True/False
LOG_LEVEL Logging level INFO/DEBUG
Project Structure
text
captcha-automation/
├── Makefile.win # Windows automation script
├── .env # Configuration file
├── requirements.txt # Python dependencies
├── main.py # Main automation script
├── browser_manager.py # Browser management with anti-detection
├── base_solver.py # Base captcha solver class
├── capmonster_solver.py # CapMonster implementation
├── solvecaptcha_solver.py # SolveCaptcha implementation
└── capsolver_solver.py # Capsolver implementation
Troubleshooting
If Make doesn't work: Run commands manually:

bash
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m playwright install chromium
.\.venv\Scripts\python main.py
Proxy issues: Check your proxy format in .env

API key errors: Verify your API key with the captcha service

Browser issues: Try setting HEADLESS=False to see what happens

Features
✅ Multiple captcha solving services

✅ Anti-detection browser automation

✅ Proxy support with authentication

✅ Configurable via environment variables

✅ Automatic retries on failure

✅ Comprehensive logging

License
MIT License - feel free to use for your projects!

text

## Як запустити на Windows:

1. **Збережіть всі файли** в одну папку
2. **Перейменуйте Makefile.win** просто в `Makefile` (якщо використовуєте Git Bash)
3. **Налаштуйте `.env` файл** з вашими даними:

   - API ключ від обраного сервісу капчі
   - URL сайту з капчею
   - Проксі (якщо потрібно)

4. **Запуск**:
   - **Подвійний клік на Makefile** (якщо асоційовано з make)
   - **Або в командному рядку**:
     ```cmd
     make install
     make run
     ```

Система автоматично створить віртуальне середовище, встановить залежності, налаштує браузер і запустить автоматизацію!
