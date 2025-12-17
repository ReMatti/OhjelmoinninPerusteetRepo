# Copyright (c) 2025 Matti Remes
# License: MIT

import csv
from datetime import datetime, date, timedelta
from collections import defaultdict
from typing import Dict


def muotoile_luku(arvo: float) -> str:

    return f"{arvo:.2f}".replace(".", ",")


def viikonpaiva_suomeksi(paiva: date) -> str:
# Viikonpäivät suomeksi
    paivat = [
        "maanantai",
        "tiistai",
        "keskiviikko",
        "torstai",
        "perjantai",
        "lauantai",
        "sunnuntai",
    ]
    return paivat[paiva.weekday()]


def lue_ja_laske_data(tiedoston_nimi: str) -> Dict[date, Dict[str, float]]:
    
# Lukee CSV-tiedoston ja tekee laskennat
    
    daily_data: Dict[date, Dict[str, float]] = defaultdict(
        lambda: {
            "cons1": 0.0, "cons2": 0.0, "cons3": 0.0,
            "prod1": 0.0, "prod2": 0.0, "prod3": 0.0,
        }
    )

    with open(tiedoston_nimi, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")

        for row in reader:
            aika = datetime.fromisoformat(row["Aika"])
            paiva = aika.date()

            # Kulutus Wh → kWh
            daily_data[paiva]["cons1"] += float(row["Kulutus vaihe 1 Wh"]) / 1000
            daily_data[paiva]["cons2"] += float(row["Kulutus vaihe 2 Wh"]) / 1000
            daily_data[paiva]["cons3"] += float(row["Kulutus vaihe 3 Wh"]) / 1000

            # Tuotanto Wh → kWh
            daily_data[paiva]["prod1"] += float(row["Tuotanto vaihe 1 Wh"]) / 1000
            daily_data[paiva]["prod2"] += float(row["Tuotanto vaihe 2 Wh"]) / 1000
            daily_data[paiva]["prod3"] += float(row["Tuotanto vaihe 3 Wh"]) / 1000

    return daily_data


def muodosta_raportti(data: Dict[date, Dict[str, float]]) -> str:
    if not data:
        return "Ei dataa\n"

    # Selvitetään viikon maanantai
    eka_paiva = min(data.keys())
    viikon_alku = eka_paiva - timedelta(days=eka_paiva.weekday())

    viikon_numero = viikon_alku.isocalendar().week

    rivit = []
    rivit.append(f"Viikon {viikon_numero} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n\n")

    rivit.append(
        f"{'Päivä':<12}{'Pvm':<14}"
        f"{'Kulutus [kWh]':<22}{'Tuotanto [kWh]':<22}\n"
    )
    rivit.append(
        f"{'':<12}{'(pv.kk.vvvv)':<14}"
        f"{'v1':>6}{'v2':>6}{'v3':>6}   "
        f"{'v1':>6}{'v2':>6}{'v3':>6}\n"
    )
    rivit.append("-" * 78 + "\n")

    # Käydään aina 7 päivää (ma–su)
    for i in range(7):
        paiva = viikon_alku + timedelta(days=i)
        vp = viikonpaiva_suomeksi(paiva)
        pvm_str = f"{paiva.day}.{paiva.month}.{paiva.year}"

        # Jos päivä puuttuu → nollat
        d = data.get(paiva, {
            "cons1": 0.0, "cons2": 0.0, "cons3": 0.0,
            "prod1": 0.0, "prod2": 0.0, "prod3": 0.0,
        })

        rivit.append(
            f"{vp:<12}{pvm_str:<14}"
            f"{muotoile_luku(d['cons1']):>6}"
            f"{muotoile_luku(d['cons2']):>6}"
            f"{muotoile_luku(d['cons3']):>6}   "
            f"{muotoile_luku(d['prod1']):>6}"
            f"{muotoile_luku(d['prod2']):>6}"
            f"{muotoile_luku(d['prod3']):>6}\n"
        )

    return "".join(rivit)
            

def main() -> None:
    
#Lukee CVS-tiedostot ja tulostaa raportin sekä yhteenvedon.
    
    tiedostot = [
        "viikko41.csv",
        "viikko42.csv",
        "viikko43.csv",
    ]

    kaikki_raportit = []

    for tiedosto in tiedostot:
        data = lue_ja_laske_data(tiedosto)
        raportti = muodosta_raportti(data)

        print(raportti)             
        kaikki_raportit.append(raportti)

# Tehdään yhteenveto

    with open("yhteenveto.txt", "w", encoding="utf-8") as f:
        for raportti in kaikki_raportit:
            f.write(raportti)
            f.write("\n\n")

    print("Raportti luotu")




if __name__ == "__main__":
    main()
