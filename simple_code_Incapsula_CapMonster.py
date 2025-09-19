import asyncio
import json
import random
import string

import aiohttp
from camoufox.async_api import AsyncCamoufox


def generate_user_data():
    first_name = random.choice(["John", "Jane", "Michael", "Sarah", "David", "Emily"])
    last_name = random.choice(
        ["Smith", "Johnson", "Williams", "Brown", "Jones", "Davis"]
    )
    email = (
        f"{first_name.lower()}.{last_name.lower()}{random.randint(100,999)}@gmail.com"
    )
    password = (
        f"{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_lowercase)}"
        f"{random.randint(1000,9999)}{random.choice('!@#$%^&*')}fase34"
    )
    return first_name, last_name, email, password


async def responce_text(response):
    response_text = await response.text()
    try:
        result = json.loads(response_text)  # Then parse JSON manually
    except json.JSONDecodeError:
        print(f"Invalid JSON response: {response_text}")
        raise Exception(f"Invalid JSON response from CapMonster: {response_text}")
    return result


async def solve_recaptcha(api_key, site_url, site_key):
    # Create task
    task_data = {
        "clientKey": api_key,
        "task": {
            "type": "RecaptchaV2TaskProxyless",
            "websiteURL": site_url,
            "websiteKey": site_key,
        },
    }

    async with aiohttp.ClientSession() as session:
        # Create task
        async with session.post(
            "https://api.capmonster.cloud/createTask", json=task_data
        ) as response:
            result = await responce_text(response)
            task_id = result["taskId"]

        # Get result
        for _ in range(30):
            await asyncio.sleep(5)
            result_data = {"clientKey": api_key, "taskId": task_id}

            async with session.post(
                "https://api.capmonster.cloud/getTaskResult", json=result_data
            ) as result_response:
                result = await responce_text(result_response)

                if result["status"] == "ready":
                    return result["solution"]["gRecaptchaResponse"]
                else:
                    print("Captcha not ready, waiting 5 second...")
                    asyncio.sleep(5)
    raise Exception("reCAPTCHA solving timeout")


async def main():
    CAPMONSTER_KEY = ""
    user_data_dir = "brouser_dir"

    async with AsyncCamoufox(
        window=(1282, 955),
        persistent_context=True,
        user_data_dir=user_data_dir,
        i_know_what_im_doing=True,
        geoip=True,
        humanize=3.0,
        enable_cache=True,
    ) as browser:

        pages = browser.pages
        if pages:
            page = pages[0]
        else:
            page = await browser.new_page()

        try:
            # Navigate to registration page
            await page.goto(
                "https://www.iaai.com/Registration/Free", wait_until="networkidle"
            )
            await asyncio.sleep(2)

            # Parse reCAPTCHA site key
            site_key = await page.get_attribute(".g-recaptcha", "data-sitekey")
            print(f"Found reCAPTCHA site key: {site_key}")

            # Generate random user data
            first_name, last_name, email, password = generate_user_data()

            # Fill form
            await page.fill("#FirstName", first_name)
            await page.fill("#LastName", last_name)
            await page.fill("#Email", email)
            await page.fill("#Password", password)
            await page.fill("#Confirmpassword", password)

            # Fix for checkbox - use JavaScript click instead
            await page.evaluate(
                """() => {
                const checkbox = document.querySelector("#acceptTerms");
                if (checkbox) {
                    checkbox.checked = true;
                    checkbox.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }"""
            )
            print("Checkbox checked via JavaScript")

            # Solve reCAPTCHA
            token = await solve_recaptcha(CAPMONSTER_KEY, page.url, site_key)
            await page.evaluate(
                "document.getElementById('g-recaptcha-response').innerHTML = "
                + "'"
                + token
                + "'"
            )
            print("reCAPTCHA solved and token set")
            await asyncio.sleep(3)
            await page.evaluate(
                """() => {
                const button = document.querySelector("#btn-create-account");
                if (button) {
                    button.disabled = false;
                }
            }"""
            )
            print("Button enabled manually")
            await asyncio.sleep(1)
            # Click create account
            await page.click("#btn-create-account")
            await asyncio.sleep(100)

            print("Registration completed successfully")

        except Exception as e:
            print(f"Error: {e}")
            # Take screenshot for debugging
            await page.screenshot(path="error.png")
            print("Screenshot saved as error.png")


if __name__ == "__main__":
    asyncio.run(main())
