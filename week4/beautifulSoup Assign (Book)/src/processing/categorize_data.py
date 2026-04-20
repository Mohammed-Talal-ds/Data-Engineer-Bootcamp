import pandas as pd

df = pd.read_csv('../../data/cleaned_data.csv')

df_1 = df[df.rating == 1]
df_2 = df[df.rating == 2]
df_3 = df[df.rating == 3]
df_4 = df[df.rating == 4]
df_5 = df[df.rating == 5]

print(df.head())

df_1.to_csv('../../data/categorized_data/data_category1.csv')
df_2.to_csv('../../data/categorized_data/data_category2.csv')
df_3.to_csv('../../data/categorized_data/data_category3.csv')
df_4.to_csv('../../data/categorized_data/data_category4.csv')
df_5.to_csv('../../data/categorized_data/data_category5.csv')