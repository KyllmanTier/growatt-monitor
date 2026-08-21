import json
import os
import sys
from datetime import datetime, timezone

import requests

TOKEN = os.environ["GROWATT_TOKEN"]
WIT_SN = os.environ["GROWATT_WIT_SN"]

OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "docs",
    "battery.json"
)


def fetch_wit_status():
    url = "https://openapi.growatt.com/v4/new-api/queryLastData"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
        "token": TOKEN,
    }

    data = {
        "deviceType": "wit",
        "deviceSn": WIT_SN,
    }

    response = requests.post(
        url,
        headers=headers,
        data=data,
        timeout=15
    )

    response.raise_for_status()

    result = response.json()

    if result.get("code") != 0:
        raise RuntimeError(
            f"Growatt API error: {result}"
        )

    wit_list = result.get("data", {}).get("wit", [])

    if not wit_list:
        raise RuntimeError(
            "Aucune donnée WIT retournée par Growatt"
        )

    return wit_list[0]


def main():
    now = datetime.now(timezone.utc).isoformat()

    try:
        obj = fetch_wit_status()

        # -----------------------------
        # Données principales
        # -----------------------------

        pv_power = float(obj.get("ppv", 0))

        load_power = float(
            obj.get("plocalLoadTotal", 0)
        )

        battery_power = float(
            obj.get("batPower", 0)
        )

        battery_voltage = float(
            obj.get("vbat", obj.get("vBatDsp", 0))
        )

        soc = int(
            obj.get("soc", obj.get("bSoc", 0))
        )

        grid_to_user = float(
            obj.get("pacToUserTotal", 0)
        )

        grid_to_grid = float(
            obj.get("pacToGridTotal", 0)
        )

        # -----------------------------
        # Energies
        # -----------------------------

        energy_today = float(
            obj.get("epvToday", 0)
        )

        self_consumption_today = float(
            obj.get("eselftoday", 0)
        )

        grid_import_today = float(
            obj.get("etoUserToday", 0)
        )

        grid_export_today = float(
            obj.get("etoGridToday", 0)
        )

        # -----------------------------
        # JSON destiné à GitHub Pages
        # -----------------------------

        output = {
            "success": True,
            "updated_at": now,

            "soc": soc,

            "pv_power_kw": pv_power / 1000,
            "load_power_kw": load_power / 1000,

            "power_to_grid_kw": grid_to_grid / 1000,
            "power_to_user_kw": grid_to_user / 1000,

            "bat_power_kw": battery_power / 1000,
            "bat_voltage": battery_voltage,

            "energy_today_kwh": energy_today,

            "self_consumption_today_kwh": self_consumption_today,
            "grid_import_today_kwh": grid_import_today,
            "grid_export_today_kwh": grid_export_today,

            "status": obj.get("statusText", ""),
        }

    except Exception as e:

        output = {
            "success": False,
            "updated_at": now,
            "error": str(e),
        }

    os.makedirs(
        os.path.dirname(OUTPUT_PATH),
        exist_ok=True
    )

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False
        )

    if not output["success"]:

        print(
            f"Erreur : {output['error']}",
            file=sys.stderr
        )

        sys.exit(1)


if __name__ == "__main__":
    main()
