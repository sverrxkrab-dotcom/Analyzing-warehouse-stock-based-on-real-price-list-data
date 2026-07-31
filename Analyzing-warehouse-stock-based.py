import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('price_csv.csv', sep=';', encoding='cp1251')
print(f"   Строки : {len(df)}")
print(f"   Колонки: {list(df.columns)}")

# Clean price data (ignore errors)
df['price_rub'] = pd.to_numeric(
    df['price_rub'].astype(str).str.replace(' ', '').str.replace(',', '.'),
    errors='coerce'
).fillna(0)

df['stock_value'] = pd.to_numeric(
    df['stock_value'].astype(str).str.replace(' ', '').str.replace(',', '.'),
    errors='coerce'
).fillna(0)

# Add new column: price category
df['price_category'] = df['price_rub'].apply(
    lambda x: 'Cheap' if x < 100 else
              'Budget' if x < 500 else
              'Mid' if x < 1000 else
              'Premium' if x < 5000 else
              'Luxury'
)
print(f"Total items: {len(df):,}")
print(f"Total value: {df['stock_value'].sum():,.2f} RUB")
print(f"Items with price = 0: {len(df[df['price_rub'] == 0]):,}")
print("\nPrice categories:")
print(df['price_category'].value_counts().sort_index())

# Most expensive items (price > 0)
df_pos = df[df['price_rub'] > 0]
if len(df_pos) > 0:
    print("\nMost expensive items:")
    print(df_pos.nlargest(5, 'price_rub')[['sku', 'price_rub']].to_string(index=False))