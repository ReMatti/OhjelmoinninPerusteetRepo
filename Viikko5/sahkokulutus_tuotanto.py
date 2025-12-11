import csv
from datetime import datetime
import calendar

def main():
    # Sanakirja tietojen keräämiseen per viikonpäivä
    # weekday_totals["Monday"]["cons1"], ["prod2"] jne.
    weekday_totals = {
        day: {
            "cons1": 0.0, "cons2": 0.0, "cons3": 0.0,
            "prod1": 0.0, "prod2": 0.0, "prod3": 0.0
        }
        for day in calendar.day_name
    }

    # LUETAAN CSV-TIEDOSTO
    with open("data.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            # Aika → datetime → viikonpäivä
            dt = datetime.fromisoformat(row["Aika"])
            weekday = calendar.day_name[dt.weekday()]  # Monday, Tuesday, ...

            # Parsitaan luvut (Wh → kWh)
            cons1 = float(row["Kulutus vaihe 1 Wh"]) / 1000
            cons2 = float(row["Kulutus vaihe 2 Wh"]) / 1000
            cons3 = float(row["Kulutus vaihe 3 Wh"]) / 1000

            prod1 = float(row["Tuotanto vaihe 1 Wh"]) / 1000
            prod2 = float(row["Tuotanto vaihe 2 Wh"]) / 1000
            prod3 = float(row["Tuotanto vaihe 3 Wh"]) / 1000

            # Lisätään summiin
            weekday_totals[weekday]["cons1"] += cons1
            weekday_totals[weekday]["cons2"] += cons2
            weekday_totals[weekday]["cons3"] += cons3

            weekday_totals[weekday]["prod1"] += prod1
            weekday_totals[weekday]["prod2"] += prod2
            weekday_totals[weekday]["prod3"] += prod3

    # Tulostetaan taulukko
    print("\nSähkönkulutus ja -tuotanto (kWh) per viikonpäivä:\n")

    header = (
        f"{'Päivä':<10} | "
        f"{'Cons1':>7} {'Cons2':>7} {'Cons3':>7} | "
        f"{'Prod1':>7} {'Prod2':>7} {'Prod3':>7}"
    )
    print(header)
    print("-" * len(header))

    for day in calendar.day_name:
        d = weekday_totals[day]
        print(
            f"{day:<10} | "
            f"{d['cons1']:7.3f} {d['cons2']:7.3f} {d['cons3']:7.3f} | "
            f"{d['prod1']:7.3f} {d['prod2']:7.3f} {d['prod3']:7.3f}"
        )


if __name__ == "__main__":
    main()

