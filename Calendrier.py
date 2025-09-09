from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import discord
import os
from bs4 import BeautifulSoup
import re
import random
from selenium.webdriver.chrome.options import Options
from Présence import fct_general


#chrome_driver_path = 'C:/Program Files/Chrome Driver Testing/chromedriver'

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--headless")  # si tu veux sans interface
options.add_argument("--user-data-dir=/tmp/unique-profile")  # chemin temporaire

driver = webdriver.Chrome(options=options)
driver.maximize_window()
# Ouvrir une page web
driver.get("https://www.leonard-de-vinci.net/")

adresse1 = driver.find_element(By.XPATH,"/html/body/form/div[3]/input")
adresse1.send_keys("noe.le_yhuelic@edu.devinci.fr")

bouton1=driver.find_element(By.XPATH,"/html/body/form/div[5]/span[2]")
bouton1.click()

mdp = os.getenv("MDP")
time.sleep(2)
adresse2 = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[2]/input")
adresse2.send_keys(mdp)

bouton2=driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[4]/span")
bouton2.click()

time.sleep(2)


today = datetime.now().strftime("%Y-%m-%d")

soup = BeautifulSoup(driver.page_source, "html.parser")

driver.quit()

element = soup.find("div", {
    "data-date": today,
    "class": ["b-dayview-day-detail b-calendar-cell b-today"]
})


tab_heures = {}
if element:
    divs = element.find_all("div", attrs={"tabindex": "0"})
    compteur=0
    for div in divs:
        inter=div.get_text(strip=True)
        # Expression régulière pour deux horaires au format HH:MM collés
        match = re.match(r"(\d{1,2}:\d{2})(\d{1,2}:\d{2})", inter)

        if match:
            start_time = match.group(1)
            end_time = match.group(2)
            tab_heures[compteur]=[start_time,end_time]
            compteur+=1
else:
    print("pas de cours aujourd'hui")

def dans_plage(h_debut, h_fin):
    maintenant = datetime.now().time()
    h_debut = datetime.strptime(h_debut, "%H:%M").time()
    h_fin = datetime.strptime(h_fin, "%H:%M").time()
    return h_debut <= maintenant < h_fin

while True:
    now = datetime.now()
    heure_actuelle = now.time()

    for label, (h_debut, h_fin) in tab_heures.items():
        # Attendre jusqu'à ce qu'on atteigne l'heure de début
        while not dans_plage(h_debut, h_fin):
            print(f"En attente de la plage {label}...")
            time.sleep(300)  # Attendre 120 avant de re-check

        # Quand on entre dans la plage, lancer le script toutes les 3 minutes
        print(f"Début de la plage {label} ({h_debut} - {h_fin})")
        while dans_plage(h_debut, h_fin):
            reponse = fct_general()
            if re.match(r"^Vous avez été noté présent", reponse):
                break
            time.sleep(120)  # 2 minutes
            delai = random.uniform(0, 120)
            time.sleep(delai)

        print(f"Fin de la plage {label}")

    print("Toutes les plages sont terminées pour aujourd'hui.")
    break
