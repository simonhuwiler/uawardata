# Export data

from pathlib import Path
import os
from decouple import config
import shutil
import argparse

import export_units
import export_btgs
import export_assessments

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


parser = argparse.ArgumentParser()
parser.add_argument('-p', type=str, required=True, help='"staging" or "production"')
args = parser.parse_args()
print("Update %s" % args.p)

production = True if  args.p.lower() == 'production' else False

export_folder = Path('./data/')
export_folder_website = Path('./website_tmp')

CONSTS = {
    "SHEET_UNITS_POSITION": SHEET_UNITS_POSITION,
    "SHEET_UNITS_DESCRIPTION": SHEET_UNITS_DESCRIPTION,
    "SHEET_ASSESSMENTS": SHEET_ASSESSMENTS,
    "SHEET_BTG": SHEET_BTG,
    "export_folder": export_folder,
    "export_folder_website": export_folder_website
}

# Create TMP Folder
if export_folder_website.exists():
    shutil.rmtree(export_folder_website)

os.mkdir(export_folder_website, )

# ----- Download Units
if production:
    export_units.export_repo(CONSTS)

export_units.export_website(CONSTS)

# ----- Download BTGs
export_btgs.export(CONSTS, production)

# ----- Download Assessments
export_assessments.export(CONSTS)
