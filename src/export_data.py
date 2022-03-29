# Export data

import pandas as pd
from pathlib import Path
import json
import os
from decouple import config

# Load env Vars
sheet_troops = os.getenv("SHEET_TROOPS", None)
if not sheet_troops:
    sheet_troops = config("SHEET_TROOPS")

sheet_assessments = os.getenv("SHEET_ASSESSMENTS", None)
if not sheet_assessments:
    sheet_assessments = config("SHEET_ASSESSMENTS")

sheet_btg = os.getenv("SHEET_BTG", None)
if not sheet_btg:
    sheet_btg = config("SHEET_BTG")

export_folder = Path('./data/')


# ----- Download Units
df = pd.read_csv(sheet_troops)

data = {
        "type": "FeatureCollection",
        "features": []
    }

try:
    df['date'] = pd.to_datetime(df['date'])
except:
    print("🤬 Field 'date' could not be converted to DateTime. Please check Date column")
    print("")
    pass

for i, row in df.iterrows():
    try:
        coords = row['location'].replace(' ', '').split(',')

        if len(coords) < 2:
            raise ValueError('Wrong coordinates: %s' % list(row))

        data['features'].append({
            "type": "Feature",
            "id": i,
            "properties": {
                "date": row['date'].strftime('%Y-%m-%d'),
                "type": row['type'],
                "icon": row['icon'],
                "number": row['number'] if pd.notna(row['number']) else None,
                "strength": row['strength'].strip(),
                "strength_in_btg": row['strength_in_btg'],
                "unit": row['unit'].strip(),
                "subordinate_to": row['subordinate_to'].strip(),
                "direction": row['direction'],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(coords[1]), float(coords[0])]
            }
        })
    except Exception as e:
        print("🥵 Something wroing in row %s in Sheet troops" % (i + 1))
        print(list(row))
        print("ℹ️ Errormessage: %s" % e)
        pass
        break
    
with open(export_folder / Path('./units.json'), 'w', encoding='UTF-8') as f:
    json.dump(data, f, ensure_ascii=False)

# ----- Download BTGs
df = pd.read_csv(sheet_btg)

data = {
        "type": "FeatureCollection",
        "features": []
    }

try:
    df['date'] = pd.to_datetime(df['date'])
except:
    print("🤬 Field 'date' could not be converted to DateTime. Please check Date column")
    print("")
    pass

for i, row in df.iterrows():
    try:
        coords = row['location'].replace(' ', '').split(',')

        if len(coords) < 2:
            raise ValueError('Wrong coordinates: %s' % list(row))

        data['features'].append({
            "type": "Feature",
            "id": i,
            "properties": {
                "date": row['date'].strftime('%Y-%m-%d'),
                "unit": row['unit'],
                "type_of_btg": row['type_of_btg']
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(coords[1]), float(coords[0])]
            }
        })
    except Exception as e:
        print("🥵 Something wroing in row %s in sheet BTG" % (i + 1))
        print(list(row))
        print("ℹ️ Errormessage: %s" % e)
        pass
        break
    
with open(export_folder / Path('./btgs.json'), 'w', encoding='UTF-8') as f:
    json.dump(data, f, ensure_ascii=False)

# ----- Download Assessments
df = pd.read_csv(sheet_assessments)

data = []
for i, row in df.iterrows():
    data.append({
        'date': row['date'],
        # 'date_visible': row['date_visible'],
        'text': row['text']
    })

with open(export_folder / Path('./assessments.json'), 'w', encoding='UTF-8') as f:
    json.dump(data, f)




