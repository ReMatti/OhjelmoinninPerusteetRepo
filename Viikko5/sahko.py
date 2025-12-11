import csv
from datetime import datetime
import calendar
from collections import defaultdict

def main():
    # Suomenkieliset viikonpäivät pienellä
    weekday_map = {
        "Monday": "maanantai",
        "Tuesday": "tiistai",
        "Wednesday": "keskiviikko",
        "Thursday": "torstai",
        "Friday": "perjantai",
        "Saturday": "lauantai",
        "Sunday": "sunnuntai"
    }

    # Tallennetaan tiedot päiväkohtaisesti
    # rakenne: {päivämäärä: {"weekday":..., "cons1":..., "prod3":...}}
    daily_data = defaultdict(lambda: {
        "cons1": 0.0, "cons2": 0.0, "cons3": 0.0,
        "prod1": 0.0, "prod2": 0.0, "prod3": 0.0,
        "weekday": ""
    })

    with open("viikko42.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            dt = datetime.fromisoformat(row["Aika"])
            date_str = dt.strftime("%d.%m.%Y")
            weekday_fi = weekday_map[calendar.day_name[dt.weekday()]]

            # Kerätään viikonpäivä kerran per päivä (vain ekalla kerralla)
            if daily_data[date_str]["weekday"] == "":
                daily_data[date_str]["weekday"] = weekday_fi

            # Lisätään kulutus ja tuotanto (Wh → kWh)
            daily_data[date_str]["cons1"] += float(row["Kulutus vaihe 1 Wh"]) / 1000
            daily_data[date_str]["cons2"] += float(row["Kulutus vaihe 2 Wh"]) / 1000
            daily_data[date_str]["cons3"] += float(row["Kulutus vaihe 3 Wh"]) / 1000

            daily_data[date_str]["prod1"] += float(row["Tuotanto vaihe 1 Wh"]) / 1000
            daily_data[date_str]["prod2"] += float(row["Tuotanto vaihe 2 Wh"]) / 1000
            daily_data[date_str]["prod3"] += float(row["Tuotanto vaihe 3 Wh"]) / 1000

    # Järjestetään päivät nousevaan järjestykseen
    sorted_dates = sorted(daily_data.keys(), key=lambda d: datetime.strptime(d, "%d.%m.%Y"))

    # Selvitetään viikon numero ensimmäisestä päivästä (jos löytyy)
    if sorted_dates:
        first_date = datetime.strptime(sorted_dates[0], "%d.%m.%Y")
        week_number = first_date.isocalendar().week
    else:
        week_number = "?"

    # Muotoilufunktio: kaksi desimaalia, pilkku
    def fnum(val):
        return f"{val:.2f}".replace(".", ",")

    # Tulostetaan taulukko
    print(f"\nViikon {week_number} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")
    header = (
        f"{'Päivä':<12} {'Pvm':<12} "
        f"{'Kulutus [kWh]':<22} {'Tuotanto [kWh]':<22}\n"
        f"{'':<12} {'(pv.kk.vvvv)':<12} {'v1':>6} {'v2':>6} {'v3':>6}   {'v1':>6} {'v2':>6} {'v3':>6}"
    )
    print(header)
    print("-" * 78)

    for date in sorted_dates:
        d = daily_data[date]
        print(
            f"{d['weekday']:<12} {date:<12} "
            f"{fnum(d['cons1']):>6} {fnum(d['cons2']):>6} {fnum(d['cons3']):>6}   "
            f"{fnum(d['prod1']):>6} {fnum(d['prod2']):>6} {fnum(d['prod3']):>6}"
        )

if __name__ == "__main__":
    main()
