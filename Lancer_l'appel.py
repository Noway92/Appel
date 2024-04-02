from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import discord

datetime1 = datetime.strptime("17:30", "%H:%M")
def is_between(start, end, target):
    if(target>=start and target<=end):
        return True
    return False

#chrome_driver_path = 'C:/Program Files/Chrome Driver Testing/chromedriver'

# Initialisation du navigateur Chrome
driver = webdriver.Chrome()
driver.maximize_window()
# Ouvrir une page web
driver.get("https://www.leonard-de-vinci.net/")

adresse1 = driver.find_element(By.XPATH,"/html/body/div[1]/form/div[3]/input")
mail = input("Donne ton adresse email :")
adresse1.send_keys(mail)

bouton1=driver.find_element(By.XPATH,"/html/body/div[1]/form/div[5]/span[2]")
bouton1.click()

time.sleep(2)

adresse2 = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[2]/input")
mdp = input("Donne ton mot de passe : ")
time.sleep(10)
adresse2.send_keys(mdp)


bouton2=driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div/main/div/div/div/form/div[2]/div[4]/span")
bouton2.click()

time.sleep(2)

bouton3=driver.find_element(By.PARTIAL_LINK_TEXT,"Relev")
bouton3.click()

time.sleep(2)

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

time.sleep(2)

if(test_trouver_heure):
    #C'est pour vérifier si l'appel est ouvert ou pas 
    bouton5 = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/div")
    notif=bouton5.text
    if(bouton5.text=="""ATTENTION\nVous serez marqué "absent" si vous ne cliquez pas sur le bouton ci-dessus.\nToute validation de présence invalidée par l'intervenant pour la raison "ETUDIANT NON PRESENT" est passible de sanction par la scolarité de l'école.\nToute présence doit être effective sur toute la durée de la séance.\nVous devez être présent sur votre lieu de cours au moment où vous validez votre présence !"""):
        #Cliquer sur l'appel
        boutton_appel = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[3]/div/div[2]/div/div[2]/span[2]")
        boutton_appel.click()
        time.sleep
        notif="Vous venez de validez votre présence"
    
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
    #print(f'Connecté en tant que {client.user}')
    await send_notification(notif)

@client.event
async def send_notification(notif):
    channel=client.get_channel(#Ecrire son propre channel)
    await channel.send(notif)
    '''
    if(notif=="l'appel n'est pas encore ouvert ou à déjà été validé"):
        await channel.send("l'appel n'est pas encore ouvert ou à déjà été validé")
    else:
        await channel.send("l'appel est validé")
    '''
    

#On a écrit le TOKEN du BOT
#Il faudra le changer de place pour le mettre dans la boucle
client.run(#ECRIRE SON PROPRE TOKEN du BOT)






