# Copyright (c) 2025 Matti Remes
# License: MIT
# You are free to use or modify this code



import csv
from datetime import datetime, date
from typing import List, Dict, Tuple, Optional
from collections import defaultdict

# =====================================================
# APUFUNKTIOT
# =====================================================

def muotoile_luku(arvo: float) -> str:
    """Palauttaa luvun kahden desimaalin tarkkuudella pilkkua käyttäen."""
    return f"{arvo:.2f}".replace(".", ",")


def muotoile_pvm(pvm: date) -> str:
    """Palauttaa päivämäärän muodossa pv.kk.vvvv."""
    return f"{pvm.day}.{pvm.month}.{pvm.year}"


def lue_pvm(kehote: str) -> date:
    """Lukee päivämäärän muodossa pv.kk.vvvv ja palauttaa date-olion."""
    while True:
        try:
            return datetime.strptime(input(kehote), "%d.%m.%Y").date()
        except ValueError:
            print("Virheellinen päivämäärä. Käytä muotoa pv.kk.vvvv.")


# =====================================================
# DATAN LUKU
# =====================================================

def lue_data(tiedoston_nimi: str) -> List[Dict]:
    """Lukee CSV-tiedoston ja palauttaa mittausdatan listana sanakirjoja."""
    data: List[Dict] = []

    with open(tiedoston_nimi, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        for rivi in reader:
            data.append({
                "aika": datetime.fromisoformat(rivi["Aika"]),
                "kulutus": float(rivi["Kulutus (netotettu) kWh"].replace(",", ".")),
                "tuotanto": float(rivi["Tuotanto (netotettu) kWh"].replace(",", ".")),
                "lampotila": float(rivi["Vuorokauden keskilämpötila"].replace(",", "."))
            })

    return data


# =====================================================
# LASKENTA-APUFUNKTIOT
# =====================================================

def etsi_suurin_ja_pienin_paiva(
    data: List[Dict],
    ehto
) -> Optional[Tuple[date, float, float, date, float, float]]:
    """
    Etsii suurimman ja pienimmän kulutuspäivän annetulla ehdolla.
    """
    paivat = defaultdict(lambda: {"kulutus": 0.0, "lampotilat": []})

    for rivi in data:
        if ehto(rivi):
            pvm = rivi["aika"].date()
            paivat[pvm]["kulutus"] += rivi["kulutus"]
            paivat[pvm]["lampotilat"].append(rivi["lampotila"])

    if not paivat:
        return None

    suurin = max(paivat, key=lambda p: paivat[p]["kulutus"])
    pienin = min(paivat, key=lambda p: paivat[p]["kulutus"])

    return (
        suurin,
        paivat[suurin]["kulutus"],
        sum(paivat[suurin]["lampotilat"]) / len(paivat[suurin]["lampotilat"]),
        pienin,
        paivat[pienin]["kulutus"],
        sum(paivat[pienin]["lampotilat"]) / len(paivat[pienin]["lampotilat"]),
    )


# =====================================================
# RAPORTIT
# =====================================================

def raportti_aikavali(alku: date, loppu: date, data: List[Dict]) -> str:
    """Luo päiväkohtaisen raportin annetulta aikaväliltä."""
    raportti = "-" * 53 + "\n"
    raportti += f"Raportti väliltä {muotoile_pvm(alku)}-{muotoile_pvm(loppu)}\n\n"

    kulutus = tuotanto = lampotila = 0.0
    tunnit = 0

    for rivi in data:
        pvm = rivi["aika"].date()
        if alku <= pvm <= loppu:
            kulutus += rivi["kulutus"]
            tuotanto += rivi["tuotanto"]
            lampotila += rivi["lampotila"]
            tunnit += 1

    if tunnit == 0:
        raportti += "Ei dataa valitulta aikaväliltä.\n"
        return raportti + "-" * 53 + "\n"

    raportti += f"- Kokonaiskulutus: {muotoile_luku(kulutus)} kWh\n"
    raportti += f"- Kokonaistuotanto: {muotoile_luku(tuotanto)} kWh\n"
    raportti += f"- Nettokuorma: {muotoile_luku(kulutus - tuotanto)} kWh\n"
    raportti += f"- Keskilämpötila: {muotoile_luku(lampotila / tunnit)} °C\n"

    tulos = etsi_suurin_ja_pienin_paiva(
        data,
        lambda r: alku <= r["aika"].date() <= loppu
    )

    if tulos:
        sp, sk, sl, pp, pk, pl = tulos
        raportti += (
            f"\nSuurin kulutuspäivä: {muotoile_pvm(sp)} "
            f"({muotoile_luku(sk)} kWh, {muotoile_luku(sl)} °C)\n"
        )
        raportti += (
            f"Pienin kulutuspäivä: {muotoile_pvm(pp)} "
            f"({muotoile_luku(pk)} kWh, {muotoile_luku(pl)} °C)\n"
        )

    return raportti + "-" * 53 + "\n"


def raportti_kk(kuukausi: int, data: List[Dict]) -> str:
    """Luo kuukausikohtaisen raportin."""
    kuukaudet = [
        "Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu",
        "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"
    ]

    raportti = "-" * 53 + "\n"
    raportti += f"Raportti kuulta: {kuukaudet[kuukausi - 1]} 2025\n\n"

    kulutus = tuotanto = lampotila = 0.0
    tunnit = 0

    for rivi in data:
        if rivi["aika"].month == kuukausi:
            kulutus += rivi["kulutus"]
            tuotanto += rivi["tuotanto"]
            lampotila += rivi["lampotila"]
            tunnit += 1

    if tunnit == 0:
        return raportti + "Ei dataa.\n" + "-" * 53 + "\n"

    raportti += f"- Kokonaiskulutus: {muotoile_luku(kulutus)} kWh\n"
    raportti += f"- Kokonaistuotanto: {muotoile_luku(tuotanto)} kWh\n"
    raportti += f"- Nettokuorma: {muotoile_luku(kulutus - tuotanto)} kWh\n"
    raportti += f"- Keskilämpötila: {muotoile_luku(lampotila / tunnit)} °C\n"

    tulos = etsi_suurin_ja_pienin_paiva(
        data,
        lambda r: r["aika"].month == kuukausi
    )

    if tulos:
        sp, sk, sl, pp, pk, pl = tulos
        raportti += (
            f"\nSuurin kulutuspäivä: {muotoile_pvm(sp)} "
            f"({muotoile_luku(sk)} kWh, {muotoile_luku(sl)} °C)\n"
        )
        raportti += (
            f"Pienin kulutuspäivä: {muotoile_pvm(pp)} "
            f"({muotoile_luku(pk)} kWh, {muotoile_luku(pl)} °C)\n"
        )

    return raportti + "-" * 53 + "\n"


def raportti_vuosi(data: List[Dict]) -> str:
    """Luo vuoden 2025 kokonaisraportin."""
    raportti = "-" * 53 + "\nRaportti vuodelta 2025\n\n"

    kulutus = sum(r["kulutus"] for r in data)
    tuotanto = sum(r["tuotanto"] for r in data)
    lampotila = sum(r["lampotila"] for r in data)

    raportti += f"- Kokonaiskulutus: {muotoile_luku(kulutus)} kWh\n"
    raportti += f"- Kokonaistuotanto: {muotoile_luku(tuotanto)} kWh\n"
    raportti += f"- Nettokuorma: {muotoile_luku(kulutus - tuotanto)} kWh\n"
    raportti += f"- Keskilämpötila: {muotoile_luku(lampotila / len(data))} °C\n"

    tulos = etsi_suurin_ja_pienin_paiva(data, lambda r: True)
    if tulos:
        sp, sk, sl, pp, pk, pl = tulos
        raportti += (
            f"\nSuurin kulutuspäivä: {muotoile_pvm(sp)} "
            f"({muotoile_luku(sk)} kWh, {muotoile_luku(sl)} °C)\n"
        )
        raportti += (
            f"Pienin kulutuspäivä: {muotoile_pvm(pp)} "
            f"({muotoile_luku(pk)} kWh, {muotoile_luku(pl)} °C)\n"
        )

    return raportti + "-" * 53 + "\n"


# =====================================================
# PÄÄOHJELMA
# =====================================================

def main() -> None:
    """Ohjelman pääfunktio."""
    tietokanta = lue_data("2025.csv")

    while True:
        print("Valitse raporttityyppi:")
        print("------------------------------------------------")
        print("1) Päiväkohtainen yhteenveto aikaväliltä")
        print("2) Kuukausikohtainen yhteenveto")
        print("3) Vuoden 2025 kokonaisyhteenveto")
        print("4) Lopeta ohjelma")
        print("------------------------------------------------")

        valinta = input("Anna valinta (1–4): ")

        if valinta == "1":
            alku = lue_pvm("Anna alkupäivä (pv.kk.vvvv): ")
            loppu = lue_pvm("Anna loppupäivä (pv.kk.vvvv): ")
            raportti = raportti_aikavali(alku, loppu, tietokanta)

        elif valinta == "2":
            while True:
                try:
                    kuukausi = int(input("Anna kuukauden numero (1–12): "))
                    if 1 <= kuukausi <= 12:
                        break
                    print("Anna numero väliltä 1–12.")
                except ValueError:
                    print("Anna numero, ei tekstiä.")

            raportti = raportti_kk(kuukausi, tietokanta)

        elif valinta == "3":
            raportti = raportti_vuosi(tietokanta)

        elif valinta == "4":
            print("Lopetetaan ohjelma... Unkka kuittaa ja kiittää")
            break

        else:
            print("Ah ah ah, you didn't choose the right magic number. Kokeile uudestaan.")
            continue  

        print("\n" + raportti)

        while True:
            print("------------------------------------------------")
            print("Mitä haluat tehdä seuraavaksi?")
            print("1) Kirjoita raportti tiedostoon raportti.txt")
            print("2) Luo uusi raportti")
            print("3) Lopeta")
            print("------------------------------------------------")

            jatko = input("Anna valinta (1–3): ")

            if jatko == "1":
                with open("raportti.txt", "w", encoding="utf-8") as f:
                    f.write(raportti)
                print("Raportti kirjoitettu tiedostoon raportti.txt\n")

            elif jatko == "2":
                break

            elif jatko == "3":
                print("Lopetetaan ohjelma... Unkka kuittaa ja kiittää")
                return  

            else:
                print("Virheellinen valinta, kokeile uudestaan\n")
               # Jos painaa väärin ei mene takaisin ensimäiseen valikkoon vaan antaa valita uudelleen

            print("------------------------------------------------")
            

if __name__ == "__main__":
    main()
