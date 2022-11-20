"""
Модуль вспомогательных методов, используемых в лабораторных работах
"""
import os
from typing import List

import pandas as pd


def prepare_data_from_csv(filename: str) -> pd.DataFrame:
    df = pd.read_csv(filename)
    df['date'] = pd.to_datetime(df['<DATE>'].astype(str), dayfirst=True)
    name = os.path.basename(filename)[:4]
    df = df.drop(['<DATE>', '<TIME>', '<OPEN>', '<HIGH>', '<LOW>'], axis=1)
    df = df.set_index(['date'])
    df.columns = [name + '_cl', name + '_vol']
    return df


def find_datasets() -> List[str]:
    res = []
    for root, dirs, files in os.walk("./../"):
        for file in files:
            if file.startswith('FX') and file.endswith(".csv"):
                res.append(os.path.join(root, file))
    return res


def load_data() -> pd.DataFrame:
    # Находим файлы с данными в корневой папке
    datasets = find_datasets()
    # Подготовка данных.
    # Нам необходимы только дата, значение при закрытии торгов (CLOSE) и объём продаж (VOL)
    preprocessed_dfs = [prepare_data_from_csv(filename) for filename in datasets]
    preprocessed_dfs = [df.loc[~df.index.duplicated(keep='first')] for df in preprocessed_dfs]
    # Объединяем полученные данные в единый датасет
    etf = pd.concat(preprocessed_dfs, axis=1)
    # Убираем нулевые значения для оптимизации расчетов
    etf.dropna(inplace=True, axis=0)
    return etf
