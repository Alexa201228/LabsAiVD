"""
Лабораторная №9 - Визуализация данных.
В данной лабораторной работе представлены средства для визуализации
и анализа финансовых данных.
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from utils import load_data


def trend(x):
    if x > -0.5 and x <= 0.5:
        return 'Практически или без изменений'
    elif x > 0.5 and x <= 1.5:
        return 'Небольшой позитив'
    elif x > -1.5 and x <= -0.5:
        return 'Небольшой негатив'
    elif x > 1.5 and x <= 2.5:
        return 'Позитив'
    elif x > -2.5 and x <= -1.5:
        return 'Негатив'
    elif x > 2.5 and x <= 5:
        return 'Значительный позитив'
    elif x > -5 and x <= -2.5:
        return 'Значительный негатив'
    elif x > 5:
        return 'Максимальный позитив'
    elif x <= -5:
        return 'Максимальный негатив'


if __name__ == '__main__':
    etf = load_data()

    # Вычисляем дневную доходность
    etf_cl = etf[['FXGD_cl', 'FXRL_cl', 'FXTB_cl', 'FXUS_cl', 'FXRU_cl', 'FXCN_cl']]
    etf_cl_pct = etf_cl.pct_change() * 100
    etf_cl_pct.columns = ['FXGD_cl_pct', 'FXRL_cl_pct', 'FXTB_cl_pct', 'FXUS_cl_pct', 'FXRU_cl_pct', 'FXCN_cl_pct']
    etf_vol = etf[['FXGD_vol', 'FXRL_vol', 'FXTB_vol', 'FXUS_vol', 'FXRU_vol', 'FXCN_vol']]
    etf_new = pd.concat([etf_cl, etf_vol, etf_cl_pct], axis=1)
    etf_new = etf_new.dropna()

    for stock in etf_new.columns[12:]:
        etf_new["Trend_" + str(stock)] = np.zeros(etf_new[stock].count())
        etf_new["Trend_" + str(stock)] = etf_new[stock].apply(lambda x: trend(x))

    sns.set(style="darkgrid")

    fig, axs = plt.subplots(3, 2, figsize=(40, 37))

    axs[0, 0].pie(etf_new['Trend_FXGD_cl_pct'].value_counts(), pctdistance=1.2, autopct="%.2f%%")
    axs[0, 0].set_title('FXGD')

    axs[0, 1].pie(etf_new['Trend_FXRL_cl_pct'].value_counts(),  pctdistance=1.2, autopct="%.2f%%")
    axs[0, 1].set_title('FXRL')

    axs[1, 0].pie(etf_new['Trend_FXTB_cl_pct'].value_counts(), pctdistance=1.2, autopct="%.2f%%")
    axs[1, 0].set_title('FXTB')

    axs[1, 1].pie(etf_new['Trend_FXUS_cl_pct'].value_counts(), pctdistance=1.2, autopct="%.2f%%")
    axs[1, 1].set_title('FXUS')

    axs[2, 0].pie(etf_new['Trend_FXRU_cl_pct'].value_counts(), pctdistance=1.2, autopct="%.2f%%")
    axs[2, 0].set_title('FXRU')

    axs[2, 1].pie(etf_new['Trend_FXCN_cl_pct'].value_counts(), pctdistance=1.2,  autopct="%.2f%%")

    axs[2, 1].set_title('FXCN')
    labels = etf_new['Trend_FXCN_cl_pct'].value_counts().index
    fig.legend(labels, loc='lower left', prop={'size': 30}, bbox_transform=fig.transFigure)
    plt.show()
