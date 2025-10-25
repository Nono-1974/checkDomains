import requests
import pandas as pd
from datetime import datetime

# Fichier texte en entrée (noms de domaines)
input_file = "domaines.txt"

# Fichier Excel de sortie
output_file = f"resultats_dns_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

def get_ip_from_google_dns(domain):
    """Effectue une requête DNS publique via Google DNS-over-HTTPS"""
    api_url = f"https://dns.google/resolve?name={domain}&type=A"
    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()

        if "Answer" in data:
            # On garde uniquement les enregistrements A (IPv4)
            ips = [a["data"] for a in data["Answer"] if a.get("type") == 1]
            if ips:
                return ", ".join(ips)
        return "Domaine inexistant ou sans enregistrement A"
    except Exception as e:
        return f"Erreur : {type(e).__name__}"

# Lecture des domaines dans le fichier texte
with open(input_file, "r", encoding="utf-8") as f:
    domaines = [line.strip() for line in f if line.strip()]

# Résolution DNS et stockage des résultats
resultats = []
for domaine in domaines:
    print(f"🔍 Vérification de {domaine} ...")
    ip = get_ip_from_google_dns(domaine)
    resultats.append({"Nom de domaine": domaine, "Résultat": ip})

# Création d’un DataFrame pandas
df = pd.DataFrame(resultats)

# Export direct vers Excel (.xlsx)
df.to_excel(output_file, index=False)

print(f"\n✅ Fichier Excel créé : {output_file}")
