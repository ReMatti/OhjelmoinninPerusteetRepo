from datetime import datetime, timedelta

def main():
    tiedosto_nimi = "varaukset.txt"
    summa = 0.0

    with open(tiedosto_nimi, "r", encoding="utf-8") as f:
        for rivi in f:
            rivi = rivi.strip()
            arvot = rivi.split("|")

            # Muuttujat
            varaus_id = arvot[0]
            nimi = arvot[1]
            paiva_iso = arvot[2]  # esim. 2025-11-16
            alkuperainen_aika = arvot[3]  # esim. 10.00
            tuntimaara = int(arvot[4])
            tuntihinta = float(arvot[5])
            maksettu = "Kyllä" if arvot[6].lower() == "true" else "Ei"
            kohde = arvot[7]
            puhelin = arvot[8]
            sahkoposti = arvot[9]

            # Muotoillaan päivämäärä suomalaiseksi
            vuosi, kuukausi, paiva = paiva_iso.split("-")
            paiva_suomi = f"{paiva}.{kuukausi}.{vuosi}"

            # Lasketaan kokonaishinta
            kokonaishinta = tuntimaara * tuntihinta
            summa += kokonaishinta

            # Muotoillaan hinnat pilkulla
            tuntihinta_str = f"{tuntihinta:.2f}".replace(".", ",")
            kokonaishinta_str = f"{kokonaishinta:.2f}".replace(".", ",")

            # Lasketaan loppumisaika (muutetaan piste kaksoispisteeksi laskentaa varten)
            aika_laskentaa_varten = alkuperainen_aika.replace(".", ":")
            aloitus_dt = datetime.strptime(f"{paiva_iso} {aika_laskentaa_varten}", "%Y-%m-%d %H:%M")
            loppu_dt = aloitus_dt + timedelta(hours=tuntimaara)
            loppuaika = loppu_dt.strftime("%H.%M")  # Tulostetaan pisteellä

            # Tulostetaan varaus
            print(f"""
Varausnumero: {varaus_id}
Varaaja: {nimi}
Päivämäärä: {paiva_suomi}
Aloitusaika: {alkuperainen_aika}
Loppumisaika: {loppuaika}
Tuntimäärä: {tuntimaara}
Tuntihinta: {tuntihinta_str} €
Kokonaishinta: {kokonaishinta_str} €
Maksettu: {maksettu}
Kohde: {kohde}
Puhelin: {puhelin}
Sähköposti: {sahkoposti}
""")

    # Yhteenveto
    summa_str = f"{summa:.2f}".replace(".", ",")
    print(f"Kaikkien varausten kokonaishinta yhteensä: {summa_str} €")

if __name__ == "__main__":
    main()