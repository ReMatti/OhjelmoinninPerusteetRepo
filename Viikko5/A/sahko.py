# Copyright (c) 2025 Matti Remes
# License: MIT

import csv
from datetime import datetime, date
from collections import defaultdict
from typing import Dict


def muotoile_luku(arvo: float) -> str:
    """
    Muotoilee luvun kahden desimaalin tarkkuudella ja pilkulla.
    """
    return f"{arvo:.2f}".replace(".", ",")


def viikonpaiva_suomeksi(paiva: date) -> str:
    """
    Palauttaa viikonpäivän nimen suomeksi.
    """
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
    """
    Lukee CSV-tiedoston ja laskee päiväkohtaiset kulutus- ja tuotantosummat kWh-yksikössä.
    """
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


def tulosta_taulukko(data: Dict[date, Dict[str, float]]) -> None:
    """
    Tulostaa viikon sähkönkulutus- ja tuotantotaulukon.
    """
    paivat = sorted(data.keys())

    if paivat:
        viikon_numero = paivat[0].isocalendar().week
    else:
        viikon_numero = "?"

    print(f"\nViikon {viikon_numero} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")

    print(
        f"{'Päivä':<12}{'Pvm':<14}"
        f"{'Kulutus [kWh]':<22}{'Tuotanto [kWh]':<22}"
    )
    print(
        f"{'':<12}{'(pv.kk.vvvv)':<14}"
        f"{'v1':>6}{'v2':>6}{'v3':>6}   "
        f"{'v1':>6}{'v2':>6}{'v3':>6}"
    )
    print("-" * 78)

    for paiva in paivat:
        pvm_str = f"{paiva.day}.{paiva.month}.{paiva.year}"
        vp = viikonpaiva_suomeksi(paiva)

        d = data[paiva]

        print(
            f"{vp:<12}{pvm_str:<14}"
            f"{muotoile_luku(d['cons1']):>6}"
            f"{muotoile_luku(d['cons2']):>6}"
            f"{muotoile_luku(d['cons3']):>6}   "
            f"{muotoile_luku(d['prod1']):>6}"
            f"{muotoile_luku(d['prod2']):>6}"
            f"{muotoile_luku(d['prod3']):>6}"
        )


def main() -> None:
    """
    Ohjelman pääfunktio: lukee datan, laskee päiväkohtaiset summat ja tulostaa raportin.
    """
    data = lue_ja_laske_data("viikko42.csv")
    tulosta_taulukko(data)


if __name__ == "__main__":
    main()
