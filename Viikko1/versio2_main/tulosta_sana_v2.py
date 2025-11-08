
def main():
  
    tiedosto = "sana.txt"

   
    with open(tiedosto, "r", encoding="utf-8") as f:
        sana = f.read().strip()

   
    print(sana)



if __name__ == "__main__":
    main()