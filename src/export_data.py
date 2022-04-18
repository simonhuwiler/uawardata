# Export data

import pandas as pd
from pathlib import Path
import json
import os
from decouple import config
import shutil

# Load env Vars
SHEET_UNITS_POSITION = os.getenv("SHEET_UNITS_POSITION", None)
if not SHEET_UNITS_POSITION:
    SHEET_UNITS_POSITION = config("SHEET_UNITS_POSITION")

SHEET_UNITS_DESCRIPTION = os.getenv("SHEET_UNITS_DESCRIPTION", None)
if not SHEET_UNITS_DESCRIPTION:
    SHEET_UNITS_DESCRIPTION = config("SHEET_UNITS_DESCRIPTION")

SHEET_ASSESSMENTS = os.getenv("SHEET_ASSESSMENTS", None)
if not SHEET_ASSESSMENTS:
    SHEET_ASSESSMENTS = config("SHEET_ASSESSMENTS")

SHEET_BTG = os.getenv("SHEET_BTG", None)
if not SHEET_BTG:
    SHEET_BTG = config("SHEET_BTG")

export_folder = Path('./data/')
export_folder_website = Path('./website_tmp')

# Create TMP Folder
if export_folder_website.exists():
    shutil.rmtree(export_folder_website)

os.mkdir(export_folder_website, )

# ----- Download Units
df = pd.read_csv(SHEET_UNITS_POSITION)

df_description = pd.read_csv(SHEET_UNITS_DESCRIPTION)

# Merge
df = df.merge(df_description, how='left', on='unit')
if len(df[df.icon.isna()]) > 0:
    print(df[df.icon.isna()])
    raise ValueError("🤬 Unit Position withouth corresponding Unit in 'units_description'")

# Sort values
df = df.sort_values(['date', 'unitnumber'])

data = {
        "type": "FeatureCollection",
        "features": []
    }

# Fill nas
df['subordinate_to'] = df['subordinate_to'].fillna('')
df['unit'] = df['unit'].fillna('')

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

df = df[['date', 'lat', 'lng', 'icon', 'type', 'strength', 'strength_in_btg_text', 'strength_in_btg_number', 'unit', 'unitnumber', 'subordinate_to']]

for i, row in df.iterrows():
    try:
        data['features'].append({
            "type": "Feature",
            "id": i + 1,
            "properties": {
                "date": row['date'].strftime('%Y-%m-%d'),
                "icon": row['icon'],
                "type": row['type'],
                "strength": row['strength'].strip(),
                #"strength_in_btg": row['strength_in_btg_text'],
                "strength_in_btg_number": row['strength_in_btg_number'],
                "strength_in_btg_text": row['strength_in_btg_text'],
                "unit": row['unit'].strip(),
                "unitnumber": row['unitnumber'] if pd.notna(row['unitnumber']) else None,
                "subordinate_to": row['subordinate_to'].strip(),
            },
            "geometry": {
                "type": "Point",
                "coordinates": [float(row['lng']), float(row['lat'])]
            }
        })
    except Exception as e:
        print("🥵 Something wroing in row %s in Sheet troops" % (i + 1))
        print(list(row))
        print("ℹ️ Errormessage: %s" % e)
        pass
        break
    
# Export website
json.dump(data, open(export_folder_website / Path('./units.json'), 'w', encoding='UTF-8'), ensure_ascii=False)

# Export Repo All
json.dump(data, open(export_folder / Path('./geojson/units_all.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)
df.to_csv(export_folder / './csv/units_all.csv', index=False)

# Export Repo Current
df[df.date == df.date.max()].to_csv(export_folder / './csv/units_current.csv', index=False)
data['features'] = list(filter(lambda x: x['properties']['date'] == df.date.max().strftime('%Y-%m-%d'), data['features']))
json.dump(data, open(export_folder / Path('./geojson/units_current.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)

# ----- Download BTGs
df = pd.read_csv(SHEET_BTG)
df = df.sort_values('date')

# Remove empty types
df = df[df['type_of_btg'].notna()]

# Fillna
df['unit'] = df['unit'].fillna('')

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

df = df[['date', 'lat', 'lng', 'unit', 'type_of_btg']]

for i, row in df.iterrows():
    try:

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
                "coordinates": [float(row['lng']), float(row['lat'])]
            }
        })
    except Exception as e:
        print("🥵 Something wroing in row %s in sheet BTG" % (i + 1))
        print(list(row))
        print("ℹ️ Errormessage: %s" % e)
        pass
        break
    
# Export Website
json.dump(data, open(export_folder_website / Path('./btgs.json'), 'w', encoding='UTF-8'), ensure_ascii=False)

# Export Repo All
json.dump(data, open(export_folder / Path('./geojson/btgs_all.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)
df.to_csv(export_folder / './csv/btgs_all.csv', index=False)

# Export Repo Current
df[df.date == df.date.max()].to_csv(export_folder / './csv/btgs_current.csv', index=False)
data['features'] = list(filter(lambda x: x['properties']['date'] == df.date.max().strftime('%Y-%m-%d'), data['features']))
json.dump(data, open(export_folder / Path('./geojson/btgs_current.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)


# ----- Download Assessments
df = pd.read_csv(SHEET_ASSESSMENTS)
df = df.sort_values('date')
df['text'] = df['text'].fillna('')

data = []
for i, row in df.iterrows():
    data.append({
        'date': row['date'],
        # 'date_visible': row['date_visible'],
        'text': row['text']
    })

with open(export_folder_website / Path('./assessments.json'), 'w', encoding='UTF-8') as f:
    json.dump(data, f)




