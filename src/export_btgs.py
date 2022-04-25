import pandas as pd
import json
from pathlib import Path
from utils import country_from_icon

def export(CONSTS, production=True):

    # Download BTG
    df = pd.read_csv(CONSTS['SHEET_BTG'])
    df = df.sort_values('date')

    # Download Description
    df_description = pd.read_csv(CONSTS['SHEET_UNITS_DESCRIPTION'])
    df_description = df_description.drop_duplicates('unit')

    # Join and add country
    df = df.merge(df_description[['unit', 'icon']], how='left', on='unit')
    if len(df[df.icon.isna()]) > 0:
        for i, row in df[df.icon.isna()].iterrows():
            print("👉 BTG '%s' not found in unit_description. Date %s" % (row['unit'], row['date']))

        raise ValueError("Could not find BTGs in unit_description. Which ones, see above 👆")

    df['country'] = df['icon'].apply(country_from_icon)

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

    df = df[['date', 'lat', 'lng', 'unit', 'type_of_btg', 'country']]

    for i, row in df.iterrows():
        try:

            data['features'].append({
                "type": "Feature",
                "id": i,
                "properties": {
                    "date": row['date'].strftime('%Y-%m-%d'),
                    "unit": row['unit'],
                    "type_of_btg": row['type_of_btg'],
                    "country": row['country']
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
    json.dump(data, open(CONSTS['export_folder_website'] / Path('./btgs.json'), 'w', encoding='UTF-8'), ensure_ascii=False)

    if production:
        # Export Repo All
        json.dump(data, open(CONSTS['export_folder'] / Path('./geojson/btgs_all.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)
        df.to_csv(CONSTS['export_folder'] / './csv/btgs_all.csv', index=False)

        # Export Repo Current
        df[df.date == df.date.max()].to_csv(CONSTS['export_folder'] / './csv/btgs_current.csv', index=False)
        data['features'] = list(filter(lambda x: x['properties']['date'] == df.date.max().strftime('%Y-%m-%d'), data['features']))
        json.dump(data, open(CONSTS['export_folder'] / Path('./geojson/btgs_current.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)
