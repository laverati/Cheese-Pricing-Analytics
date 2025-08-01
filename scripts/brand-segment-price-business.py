import pandas as pd

# 1. Загрузить табличку
df = pd.read_excel('table-cheese-OK-brands.xlsx', header=5)

# 2. Привести цену к числу и убрать пустые
df['Средняя цена'] = pd.to_numeric(df['Средняя цена продажи (руб)'], errors='coerce')
df = df.dropna(subset=['Средняя цена'])

# 3. Агрегировать по бренду: вычислить у каждого бренда среднюю цену
brand_price = (
    df
    .groupby('Бренд', as_index=False)['Средняя цена']
    .mean()
    .rename(columns={'Средняя цена': 'AvgPricePerBrand'})
)

# 4. Посчитать квантильные пороги по брендам
q25, q50, q75 = brand_price['AvgPricePerBrand'].quantile([0.25, 0.5, 0.75])

# 5. Присвоить каждому бренду сегмент
def segment(p):
    if p <= q25:
        return 'Низкий'
    elif p <= q50:
        return 'Средний'
    elif p <= q75:
        return 'Высокий'
    else:
        return 'Премиальный'

brand_price['Сегмент'] = brand_price['AvgPricePerBrand'].apply(segment)

# 6. Сохраняем результат
brand_price.to_excel('Сегментация_по_брендам.xlsx', index=False)

print(brand_price.head())
print('Пороги квантилей:', q25, q50, q75)
