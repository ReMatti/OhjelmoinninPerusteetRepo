# Copyright (c) 2025 Ville Heikkiniemi
#
# This code is licensed under the MIT License.
# You are free to use, modify, and distribute this code,
# provided that the original copyright notice is retained.
#
# See LICENSE file in the project root for full license information.


# Käytän sanakirjoja tässä. En ole vielä tutustunut olio ohjelmointiin niin hyvin, mutta aion ottaa siitäkin selvää. 
# #Tämä sopii hyvin tiedostojen lukemiseen johon on helppoo lisätä asioita tai poistaa.
# Sanakirjan etuna on että erillisinä tietoina olevat tiedot on tallennettu nimetyn avaimen taakse. 
# Sanakirjaa voi käyttää myös tiedon ryhmittelysssä.
# Sanakirjat kuvaavat dataa selkeästi, esim. mikä tekee koodista helpommin luettavaa ja ymmärrettävää.
# Sopii hyvin tiedon lukemiseen, esim. tiedostot, JSON


from datetime import datetime

def muunna_varaustiedot(varaus_lista: list) -> dict:
    return{
        "id": int(varaus_lista[0]),
        "nimi": varaus_lista[1],
        "sahkoposti": varaus_lista[2],
        "puhelin": varaus_lista[3],
        "paiva": datetime.strptime(varaus_lista[4], "%Y-%m-%d").date(),
        "kellonaika": datetime.strptime(varaus_lista[5], "%H:%M").time(),
        "kesto": int(varaus_lista[6]),
        "hinta": float(varaus_lista[7]),
        "vahvistettu": varaus_lista[8].lower() == "true",
        "kohde": varaus_lista[9],
        "luotu": datetime.strptime(varaus_lista[10], "%Y-%m-%d %H:%M:%S"),
    }
    

def hae_varaukset(varaustiedosto: str) -> list[dict]:
    varaukset = []
    
    with open(varaustiedosto, "r", encoding="utf-8") as f:
        for varaus in f:
            varaus = varaus.strip()
            varaustiedot = varaus.split('|')
            varaukset.append(muunna_varaustiedot(varaustiedot))
    return varaukset

def vahvistetut_varaukset(varaukset: list[dict]):
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            print(
                f"- {varaus['nimi']}, {varaus['kohde']}, "
                f"{varaus['paiva'].strftime('%d.%m.%Y')} "
                f"klo {varaus['kellonaika'].strftime('%H.%M')}"
            )

    print()

def pitkat_varaukset(varaukset: list[dict]):
     for varaus in varaukset:
        if varaus["kesto"] >= 3:
            print(
                f"- {varaus['nimi']}, "
                f"{varaus['paiva'].strftime('%d.%m.%Y')} "
                f"klo {varaus['kellonaika'].strftime('%H.%M')}, "
                f"kesto {varaus['kesto']} h, {varaus['kohde']}"
            )
     print()

def varausten_vahvistusstatus(varaukset: list[dict]):
        for varaus in varaukset:
            status = "Vahvistettu" if varaus["vahvistettu"] else "EI vahvistettu"
            print(f"{varaus['nimi']} → {status}")

        print()

def varausten_lkm(varaukset: list):
    vahvistetutVaraukset = 0
    eiVahvistetutVaraukset = 0

    for varaus in varaukset:
        if varaus["vahvistettu"]:
            vahvistetutVaraukset += 1
        else:
            eiVahvistetutVaraukset += 1

    print(f"- Vahvistettuja varauksia: {vahvistetutVaraukset} kpl")
    print(f"- Ei-vahvistettuja varauksia: {eiVahvistetutVaraukset} kpl")
    print()

def varausten_kokonaistulot(varaukset: list):
    varaustenTulot = 0
    for varaus in varaukset:
        if varaus["vahvistettu"]:
            varaustenTulot += varaus["kesto"]*varaus["hinta"]

    print(
        "Vahvistettujen varausten kokonaistulot:",
          f"{varaustenTulot:.2f}".replace('.', ','),
          "€"
    )
    print()

def main():
    varaukset = hae_varaukset("varaukset.txt")
    print("1) Vahvistetut varaukset")
    vahvistetut_varaukset(varaukset)
    print("2) Pitkät varaukset (≥ 3 h)")
    pitkat_varaukset(varaukset)
    print("3) Varausten vahvistusstatus")
    varausten_vahvistusstatus(varaukset)
    print("4) Yhteenveto vahvistuksista")
    varausten_lkm(varaukset)
    print("5) Vahvistettujen varausten kokonaistulot")
    varausten_kokonaistulot(varaukset)

if __name__ == "__main__":
    main()