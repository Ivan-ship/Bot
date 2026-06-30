import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from dotenv import load_dotenv
import os
import uuid
import secrets

load_dotenv()

BASE_URL = os.getenv("URL")
USERNAME = os.getenv("XUI_USERNAME")
PASSWORD = os.getenv("XUI_PASSWORD")
XUI_HOST = os.getenv("XUI_HOST")
XUI_PORT = os.getenv("XUI_PORT")

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
        
        #Create test user
        async with session.get(
            f"{BASE_URL}/panel/api/inbounds/list"
            ) as response:
            data = await response.json()

            headers = {
                "X-CSRF-Token": csrf,
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json",
                "Origin": BASE_URL,
                "Referer": f"{BASE_URL}/panel/"
            }
            inbound = data["obj"][0]
            inbound_id = inbound["id"]
            print("Создание пользователя")
            client_id = await create_clients(
                session=session, 
                inbound_id=inbound_id, 
                email="email3@gmail.com",
                headers=headers
                )
            print("UUID: ", client_id)

            profile = {
                "client_id": client_id,
                "email": "email@gmail.com",
                "remark": inbound["remark"]
            }


            vless_url = await generate_vless_url(profile)
            print("VLESS URL: ")
            print(vless_url)

        
#Create users in inbounds
async def create_clients(session, inbound_id, email, headers):
    client_id = str(uuid.uuid4())

    try:
        payload = {
                "client": 
                    {
                        "id": client_id,
                        "email": email,
                        "auth": secrets.token_urlsafe(12),
                        "comment": "",
                        "enable": True,
                        "flow": "",
                        "group": "",
                        "password": secrets.token_urlsafe(12),
                        "reset": 0,
                        "security": "auto",
                        "subId": secrets.token_hex(8),
                        "totalGB": 0,
                        "limitIp": 0,
                        "expiryTime": 0,
                        "tgId": 0
                    },
                "inboundIds": [inbound_id]
        }

        async with session.post(
            f"{BASE_URL}/panel/api/clients/add",
            json = payload,
            headers = headers
        ) as response:
            text = await response.text()
            print("CREATE STATUS:", response.status, text)
        return client_id
    except Exception as ex:
        print(f"Произошел сбой! {ex}")
    
#Return vless url
async def generate_vless_url(profile_data: dict) -> str:
    remark = profile_data.get('remark', 'AUS')
    email = profile_data['email']
    pbk = "Yjh-oB876wBg6dQxz51wRCacTz3tCGJBqAadjseypyg"
    fp = "chrome"
    sni = "www.oracle.com"
    sid = "8f93ac5e007a18"

    return(
        f"vless://{profile_data['client_id']}@{XUI_HOST}:{XUI_PORT}"
        f"?encryption=none&fp={fp}&&pbk={pbk}&security=reality&"
        f"sid={sid}&sni={sni}&spx=%2FFrWohfbzLqhPWOS&type=tcp#{remark}-{email}"
    )
    
    
asyncio.run(main())