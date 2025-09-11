from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import discord
import os
import random
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np
import pytz

def get_paris_time():
    return datetime.now(pytz.timezone("Europe/Paris"))

def human_like_click(driver, element):
    actions = ActionChains(driver)
    actions.move_to_element_with_offset(element, 10, 10)
    actions.pause(max(0, np.random.normal(loc=1.5, scale=0.5)))
    actions.click()
    actions.perform()


def fct_general():
    def is_between(start, end, target):
        if(target>=start and target<=end):
            return True
        return False

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
    human_like_click(driver, adresse1)
    adresse1.send_keys("noe.le_yhuelic@edu.devinci.fr")

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

    bouton3=driver.find_element(By.PARTIAL_LINK_TEXT,"Relev")
    human_like_click(driver, bouton3)

    time.sleep(max(0, np.random.normal(3, 1)))  # Moyenne 1.5s, écart-type 0.5s

    #Recupérer le nombre de cours ce jour-ci

    elements = driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/table/tbody/tr")
    # Compter le nombre d'éléments trouvés
    nombre_elements = len(elements)

    test_trouver_heure=False;
    for i in range(1,nombre_elements+1):
        
        #time.sleep(2)
        info = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[1]")
        heure_cours=info.text

        # Diviser la chaîne en deux parties
        heure1, heure2 = heure_cours.split(" -")

        # Convertir chaque partie en objet datetime
        start_heure = datetime.strptime(heure1, "%H:%M")
        end_heure = datetime.strptime(heure2, "%H:%M")

        current_time = get_paris_time()  # Heure actuelle à Paris (UTC+2)
        current_time_str = current_time.strftime("%H:%M")  # Convertit en "HH:MM"
        current_time_parsed = datetime.strptime(current_time_str, "%H:%M")
        #if is_between(start_heure, end_heure, datetime.strptime(str(datetime1.hour)+":"+str(datetime1.minute), "%H:%M")):
        if is_between(start_heure, end_heure, current_time_parsed):
            test_trouver_heure=True
            bouton4=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[4]/a")
            human_like_click(driver, bouton4)
            break

    time.sleep(max(0, np.random.normal(15, 5)))  # Moyenne 1.5s, écart-type 0.5s
    print("Test1 : ",test_trouver_heure)
    if(test_trouver_heure):
        #C'est pour vérifier si l'appel est ouvert ou pas 
        bouton5 = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div")
        notif=bouton5.text
        if(bouton5.text=="""ATTENTION\nVous serez marqué "absent" si vous ne cliquez pas sur le bouton ci-dessus.\nToute validation de présence invalidée par l'intervenant pour la raison "ETUDIANT NON PRESENT" est passible de sanction par la scolarité de l'école.\nToute présence doit être effective sur toute la durée de la séance.\nVous devez être présent sur votre lieu de cours au moment où vous validez votre présence !"""):
            
            """#Cliquer sur l'appel
            boutton_appel = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/span[2]")
            boutton_appel.click()
            time.sleep"""

            notif="l'appel est ouvert" 
    else:
        notif="Tu n'a pas cours :)"
    # Fermer le navigateur
    driver.quit()

    intents = discord.Intents.default()
    intents.messages = True  # Autoriser l'accès aux événements de message

    # Initialise le client Discord avec les intentions spécifiées
    client = discord.Client(intents=intents)

    @client.event
    #C'est dans cette fonction que le bot va vraiment faire les actions
    async def on_ready():
        await send_notification(notif)

        # Arrêter le client Discord
        await client.close()

    @client.event
    async def send_notification(notif):
        channel=client.get_channel(533322569713975296)
        if notif == "l'appel est ouvert":
            await channel.send(notif)
        else:
            print(f"Notification ignored: {notif}")

    #On a écrit le TOKEN du BOT
    #Il faudra le chanegr de place pour le mettre dans la boucle
    client.run('')

    return notif

