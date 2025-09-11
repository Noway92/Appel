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
from Présence import fct_general,human_like_click, get_paris_time
import numpy as np
import time

# Délai aléatoire entre 0 et 20 minutes (moyenne ~10 min)
delai = max(0, np.random.normal(loc=10, scale=3))  # loc=10 (moyenne), scale=3 (écart-type)
time.sleep(delai * 60)  # Convertit en secondes

#chrome_driver_path = 'C:/Program Files/Chrome Driver Testing/chromedriver'

options = Options()
options.add_argument("--headless")  # Obligatoire pour toi
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--lang=fr-FR")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
# Réutiliser un profil existant si possible (évite les profils temporaires)
# options.add_argument("--user-data-dir=/home/noe/.config/google-chrome/Default")
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.maximize_window()
# Ouvrir une page web
driver.get("https://www.leonard-de-vinci.net/")

adresse1 = driver.find_element(By.XPATH,"/html/body/form/div[3]/input")
adresse1.send_keys("adresse ecole")

bouton1=driver.find_element(By.XPATH,"/html/body/form/div[5]/span[2]")
human_like_click(driver, bouton1)

mdp = os.getenv("MDP")
time.sleep(max(0, np.random.normal(3, 1)))  # Moyenne 1.5s, écart-type 0.5s
adresse2 = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[2]/input")
human_like_click(driver, adresse2)
adresse2.send_keys(mdp)

bouton2=driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[4]/span")
human_like_click(driver, bouton2)

time.sleep(max(0, np.random.normal(3, 1)))  # Moyenne 1.5s, écart-type 0.5s


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
    maintenant = get_paris_time().time()
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
            delai = max(0.5, np.random.normal(loc=1.5, scale=0.5))  # en minutes
            time.sleep(delai * 60)  # Convertit en secondes

        print(f"Fin de la plage {label}")

    print("Toutes les plages sont terminées pour aujourd'hui.")
    break
