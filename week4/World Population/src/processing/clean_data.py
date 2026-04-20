import pandas as pd


df = pd.read_csv('data/raw_data.csv')


df['Population 2026'] = df['Population 2026'].str.replace(",","")
df['Population 2026'] = df['Population 2026'].str.strip()
df['Population 2026'] = df['Population 2026'].astype(int)

df['Yearly Change'] = df['Yearly Change'].str.replace('%','')
df['Yearly Change'] = df['Yearly Change'].str.replace('â','-')
df['Yearly Change'] = df['Yearly Change'].astype(float)

df['Net Change'] = df['Net Change'].str.replace(',','')
df['Net Change'] = df['Net Change'].str.replace('â','-')
df['Net Change'] = df['Net Change'].astype(int)

df['Density (P/KmÂ²)'] = df['Density (P/KmÂ²)'].str.replace(',','')
df['Density (P/KmÂ²)'] = df['Density (P/KmÂ²)'].astype(float)

df['Land Area (KmÂ²)'] = df['Land Area (KmÂ²)'].str.replace(',','')
df['Land Area (KmÂ²)'] = df['Land Area (KmÂ²)'].astype(float)

df['Migrants (net)'] = df['Migrants (net)'].str.replace(',','')
df['Migrants (net)'] = df['Migrants (net)'].str.replace('â','-')
df['Migrants (net)'] = df['Migrants (net)'].astype(int)

df['Fert. Rate'] = df['Fert. Rate'].astype(float)

df['Median Age'] = df['Median Age'].astype(float)

df['Urban Pop %'] = df['Urban Pop %'].str.replace('%','')
df['Urban Pop %'] = df['Urban Pop %'].str.replace('â','-')
df['Urban Pop %']= pd.to_numeric(df['Urban Pop %'],errors='coerce')

df['World Share'] = df['World Share'].str.replace('%', '')
df['World Share'] = df['World Share'].astype(float)

print(df.info())

df.to_csv('data/cleaned_data.csv')