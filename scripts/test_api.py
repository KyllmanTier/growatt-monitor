import os
import requests
import json

TOKEN = os.environ["GROWATT_TOKEN"]
WIT_SN = os.environ["WIT_SN"]

url = "https://openapi.growatt.com/v4/new-api/queryLastData"

headers = {
    "token": TOKEN,
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "deviceType": "wit",
    "deviceSn": WIT_SN,
}

try:
    response = requests.post(
        url,
        headers=headers,
        data=data,
        timeout=15
    )

    print("HTTP status:", response.status_code)

    result = response.json()

    # On affiche la réponse pour identifier les champs disponibles.
    # Le token n'est pas dans cette réponse.
    print(json.dumps(result, indent=2, ensure_ascii=False))

except Exception as e:
    print("ERREUR:", str(e))
    raise
