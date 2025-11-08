

def main():
    tiedosto = "sana.txt"

    try:
        with open(tiedosto, "r", encoding="utf-8") as f:
            sana = f.read().strip()

       
        if not sana:
            print("Virhe: tiedosto on tyhjä.")
            return

        
        print(sana)

    except FileNotFoundError:
        print(f"Virhe: tiedostoa '{tiedosto}' ei löytynyt.")
    except PermissionError:
        print(f"Virhe: tiedostoon '{tiedosto}' ei ole lukuoikeutta.")
    except Exception as e:
        print(f"Tuntematon virhe: {e}")


if __name__ == "__main__":
    main()