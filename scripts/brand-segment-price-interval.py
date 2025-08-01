import pandas as pd

# 1. Загрузка исходных данных
df = pd.read_excel('table-cheese-OK-brands.xlsx', header=5)

# 2. Конвертация и очистка
df['MaxPrice'] = pd.to_numeric(df['Максимальная продажная цена'], errors='coerce')
df = df.dropna(subset=['MaxPrice'])

# 3. Агрегация по бренду: средняя максимальная цена
brand_max = (
    df
    .groupby('Бренд', as_index=False)['MaxPrice']
    .mean()
    .rename(columns={'MaxPrice': 'AvgMaxPricePerBrand'})
)

# 4. Бизнес‑пороги и метки
bins = [0, 300, 1000, 2000, float('inf')]
labels = ['Низкий', 'Средний', 'Высокий', 'Премиальный']

# 5. Присвоение сегмента
brand_max['Segment'] = pd.cut(
    brand_max['AvgMaxPricePerBrand'],
    bins=bins,
    labels=labels,
    right=False
)

# 6. Сохранение результата
brand_max.to_excel('brand-segment-OK.xlsx', index=False)

# 7. Вывод для проверки
print(brand_max.head(20))
