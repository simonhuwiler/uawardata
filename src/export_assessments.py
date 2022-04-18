import pandas as pd
import json
from pathlib import Path

def export(CONSTS):
    df = pd.read_csv(CONSTS['SHEET_ASSESSMENTS'])
    df = df.sort_values('date')
    df['text'] = df['text'].fillna('')

    data = []
    for i, row in df.iterrows():
        data.append({
            'date': row['date'],
            # 'date_visible': row['date_visible'],
            'text': row['text']
        })

    with open(CONSTS['export_folder_website'] / Path('./assessments.json'), 'w', encoding='UTF-8') as f:
        json.dump(data, f)