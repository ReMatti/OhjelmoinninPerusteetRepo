import csv
from datetime import datetime
import calendar

def main():
    # --- Suomenkieliset viikonpäivät pienellä ---
    weekday_map = {
        "Monday": "maanantai",
        "Tuesday": "tiistai",
        "Wednesday": "keskiviikko",
        "Thursday": "torstai",
        "Friday": "perjantai",
        "Saturday": "lauantai",
        "Sunday": "sunnuntai"
    }

    # Lista päivittäisille tuloksille
    results = []

    # --- LUETAAN CSV ---
    with open("viikko42.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=';')

        for row in reader:
            dt = datetime.fromisoformat(row["Aika"])

            # Päivämäärä pv.kk.vvvv
            date_str = dt.strftime("%d.%m.%Y")

            # Viikonpäivä suomeksi
            weekday_fi = weekday_map[calendar.day_name[dt.weekday()]]

            # Wh → kWh, 2 desimaalia ja pilkku
            def fnum(v):
                return f"{float(v)/1000:.2f}".replace(".", ",")

            cons1 = fnum(row["Kulutus vaihe 1 Wh"])
            cons2 = fnum(row["Kulutus vaihe 2 Wh"])
            cons3 = fnum(row["Kulutus vaihe 3 Wh"])

            prod1 = fnum(row["Tuotanto vaihe 1 Wh"])
            prod2 = fnum(row["Tuotanto vaihe 2 Wh"])
            prod3 = fnum(row["Tuotanto vaihe 3 Wh"])

            results.append({
                "weekday": weekday_fi,
                "date": date_str,
                "cons1": cons1, "cons2": cons2, "cons3": cons3,
                "prod1": prod1, "prod2": prod2, "prod3": prod3,
            })

    # Viikon numero ensimmäisestä päivästä
    if results:
        week_number = datetime.strptime(results[0]["date"], "%d.%m.%Y").isocalendar().week
    else:
        week_number = "?"

    # --- TULOSTUS ---
    print(f"\nViikon {week_number} sähkönkulutus ja -tuotanto (kWh, vaiheittain)\n")

    header = (
        f"{'Päivä':<12} {'Pvm':<12} "
        f"{'Kulutus [kWh]':<22} {'Tuotanto [kWh]':<22}\n"
        f"{'':<12} {'(pv.kk.vvvv)':<12} {'v1':>6} {'v2':>6} {'v3':>6}   {'v1':>6} {'v2':>6} {'v3':>6}"
    )
    print(header)
    print("-" * 78)

    for r in results:
        print(
            f"{r['weekday']:<12} {r['date']:<12} "
            f"{r['cons1']:>6} {r['cons2']:>6} {r['cons3']:>6}   "
            f"{r['prod1']:>6} {r['prod2']:>6} {r['prod3']:>6}"
        )

if __name__ == "__main__":
    main()
