# Export data

from logging import raiseExceptions
import pandas as pd
from pathlib import Path
import json
import os
from decouple import config
import shutil

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
export_folder_website = Path('./website_tmp')

# Create TMP Folder
if export_folder_website.exists():
    shutil.rmtree(export_folder_website)

os.mkdir(export_folder_website, )

# ----- Download Units
df = pd.read_csv(sheet_troops)

data = {
        "type": "FeatureCollection",
        "features": []
    }

# Convert date
try:
    df['date'] = pd.to_datetime(df['date'])
except:
    raise ValueError("🤬 Field 'date' could not be converted to DateTime. Please check Date column")

# Convert Lat Lng
try:
    df['lat'] = df['location'].apply(lambda x: x.replace(' ', '').split(',')[0])
    df['lng'] = df['location'].apply(lambda x: x.replace(' ', '').split(',')[1])
except:
    raise ValueError("🤬 Could not convert 'Location? into Lat Lng. Probably empty or invalid input")

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
                "icon": row['icon'],
                "type": row['type'],
                "strength": row['strength'].strip(),
                "strength_in_btg": row['strength_in_btg'],
                "unit": row['unit'].strip(),
                "number": row['number'] if pd.notna(row['number']) else None,
                "subordinate_to": row['subordinate_to'].strip(),
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
    
json.dump(data, open(export_folder / Path('./units.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)
json.dump(data, open(export_folder_website / Path('./units.json'), 'w', encoding='UTF-8'), ensure_ascii=False)
df[['lat', 'lng', 'date', 'icon', 'type', 'strength', 'strength_in_btg', 'unit', 'number', 'subordinate_to']].to_csv(export_folder / './units.csv', index=False)

# ----- Download BTGs
df = pd.read_csv(sheet_btg)

data = {
        "type": "FeatureCollection",
        "features": []
    }

try:
    df['date'] = pd.to_datetime(df['date'])
except:
    raise ValueError("🤬 Field 'date' could not be converted to DateTime. Please check Date column")

# Convert Lat Lng
try:
    df['lat'] = df['location'].apply(lambda x: x.replace(' ', '').split(',')[0])
    df['lng'] = df['location'].apply(lambda x: x.replace(' ', '').split(',')[1])
except:
    raise ValueError("🤬 Could not convert 'Location? into Lat Lng. Probably empty or invalid input")


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
    
json.dump(data, open(export_folder / Path('./btgs.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)
json.dump(data, open(export_folder_website / Path('./btgs.json'), 'w', encoding='UTF-8'), ensure_ascii=False)
df[['date', 'lat', 'lng', 'unit', 'type_of_btg']].to_csv(export_folder / './btgs.csv', index=False)

# ----- Download Assessments
df = pd.read_csv(sheet_assessments)

data = []
for i, row in df.iterrows():
    data.append({
        'date': row['date'],
        # 'date_visible': row['date_visible'],
        'text': row['text']
    })

with open(export_folder_website / Path('./assessments.json'), 'w', encoding='UTF-8') as f:
    json.dump(data, f)




