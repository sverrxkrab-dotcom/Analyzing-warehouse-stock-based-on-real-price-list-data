import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

df = pd.read_csv('price_csv.csv', sep=';', encoding='cp1251')
print(f"   Rows : {len(df)}")
print(f"   Columns: {list(df.columns)}")

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

# Categories by share of total cost
category_value = df.groupby('price_category')['stock_value'].sum().sort_values(ascending=False)
category_value_pct = (category_value / category_value.sum() * 100).round(2)

value_by_category = pd.DataFrame({
    'Total Value (RUB)': category_value,
    'Share (%)': category_value_pct
})
print(value_by_category)


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

# Average price and value by category
stats_by_category = df[df['price_rub'] > 0].groupby('price_category').agg({
    'price_rub': ['count', 'mean', 'median', 'std'],
    'stock_value': ['sum', 'mean']
}).round(2)

print("\nStatistics by category:")
print(stats_by_category)

# Top 3 categories by value share
top_3_categories = value_by_category.nlargest(3, 'Share (%)')
print("\nTop 3 categories by value share:")
print(top_3_categories)

# Pareto analysis (80/20 rule)
df_sorted = df_pos.sort_values('stock_value', ascending=False)
df_sorted['cumulative_percent'] = df_sorted['stock_value'].cumsum() / df_sorted['stock_value'].sum() * 100
items_80_percent = len(df_sorted[df_sorted['cumulative_percent'] <= 80])
print(f"\nPareto Analysis (80/20 rule):")
print(f"Items making up 80% of warehouse value: {items_80_percent:,} out of {len(df_pos):,} ({items_80_percent/len(df_pos)*100:.1f}%)")