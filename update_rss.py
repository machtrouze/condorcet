
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import os

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv("IDFM_API_KEY")
if not API_KEY:
    raise Exception("Clé API manquante. Configurez le secret IDFM_API_KEY dans GitHub Actions.")

# URL de l'API
API_URL = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring"

# Paramètres de la requête
params = {
    "MonitoringRef": "STIF:StopPoint:Q:7619:",  # ID de l'arrêt
    "LineRef": "STIF:Line::C00317:"            # ID de la ligne (optionnel)
}

# Headers avec clé API
headers = {
    "apikey": API_KEY,
    "Accept": "application/json"
}

# Appel API
response = requests.get(API_URL, headers=headers, params=params)
if response.status_code != 200:
    raise Exception(f"Erreur API: {response.status_code} - {response.text}")

data = response.json()

# Création du flux RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Horaires Bus - Condorcet"
ET.SubElement(channel, "link").text = "https://prim.iledefrance-mobilites.fr"
ET.SubElement(channel, "description").text = "Affichage du prochain horaire de passage (GMT+1)"

# Extraire le prochain passage
visits = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"][:3]

for visit in visits:
    call = visit["MonitoredVehicleJourney"]["MonitoredCall"]
    destination = visit["MonitoredVehicleJourney"]['DestinationName'][0]['value']
    # Convertir en datetime et ajouter +1 heure pour GMT+1
    heure_passage = datetime.fromisoformat(call["ExpectedArrivalTime"].replace("Z", "+00:00")) + timedelta(hours=1)
    heure_formatee = heure_passage.strftime("%H:%M")

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = f"Prochain bus à {heure_formatee}"
    ET.SubElement(item, "description").text = f"vers {destination}"
    ET.SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    ET.SubElement(item, "guid").text = call["ExpectedArrivalTime"]

# Sauvegarde du fichier RSS
rss_xml = ET.tostring(rss, encoding="utf-8", xml_declaration=True).decode("utf-8")
with open("horaires_bus.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)

print("Flux RSS généré avec les 3 prochains passages (heures en GMT+1).")
