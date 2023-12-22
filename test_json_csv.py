import pandas as pd
import json

# Charger le fichier JSON
with open('usage/gen2ou-0.json', 'r') as file:
    data = json.load(file)

# Convertir le JSON en DataFrame pandas
df = pd.DataFrame(data)

# Sauvegarder le DataFrame au format CSV
df.to_csv('test_gen2ou.csv', index=False)