import os
from dotenv import load_dotenv

load_dotenv()

XUI_HOST = os.getenv("XUI_HOST")
XUI_PORT = os.getenv("XUI_PORT")
LISTEN_PORT = os.getenv("LISTEN_PORT")
URI_APTH = os.getenv("URI_APTH")

async def generate_vless_url(profile_data):
    sub_id = profile_data["sub_id"]
    
    host = XUI_HOST
    listen_port = LISTEN_PORT
    uri = URI_APTH

    return (
        f"https://{host}:{listen_port}/{uri}/{sub_id}"
    )