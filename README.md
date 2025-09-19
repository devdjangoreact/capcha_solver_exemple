# Captcha Automation with Playwright

Automation system for solving Incapsula/hCaptcha using various captcha solving services with anti-detection features.

---

## Supported Captcha Solving Services

- ✅ CapMonster
- ✅ SolveCaptcha
- ✅ Capsolver

---

## Prerequisites

- Windows OS
- Python 3.8+
- Git (optional)

---

## Installation

1. **Clone or download the project:**

   ```bash
   git clone <your-repo-url>
   cd capcha_solver_exemple
   ```

2. **Configure environment variables:**

   - Copy `.env.example` to `.env`
   - Edit `.env` with your configuration:
     ```
     SOLVER_TYPE=capmonster
     API_KEY=your_actual_api_key
     TARGET_URL=https://site-with-captcha.com
     PROXY=http://user:pass@proxy.com:8080
     HEADLESS=False
     ```

3. **Install dependencies and set up environment:**
   - Double-click `Makefile.win` (if associated with `make`)
   - Or use command line:
     ```bash
     make -f Makefile.win install
     ```

---

## Usage

1. **Edit the `.env` file** with your settings.

2. **Run automation:**
   - Double-click `Makefile.win`
   - Or use command line:
     ```bash
     make -f Makefile.win run
     ```

### Manual Commands

```bash
# Install dependencies
make -f Makefile.win install

# Run automation
make -f Makefile.win run

# Clean project
make -f Makefile.win clean
```

### If you prefer Python commands:

```bash
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python -m playwright install chromium
.\.venv\Scripts\python main.py
```

---

## Troubleshooting

- **Proxy issues:** Check your proxy format in `.env`
- **API key errors:** Verify your API key with the captcha service
- **Browser issues:** Try setting `HEADLESS=False` to see browser window

---

## Features

- ✅ Multiple captcha solving services
- ✅ Anti-detection browser automation
- ✅ Proxy support with authentication
- ✅ Configurable via environment variables
- ✅ Automatic retries on failure
- ✅ Comprehensive logging

---

## License

MIT License - feel free to use for your projects!

---

## Як запустити на Windows (Ukrainian):

1. **Збережіть всі файли** в одну папку
2. **Перейменуйте Makefile.win** просто в `Makefile` (якщо використовуєте Git Bash)
3. **Налаштуйте `.env` файл** з вашими даними:
   - API ключ від обраного сервісу капчі
   - URL сайту з капчею
   - Проксі (якщо потрібно)
4. **Запуск:**
   - **Подвійний клік на Makefile** (якщо асоційовано з make)
   - **Або в командному рядку:**
     ```cmd
     make install
     make run
     ```

Система автоматично створить віртуальне середовище, встановить залежності, налаштує браузер і запустить автоматизацію!
