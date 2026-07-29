import aiohttp
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
BASE_URL = os.getenv("URL")
USERNAME = os.getenv("XUI_USERNAME")
PASSWORD = os.getenv("XUI_PASSWORD")

async def login():
    jar = aiohttp.CookieJar(unsafe=True)
    session = aiohttp.ClientSession(cookie_jar=jar)

    resp = await session.get(f"{BASE_URL}/panel/")
    html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")
    csrf = soup.find("meta", {"name": "csrf-token"})["content"]

    headers = {
        "X-CSRF-Token": csrf,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Origin": BASE_URL,
        "Referer": f"{BASE_URL}/panel/"
    }

    await session.post(
        f"{BASE_URL}/login",
        data={
            "username": USERNAME,
            "password": PASSWORD
        },
        headers={
            "X-CSRF-Token": csrf,
            "X-Requested-With": "XMLHttpRequest",
            "Origin": BASE_URL,
            "Referer": f"{BASE_URL}/login"
        }
    )

    return session, headers