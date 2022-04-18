import pandas as pd
import json
from pathlib import Path

def export_repo(CONSTS):
    df = pd.read_csv(CONSTS['SHEET_UNITS_POSITION'])

    df_description = pd.read_csv(CONSTS['SHEET_UNITS_DESCRIPTION'])

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

    # Export website XXX REMOVE HERE!
    json.dump(data, open(CONSTS['export_folder_website'] / Path('./units.json'), 'w', encoding='UTF-8'), ensure_ascii=False)
        
    # Export Repo All
    json.dump(data, open(CONSTS['export_folder'] / Path('./geojson/units_all.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)
    df.to_csv(CONSTS['export_folder'] / './csv/units_all.csv', index=False)

    # Export Repo Current
    df[df.date == df.date.max()].to_csv(CONSTS['export_folder'] / './csv/units_current.csv', index=False)
    data['features'] = list(filter(lambda x: x['properties']['date'] == df.date.max().strftime('%Y-%m-%d'), data['features']))
    json.dump(data, open(CONSTS['export_folder'] / Path('./geojson/units_current.geojson'), 'w', encoding='UTF-8'), ensure_ascii=False)

    


    # ----------- EXPORT WEBSITE
def export_website(CONSTS):
    df = pd.read_csv(CONSTS['SHEET_UNITS_POSITION'])

    df_description = pd.read_csv(CONSTS['SHEET_UNITS_DESCRIPTION'])

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

    # add Grouper
    df['_group'] = df.apply(lambda row: "%s-%s-%s" % (row['date'], row['lat'], row['lng']), axis=1)
    df = df.groupby(['_group', 'unit']).first()

    counter = 0
    for i, new_df in df.groupby(level=0):
        try:
            units = []
            icons = []

            new_df = new_df.reset_index()

            for j, row in new_df.iterrows():

                units.append({
                        "icon": row['icon'],
                        "type": row['type'],
                        "strength": row['strength'].strip(),
                        "strength_in_btg_number": row['strength_in_btg_number'],
                        "strength_in_btg_text": row['strength_in_btg_text'],
                        "unit": row['unit'].strip(),
                        "unitnumber": row['unitnumber'] if pd.notna(row['unitnumber']) else None,
                        "subordinate_to": row['subordinate_to'].strip(),
                    })

                icon_removed_hq = "%s-%s" % (row['icon'][0:10], row['icon'][11:])
                icons.append(icon_removed_hq)

            # Deside if subtype is "headquarters" or "units"
            if new_df.iloc[0]['icon'][10].lower() == 'a':
                subtype = 'headquarters'
            else:
                subtype = 'units'

            data['features'].append({
                "type": "Feature",
                "id": counter + 1,
                "properties": {
                    "date": new_df.iloc[0]['date'].strftime('%Y-%m-%d'),
                    "type": ("single" if len(new_df) == 1 else "stacked"),
                    "icon": {
                        "type": subtype,
                        "icons": icons
                    },
                    "units": units
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(new_df.iloc[0]['lng']), float(new_df.iloc[0]['lat'])]
                }
            })

            counter += 1
        except Exception as e:
            print("🥵 Something wroing in row %s in Sheet troops" % (i + 1))
            print(list(row))
            print("ℹ️ Errormessage: %s" % e)
            pass
            break
            
    # Export website
    json.dump(data, open(CONSTS['export_folder_website'] / Path('./units.json'), 'w', encoding='UTF-8'), ensure_ascii=False)