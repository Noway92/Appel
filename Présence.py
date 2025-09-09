from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import discord
import os
import random

def fct_general():
    def is_between(start, end, target):
        if(target>=start and target<=end):
            return True
        return False

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
    adresse1.send_keys("Mettre votre adresse Devinci")

    bouton1=driver.find_element(By.XPATH,"/html/body/form/div[5]/span[2]")
    bouton1.click()

    mdp = os.getenv("MDP")
    delai = random.uniform(2, 4)
    time.sleep(delai)
    adresse2 = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[2]/input")
    adresse2.send_keys(mdp)

    bouton2=driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[4]/span")
    bouton2.click()

    delai = random.uniform(2, 4)
    time.sleep(delai)

    bouton3=driver.find_element(By.PARTIAL_LINK_TEXT,"Relev")
    bouton3.click()

    delai = random.uniform(2, 4)
    time.sleep(delai)

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
        #if is_between(start_heure, end_heure, datetime.strptime(str(datetime1.hour)+":"+str(datetime1.minute), "%H:%M")):
        if is_between(start_heure, end_heure, datetime.strptime(str(datetime.now().hour)+":"+str(datetime.now().minute), "%H:%M")):
            test_trouver_heure=True
            bouton4=driver.find_element(By.XPATH,"/html/body/div[1]/div/div[3]/div[2]/div/div/div[2]/table/tbody/tr["+str(i)+"]/td[4]/a")
            bouton4.click()
            break

    delai = random.uniform(2, 15)
    time.sleep(delai)
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
    client.run('Mettre son Propre id ici :)')

    return notif





