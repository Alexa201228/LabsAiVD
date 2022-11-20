"""
Лабораторная работа №4 - Статистическая обработка данных.
Данная лабораторная работа содержит код для определения дневной доходности и
построения гистограмм, а также для анализа тренда.
"""

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

from utils import load_data

if __name__ == '__main__':

    etf = load_data()

    # Вычисляем дневную доходность
    etf_cl = etf[['FXGD_cl', 'FXRL_cl', 'FXTB_cl', 'FXUS_cl', 'FXRU_cl', 'FXCN_cl']]
    etf_cl_pct = etf_cl.pct_change() * 100
    etf_cl_pct.columns = ['FXGD_cl_pct', 'FXRL_cl_pct', 'FXTB_cl_pct', 'FXUS_cl_pct', 'FXRU_cl_pct', 'FXCN_cl_pct']
    etf_vol = etf[['FXGD_vol', 'FXRL_vol', 'FXTB_vol', 'FXUS_vol', 'FXRU_vol', 'FXCN_vol']]
    etf_new = pd.concat([etf_cl, etf_vol, etf_cl_pct], axis=1)
    etf_new = etf_new.dropna()
    print(etf_new.head())
    # Доходность в виде графика во времени
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))
    axs[0, 0].plot(etf_new.index, etf_new['FXGD_cl_pct'], 'tab:blue')
    axs[0, 0].set_title('FXGD')
    axs[0, 1].plot(etf_new.index, etf_new['FXRL_cl_pct'], 'tab:orange')
    axs[0, 1].set_title('FXRL')
    axs[1, 0].plot(etf_new.index, etf_new['FXTB_cl_pct'], 'tab:green')
    axs[1, 0].set_title('FXIT')
    axs[1, 1].plot(etf_new.index, etf_new['FXUS_cl_pct'], 'tab:red')
    axs[1, 1].set_title('FXUS')
    axs[2, 0].plot(etf_new.index, etf_new['FXRU_cl_pct'], 'tab:grey')
    axs[2, 0].set_title('FXRU')
    axs[2, 1].plot(etf_new.index, etf_new['FXCN_cl_pct'], 'tab:purple')
    axs[2, 1].set_title('FXCN')

    for ax in axs.flat:
        ax.set(xlabel='Data', ylabel='Price')

    for ax in axs.flat:
        ax.label_outer()

    plt.show()

    sns.set(style="darkgrid")

    fig, axs = plt.subplots(3, 2, figsize=(15, 15))

    sns.histplot(data=etf_new['FXGD_cl_pct'], kde=True, color="orange", ax=axs[0, 0])
    axs[0, 0].set_xlim(-10, 10)
    sns.histplot(data=etf_new['FXRL_cl_pct'], kde=True, color="olive", ax=axs[0, 1])
    axs[0, 1].set_xlim(-10, 10)
    sns.histplot(data=etf_new['FXTB_cl_pct'], kde=True, color="gold", ax=axs[1, 0])
    axs[1, 0].set_xlim(-10, 10)
    sns.histplot(data=etf_new['FXUS_cl_pct'], kde=True, color="grey", ax=axs[1, 1])
    axs[1, 1].set_xlim(-10, 10)
    sns.histplot(data=etf_new['FXRU_cl_pct'], kde=True, color="teal", ax=axs[2, 0])
    axs[2, 0].set_xlim(-10, 10)
    sns.histplot(data=etf_new['FXCN_cl_pct'], kde=True, color="brown", ax=axs[2, 1])
    axs[2, 1].set_xlim(-10, 10)

    plt.show()
