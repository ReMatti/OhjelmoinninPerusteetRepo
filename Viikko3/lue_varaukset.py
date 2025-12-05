"""
Ohjelma joka lukee tiedostossa olevat varaustiedot
ja tulostaa ne konsoliin käyttäen funkitoita.
Alla esimerkkitulostus:

Varausnumero: 123
Varaaja: Anna Virtanen
Päivämäärä: 31.10.2025
Aloitusaika: 10.00
Tuntimäärä: 2
Tuntihinta: 19,95 €
Kokonaishinta: 39,90 €
Maksettu: Kyllä
Kohde: Kokoustila A
Puhelin: 0401234567
Sähköposti: anna.virtanen@example.com

"""
from datetime import datetime

def hae_varausnumero(varaus: list[str]) -> str:
    varausnumero = int(varaus[0])
    return varausnumero

def hae_varaaja(varaus: list[str]) -> str:
    nimi = varaus[1]
    return nimi

def hae_paiva(varaus: list[str]) -> datetime:
    paivamaara = datetime.strptime(varaus[2], "%Y-%m-%d").date()
    suomalainenpvm = paivamaara.strftime("%d.%m.%Y")
    return suomalainenpvm

def hae_aloitusaika(varaus: list[str]) -> datetime:
    aloitusaika = datetime.strptime(varaus[3], "%H:%M").time()
    suomalainenaika = aloitusaika.strftime("%H.%M")
    return suomalainenaika

def hae_tuntimaara(varaus: list[str]) -> str:
    tuntimaara = int(varaus[4])
    return tuntimaara

def hae_tuntihinta(varaus: list[str]) -> float:
    tuntihinta = float(varaus[5])
    tuntihinta_str = f"{tuntihinta:.2f}".replace(".", ",")
    return tuntihinta_str

def laske_kokonaishinta(varaus: list[str]) -> float:
    kokonaishinta = int(varaus[4]) * float(varaus[5])
    kokonaishinta_str = f"{kokonaishinta:.2f}".replace(".", ",")
    return kokonaishinta_str
    
def hae_maksettu(varaus: list[str]) -> str:
    maksettu = varaus[6]
    return maksettu

def hae_kohde(varaus: list[str]) -> str:
    kohde = varaus[7]
    return kohde

def hae_puhelin(varaus: list[str]) -> str:
    puhelin = varaus[8]
    return puhelin

def hae_sahkoposti(varaus: list[str]) -> str:
    sahkoposti = varaus[9]
    return sahkoposti

def tulosta_varaus(varaus):
    print(f"Varausnumero: {hae_varausnumero(varaus)}")
    print(f"Varaaja: {hae_varaaja(varaus)}")
    print(f"Päivämäärä: {hae_paiva(varaus)}")
    print(f"Aloitusaika: {hae_aloitusaika(varaus)}")
    print(f"Tuntimäärä: {hae_tuntimaara(varaus)} ")
    print(f"Tuntihinta: {hae_tuntihinta(varaus)} €")
    print(f"Kokonaishinta {laske_kokonaishinta(varaus)} €")
    print(f"Maksettu {"Kyllä" if hae_maksettu(varaus) else "Ei"}")
    print(f"Kohde: {hae_kohde(varaus)}")
    print(f"Puhelin: {hae_puhelin(varaus)}")
    print(f"Sähköposti: {hae_sahkoposti(varaus)}")


def main():
    # Maaritellaan tiedoston nimi suoraan koodissa
    varaukset = "varaukset.txt"

    # Avataan tiedosto ja luetaan rivit listaksi
    with open(varaukset, "r", encoding="utf-8") as f:
        rivit = f.readlines()

    
# Käydään läpi jokainen varaus
    for rivi in rivit:
        varaus = rivi.strip().split('|')
        tulosta_varaus(varaus)
        print("-" * 40)



if __name__ == "__main__":
    main()