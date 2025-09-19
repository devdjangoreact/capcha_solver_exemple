import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

API_KEY = ""
PAGEURL = "https://accounts.hcaptcha.com/demo"


def solve_hcaptcha(sitekey):

    in_url = "https://api.solvecaptcha.com/in.php"
    payload = {
        "key": API_KEY,
        "method": "hcaptcha",
        "sitekey": sitekey,
        "pageurl": PAGEURL,
        "json": 1,
    }

    response = requests.post(in_url, data=payload)
    result = response.json()

    if result.get("status") != 1:
        print("Ошибка при отправке запроса:", result.get("request"))
        return None

    captcha_id = result.get("request")
    print("Получен captcha_id:", captcha_id)

    res_url = "https://api.solvecaptcha.com/res.php"
    while True:
        params = {"key": API_KEY, "action": "get", "id": captcha_id, "json": 1}
        res = requests.get(res_url, params=params)
        data = res.json()

        if data.get("status") == 1:
            print("solved!")
            return data
        elif data.get("request") == "CAPCHA_NOT_READY":
            print("don't solve, wait 5 secund...")
            time.sleep(5)
        else:
            print("Error:", data.get("request"))
            return None


def set_captcha_token(driver, token):

    try:
        driver.find_element(By.NAME, "h-captcha-response")
    except Exception:
        driver.execute_script(
            """
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'h-captcha-response';
            document.body.appendChild(input);
        """
        )
    try:
        driver.find_element(By.NAME, "g-recaptcha-response")
    except Exception:
        driver.execute_script(
            """
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'g-recaptcha-response';
            document.body.appendChild(input);
        """
        )

    driver.execute_script(
        f"""
        document.getElementsByName('h-captcha-response')[0].value = '{token}';
        document.getElementsByName('g-recaptcha-response')[0].value = '{token}';
    """
    )


def show_visual_feedback(driver):

    driver.execute_script(
        """
        var banner = document.createElement('div');
        banner.innerText = 'Captcha Solved!';
        banner.style.position = 'fixed';
        banner.style.top = '0';
        banner.style.left = '0';
        banner.style.width = '100%';
        banner.style.backgroundColor = 'green';
        banner.style.color = 'white';
        banner.style.fontSize = '24px';
        banner.style.fontWeight = 'bold';
        banner.style.textAlign = 'center';
        banner.style.zIndex = '9999';
        banner.style.padding = '10px';
        document.body.appendChild(banner);
    """
    )


def main():

    driver = webdriver.Chrome()
    driver.get(PAGEURL)

    try:
        sitekey_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-sitekey]"))
        )

        sitekey = sitekey_element.get_attribute("data-sitekey")
        print("sitekey:", sitekey)
    except Exception as e:
        print("Error find data-sitekey:", e)
        driver.quit()
        return

    solution = solve_hcaptcha(sitekey)
    if solution:
        token = solution.get("request")
        user_agent = solution.get("useragent")
        print("токен:", token)
        print("User-Agent:", user_agent)

        set_captcha_token(driver, token)
        print("Added to form.")

        show_visual_feedback(driver)

        driver.find_element(By.ID, "submit-button").click()

        time.sleep(100)
        driver.quit()
    else:
        print("Noo not solved.")
        driver.quit()


if __name__ == "__main__":
    main()
