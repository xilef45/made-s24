from io import BytesIO

import requests
import pandas as pd
import sqlite3

urls = [
    "https://dev-rad-carbon-pricing.pantheonsite.io/sites/default/files/data-latest.xlsx",
    "https://edgar.jrc.ec.europa.eu/booklet/EDGARv8.0_FT2022_GHG_booklet_2023.xlsx"
]

excelSheets = [pd.ExcelFile(BytesIO(requests.get(url).content)) for url in urls]
pd.set_option('future.no_silent_downcasting', True)
# remove the first line because of the last change data in A1
sheet_carbonPrice = pd.read_excel(excelSheets[0], excelSheets[0].sheet_names[3], skiprows=1)
sheet_carbonPrice.dropna(subset=['Name of the initiative'], inplace=True)
# remove - from cells (no data)
sheet_carbonPrice.replace(to_replace='-', value=0, inplace=True)
for year in sheet_carbonPrice.columns[8:]:
    sheet_carbonPrice[year] = pd.to_numeric(sheet_carbonPrice[year], errors='coerce')
sheet_carbonPrice.convert_dtypes()

sheet_emissions = excelSheets[1].parse(excelSheets[1].sheet_names[2])
sheet_emissions.dropna(subset=['EDGAR Country Code'], inplace=True)
sheet_emissions.convert_dtypes()

conn = sqlite3.connect('../data/data.sqlite')

sheet_carbonPrice.to_sql('carbonPrice', conn, if_exists='replace', index=False)
sheet_emissions.to_sql('emissions', conn, if_exists='replace', index=False)

conn.close()