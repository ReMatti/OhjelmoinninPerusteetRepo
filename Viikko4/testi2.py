"""
Ohjelma joka tulostaa tiedostosta luettujen varausten alkiot ja niiden tietotyypit

varausId | nimi | sähköposti | puhelin | varauksenPvm | varauksenKlo | varauksenKesto | hinta | varausVahvistettu | varattuTila | varausLuotu
------------------------------------------------------------------------
201 | Muumi Muumilaakso | muumi@valkoinenlaakso.org | 0509876543 | 2025-11-12 | 09:00:00 | 2 | 18.50 | True | Metsätila 1 | 2025-08-12 14:33:20
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
202 | Niiskuneiti Muumilaakso | niisku@muumiglam.fi | 0451122334 | 2025-12-01 | 11:30:00 | 1 | 12.00 | False | Kukkahuone | 2025-09-03 09:12:48
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
203 | Pikku Myy Myrsky | myy@pikkuraivo.net | 0415566778 | 2025-10-22 | 15:45:00 | 3 | 27.90 | True | Punainen Huone | 2025-07-29 18:05:11
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
204 | Nipsu Rahapulainen | nipsu@rahahuolet.me | 0442233445 | 2025-09-18 | 13:00:00 | 4 | 39.95 | False | Varastotila N | 2025-08-01 10:59:02
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
205 | Hemuli Kasvikerääjä | hemuli@kasvikeraily.club | 0463344556 | 2025-11-05 | 08:15:00 | 2 | 19.95 | True | Kasvitutkimuslabra | 2025-10-09 16:41:55
int | str | str | str | date | time | int | float | bool | str | datetime
------------------------------------------------------------------------
"""
from datetime import datetime

def muunna_varaustiedot(varaus: list) -> list:
    #print(varaus)
    
    muutettu_varaus = [] 
    muutettu_varaus.append(int(varaus[0]))
    muutettu_varaus.append(varaus[1])
    muutettu_varaus.append(varaus[2])
    muutettu_varaus.append(varaus[3])
    muutettu_varaus.append(datetime.strptime(varaus[4], "%Y-%m-%d").date())
    muutettu_varaus.append(datetime.strptime(varaus[5], "%H:%M").time())
    muutettu_varaus.append(int(varaus[6]))
    muutettu_varaus.append(float(varaus[7]))
    muutettu_varaus.append(varaus[8].lower() == "true")
    muutettu_varaus.append(varaus[9])
    muutettu_varaus.append(datetime.strptime(varaus[10], "%Y-%m-%d %H:%M:%S"))
    return muutettu_varaus


def hae_varaukset(varaustiedosto: str) -> list:
 
    varaukset = []
    varaukset.append(["varausId", "nimi", "sähköposti", "puhelin", "varauksenPvm", "varauksenKlo", "varauksenKesto", "hinta", "varausVahvistettu", "varattuTila", "varausLuotu"])
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset


def vahvistetut_varaukset(varaukset: list):
    for varaus in varaukset[1:]:  # ohita otsikko
        nimi = varaus[1]
        tila = varaus[9]
        pvm = varaus[4].strftime("%d.%m.%Y")   # suomalainen muoto
        aika = varaus[5].strftime("%H.%M")     # 10.00 muoto
        if(varaus[8]):
            print(f"- {nimi}, {tila}, {pvm} klo {aika}")

    print()


def pitkät_varaukset(varaukset: list):
    print("2) Pitkät varaukset (≥ 3 h)\n")
    for varaus in varaukset[1:]:
        if varaus[6] >= 3:
            pvm_str = varaus[4].strftime("%d.%m.%Y")
            aika_str = varaus[5].strftime("%H.%M")
            print(f"- {varaus[1]}, {varaus[4].strftime('%d.%m.%Y')} klo {varaus[5].strftime('%H.%M')}, kesto {varaus[6]} h, {varaus[9]}")

    print()


def vahvistusstatus(varaukset: list):
    print("3) Varausten vahvistusstatus\n")
    for v in varaukset[1:]:
        nuoli = " →"  # aina nimen jälkeen
        status = "Vahvistettu" if v[8] else "EI vahvistettu"
        print(f"- {v[1]}{nuoli} {status}")
    print()

    print()

def yhteenveto(varaukset: list):
    vahvistettuja = sum(1 for v in varaukset[1:] if v[8])
    ei_vahvistettuja = sum(1 for v in varaukset[1:] if not v[8])
    kaikki = len(varaukset) - 1
    print("4) Yhteenveto vahvistuksista")
    print(f"- Vahvistettuja: {vahvistettuja} kpl")
    print(f"- Ei vahvistettuja: {ei_vahvistettuja} kpl")
    print(f"- Kaikkia varauksia: {kaikki} kpl\n")


def kokonaistulot(varaukset: list):
    summa = sum(v[7] * v[6] for v in varaukset[1:] if v[8])
    print("5) Vahvistettujen varausten kokonaistulot")
    print(f"Yhteensä: {summa:.2f} €\n")


def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    pitkät_varaukset(varaukset)
    vahvistusstatus(varaukset)
    yhteenveto(varaukset)
    kokonaistulot(varaukset)

if __name__ == "__main__":
    main()
