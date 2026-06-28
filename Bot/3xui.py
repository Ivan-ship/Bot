import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("URL")
USERNAME = os.getenv("XUI_USERNAME")
PASSWORD = os.getenv("XUI_PASSWORD")

async def main():
    jar = aiohttp.CookieJar(unsafe=True)
    async with aiohttp.ClientSession(cookie_jar=jar) as session:
        async with session.get(f"{BASE_URL}/panel/") as response:
            html = await response.text()
            print(response.status)

            soup = BeautifulSoup(html, "html.parser")
            csrf = soup.find("meta", {"name": "csrf-token"})["content"]
            print("CSRF: ", csrf)

            # login
            headres = {
                "X-CSRF-Token": csrf,
                "X-Requested-With": "XMLHttpRequest",
                "Origin": BASE_URL,
                "Referer": f"{BASE_URL}/login", 
            }

        async with session.post(

            f"{BASE_URL}/login",
            data ={
                "username": USERNAME,
                "password": PASSWORD
            },
            headers=headres
        ) as response:
            print("LOGIN STATUS: ", response.status)
        
        async with session.get(f"{BASE_URL}/panel/api/inbounds/list") as response:
            print("API STATUS: ", response.status)
            data = await response.json()

            for inbound in data["obj"]:
                print("Inbound: ", inbound["remark"])
                settings = inbound["settings"]

                for client in settings["clients"]:
                    print(client["email"], client["id"])



asyncio.run(main())