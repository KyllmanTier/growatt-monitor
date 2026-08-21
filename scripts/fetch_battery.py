"""
Récupère le statut batterie du WIT depuis Growatt et écrit
docs/battery.json pour la page web (GitHub Pages).

Variables d'environnement attendues :
    GROWATT_COOKIE  -> le cookie de session complet (copié du navigateur)
    PLANT_ID        -> identifiant de l'installation (ex: 10229210)
    WIT_SN          -> numéro de série de l'onduleur WIT
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests

PLANT_ID = os.environ["PLANT_ID"]
WIT_SN = os.environ["WIT_SN"]
COOKIE = os.environ["GROWATT_COOKIE"]

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "battery.json")


def fetch_battery_status():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": COOKIE,
        "Referer": "https://server.growatt.com/index",
        "Origin": "https://server.growatt.com",
    })

    url = "https://server.growatt.com/panel/wit/getWITStatusData"
    data = {"plantId": PLANT_ID, "witSn": WIT_SN}

    response = session.post(url, data=data, timeout=15)
    response.raise_for_status()
    result = response.json()

    if result.get("result") != 1:
        raise RuntimeError(f"Réponse inattendue de Growatt (session probablement expirée) : {result}")

    return result.get("obj", {})


def main():
    now = datetime.now(timezone.utc).isoformat()

    try:
        obj = fetch_battery_status()

        bat_power = float(obj.get("batPower", 0))       # négatif = charge, positif = décharge
        power_to_grid = float(obj.get("pactogrid", 0))  # injecté sur le réseau
        power_to_user = float(obj.get("pactouser", 0))  # soutiré du réseau
        e_today = float(obj.get("eToday", 0))           # production du jour en kWh

        output = {
            "success": True,
            "updated_at": now,
            "soc": int(obj.get("SOC", 0)),
            "pv_power_kw": float(obj.get("ppv", 0)),
            "energy_today_kwh": e_today,
            "power_to_grid_kw": power_to_grid,
            "power_to_user_kw": power_to_user,
            "bat_power_kw": bat_power,
            "bat_voltage": float(obj.get("vBat", 0)),
            "load_power_kw": float(obj.get("pLocalLoad", 0)),
        }

    except Exception as e:
        output = {
            "success": False,
            "updated_at": now,
            "error": str(e),
        }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    if not output["success"]:
        print(f"Erreur : {output['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
