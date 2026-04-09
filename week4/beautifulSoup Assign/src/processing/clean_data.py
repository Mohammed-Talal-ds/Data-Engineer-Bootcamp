import pandas as pd


df = pd.read_csv('../../data/raw_data.csv')

# clean the price and change its type to float
df['price'] = df['price'].str.replace('Â£', '')
df['price'] = df['price'].astype(float)

# map rating to numerical values
df['rating'] = df['rating'].map({'Three': 3,
                   'One': 1,
                    'Four' : 4,
                    'Five': 5,
                    'Two': 2
                    })
df.sort_values(by=['rating'], inplace= True)

# save file to data folder
df.to_csv('../../data/cleaned_data.csv')