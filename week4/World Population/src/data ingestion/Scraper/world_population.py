
import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
URL = "https://www.worldometers.info/world-population/population-by-country"
content = requests.get(URL).text
soup = BeautifulSoup(content, 'html.parser')

table = soup.find('table')

table_body = table.find('tbody')
table_rows = table_body.find_all('tr')

for row in  table_rows:
    cells = row.find_all('td')
    num = cells[0].text
    country = cells[1].text
    population = cells[2].text
    y_change = cells[3].text
    net_change = cells[4].text
    Density = cells[5].text
    land_area = cells[6].text
    Migrants = cells[7].text
    fert_rate = cells[8].text
    median_age = cells[9].text
    urban_pop = cells[10].text
    world_share = cells[11].text
    data.append({
        'Country': country,
        'Population 2026': population,
        'Yearly Change': y_change,
        'Net Change': net_change,
        'Density (P/KmÂ²)': Density,
        'Land Area (KmÂ²)': land_area,
        'Migrants (net)': Migrants,
        'Fert. Rate': fert_rate,
        'Median Age': median_age,
        'Urban Pop %': urban_pop,
        'World Share': world_share
    })


df = pd.DataFrame(data)
df.to_csv('data/raw_data.csv', index=False)