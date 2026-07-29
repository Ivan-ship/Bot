import os
from dotenv import load_dotenv

load_dotenv()

XUI_HOST = os.getenv("XUI_HOST")
XUI_PORT = os.getenv("XUI_PORT")

async def generate_vless_url(profile_data, inbound):
    reality = inbound["streamSettings"]["realitySettings"]

    host = XUI_HOST
    port = inbound["port"]

    pbk = reality["settings"]["publicKey"]
    sid = reality["shortIds"][0]
    sni = reality["serverNames"][0]
    fp = reality["settings"]["fingerprint"]
    spx = reality["settings"]["spiderX"]

    return (
        f"vless://{profile_data['client_id']}@{host}:{port}"
        f"?type=tcp"
        f"&security=reality"
        f"&encryption=none"
        f"&pbk={pbk}"
        f"&fp={fp}"
        f"&sni={sni}"
        f"&sid={sid}"
        f"&spx={spx}"
        f"#{profile_data['remark']}"
    )