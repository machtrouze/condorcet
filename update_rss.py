import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import os

# Récupérer la clé API depuis les variables d'environnement
API_KEY = os.getenv("IDFM_API_KEY")
if not API_KEY:
    raise Exception("Clé API manquante. Configurez le secret IDFM_API_KEY dans GitHub Actions.")

API_URL = "https://prim.iledefrance-mobilites.fr/marketplace/stop-monitoring"
params = {
    "MonitoringRef": "STIF:StopPoint:Q:7619:",
    "LineRef": "STIF:Line::C00317:"
}
headers = {
    "apikey": API_KEY,
    "Accept": "application/json"
}

response = requests.get(API_URL, headers=headers, params=params)
if response.status_code != 200:
    raise Exception(f"Erreur API: {response.status_code} - {response.text}")

data = response.json()

rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Horaires Bus - Condorcet"
ET.SubElement(channel, "link").text = "https://prim.iledefrance-mobilites.fr"
ET.SubElement(channel, "description").text = "Prochains passages à l'arrêt Condorcet"

visits = data["Siri"]["ServiceDelivery"]["StopMonitoringDelivery"][0]["MonitoredStopVisit"]
for visit in visits:
    journey = visit["MonitoredVehicleJourney"]
    call = journey["MonitoredCall"]
    title = f"Bus vers {journey['DestinationName'][0]['value']} à {call['ExpectedArrivalTime']}"
    description = f"Ligne {journey['LineRef']['value']} - Arrêt {call['StopPointName'][0]['value']}"
    pub_date = datetime.fromisoformat(call["ExpectedArrivalTime"].replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S GMT")

    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "description").text = description
    ET.SubElement(item, "pubDate").text = pub_date
    ET.SubElement(item, "guid").text = visit["ItemIdentifier"]

rss_xml = ET.tostring(rss, encoding="utf-8", xml_declaration=True).decode("utf-8")
with open("horaires_bus.xml", "w", encoding="utf-8") as f:
    f.write(rss_xml)

print("Flux RSS généré et sauvegardé dans horaires_bus.xml")
