import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Nastavení
POCET_RADKU = 2000
START_DATUM = datetime(2023, 1, 1)
KONEC_DATUM = datetime(2023, 12, 31)

# Číselníky
POBOCKY = ['Praha', 'Brno', 'Ostrava', 'Plzeň', 'Liberec', 'Olomouc', 'Hradec Králové', 'České Budějovice']

PRODUKTY = {
    'Elektronika': [
        ('Notebook Pro', 25000), ('Notebook Air', 22000), ('Herní Notebook', 35000),
        ('Myš bezdrátová', 500), ('Myš herní', 1200), ('Klávesnice', 800),
        ('Monitor 24"', 3500), ('Monitor 27" 4K', 8000), ('Monitor prohnutý', 6000),
        ('Sluchátka', 1500), ('Webkamera', 1200), ('USB Hub', 400)
    ],
    'Nábytek': [
        ('Kancelářská židle', 3500), ('Herní křeslo', 5000), ('Ergo židle', 12000),
        ('Psací stůl', 4000), ('Polohovací stůl', 12000), ('Kontejner', 2500),
        ('Lampa stolní', 800), ('Lampa stojací', 1500), ('Pohovka', 15000),
        ('Knihovna', 3000), ('Regál', 1200)
    ],
    'Domácnost': [
        ('Kávovar automat', 12000), ('Kávovar pákový', 4000), ('Mlýnek na kávu', 1500),
        ('Vysavač tyčový', 5000), ('Robotický vysavač', 9000), ('Čistička vzduchu', 4500),
        ('Rychlovarná konvice', 800), ('Toustovač', 600), ('Mixér', 1200)
    ]
}

def generuj_data():
    data = []
    
    # Rozsah dat
    delta = KONEC_DATUM - START_DATUM
    
    print(f"Generuji {POCET_RADKU} řádků dat...")
    
    for _ in range(POCET_RADKU):
        # 1. Datum (s váhou pro Q4 - Vánoce)
        random_days = random.randint(0, delta.days)
        datum = START_DATUM + timedelta(days=random_days)
        
        # Větší pravděpodobnost nákupu v Q4 (říjen-prosinec)
        if datum.month >= 10:
            if random.random() > 0.3: # 70% šance, že si datum necháme, pokud je v Q4
                pass
            else:
                # Zkusíme vygenerovat jiné datum (posuneme do Q4)
                datum = datetime(2023, random.randint(10, 12), random.randint(1, 28))
        
        # 2. Kategorie a Produkt
        kategorie = random.choice(list(PRODUKTY.keys()))
        produkt_info = random.choice(PRODUKTY[kategorie])
        produkt_nazev = produkt_info[0]
        zakladni_cena = produkt_info[1]
        
        # 3. Cena (náhodná fluktuace +/- 10% a občas sleva)
        fluktuace = random.uniform(0.95, 1.05)
        cena = int(zakladni_cena * fluktuace)
        
        # Občasná "akce" (10% šance na 20% slevu)
        if random.random() < 0.1:
            cena = int(cena * 0.8)
            
        # Zaokrouhlení na desítky
        cena = round(cena / 10) * 10
        
        # 4. Množství (váha na 1 ks)
        mnozstvi = random.choices([1, 2, 3, 4, 5, 10], weights=[70, 15, 5, 3, 2, 1])[0]
        
        # 5. Pobočka (váha na velká města)
        pobocka = random.choices(
            POBOCKY, 
            weights=[30, 20, 15, 10, 5, 5, 5, 5] # Praha a Brno nejčastější
        )[0]
        
        data.append([datum.strftime("%Y-%m-%d"), produkt_nazev, kategorie, pobocka, cena, mnozstvi])
        
    # Vytvoření DataFrame
    df = pd.DataFrame(data, columns=['Datum', 'Produkt', 'Kategorie', 'Pobocka', 'Cena', 'Mnozstvi'])
    
    # Seřazení podle data
    df = df.sort_values('Datum')
    
    # Uložení
    df.to_csv('data/prodeje.csv', index=False)
    print("Hotovo! Soubor 'data/prodeje.csv' byl aktualizován.")

if __name__ == "__main__":
    generuj_data()
