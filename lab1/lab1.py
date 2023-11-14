import numpy as np
import math as mt
import matplotlib.pyplot as plt
import pandas as pd

def randoNORM (dm, dsig, iter):
    #Генерація похибки за нормальним законом зміни
    S = np.random.normal(dm, dsig, iter)
    mS = np.median(S)
    dS = np.var(S)
    scvS = mt.sqrt(dS)
    #plt.hist(S, bins=20, facecolor="green", alpha=0.5)
    #plt.show()
    return S

def randoXi (k, iter):
    # Генерація похибки за Хі-квадрат
    S = np.random.chisquare(k, iter)
    mS = np.mean(S)
    dS = np.var(S)
    scvS = mt.sqrt(dS)
    #plt.hist(S, bins=20, facecolor="red", alpha=0.5)
    #plt.show()
    return S

def randoExp (alpha, iter):
    # Генерація похибки за експоненційним законом
    S = np.random.exponential(alpha, iter)
    mS = np.mean(S)
    dS = np.var(S)
    scvS = mt.sqrt(dS)
    #plt.hist(S, bins=20, facecolor="orange", alpha=0.5)
    #plt.show()
    return S

def randoUni (a, b, iter):
    # Генерація похибки за рівномірним законом
    S = np.zeros(iter)
    for i in range(iter):
        S[i] = np.random.uniform(a,b)
    mS = np.mean(S)
    dS = np.var(S)
    scvS = mt.sqrt(dS)
    #plt.hist(S, bins=20, facecolor="pink", alpha=0.5)
    #plt.show()
    return S

def Model_sq (n):
    #Генерація тренду модельного процесу за квадратичним законом
    S0 = np.zeros(n)
    for i in range(n):
        S0[i] = (0.00000005*i*i)
    return S0

def Model_linear (n):
    #Генерація тренду модельного процесу за лінійним законом
    S0 = np.zeros(n)
    for i in range(n):
        S0[i] = 0.0005*i + 2
    return S0

def Model_NORM (SN, S0N, n):
    #Поєднання згенерованого тренду зі згенерованими похибками
    SV=np.zeros(n)
    for i in range(n):
        SV[i] = S0N[i] + SN[i]
    return SV

def Plot_All(S0_L, SV_L, Text):
    #Зображення на графіку згенерованого процесу та тренду
    plt.clf()
    plt.plot(SV_L)
    plt.plot(S0_L)
    plt.ylabel(Text)
    plt.show()
    return

def parse_file(url, file_name, data_name):
    #Парсинг ексель файлу і створення вибірки із вказаного стовпчика
    d = pd.read_excel(file_name)
    for name, values in d[[data_name]].items():
        print(values)
    S_real = np.zeros(len(values))
    for i in range(len(values)):
        S_real[i] = values[i]
    return S_real

def find_stat_values (SL, Text):
    #Знаходження та відображення статистичних характеристик
    mS = np.median(SL)
    dS = np.var(SL)
    scvS = mt.sqrt(dS)
    print('------------', Text, '-------------')
    print('матиматичне сподівання: ', mS)
    print('дисперсія: ', dS)
    print('СКВ: ', scvS)
    print('-----------------------------------------------------')
    return


if __name__ == '__main__':

    n = 10000
    iter = int(n)
    dm = 0
    dsig = 5
    k = 5
    alpha = 1

    S0 = Model_sq(n)
    S0_lin = Model_linear(n)

    S = randoNORM(dm, dsig, iter)

    SV = Model_NORM(S, S0, n)
    Plot_All(S0, SV, "Квадратичний тренд + нормальний шум")
    SV_lin = Model_NORM(S, S0_lin, n)
    Plot_All(S0_lin, SV_lin, "Лінійний тренд + нормальний шум")

    S_xi = randoXi(k, iter)
    SV_1 = Model_NORM(S_xi, S0, n)
    Plot_All(S0, SV_1, "Квадратичний тренд + хі2 шум")
    SV_1_lin = Model_NORM(S_xi, S0_lin, n)
    Plot_All(S0_lin, SV_1_lin, "Лінійний тренд + хі2 шум")

    S_exp = randoExp(alpha, iter)
    SV_2 = Model_NORM(S_exp, S0, n)
    Plot_All(S0, SV_2, "Квадратичний тренд + експоненційний шум")
    SV_2_lin = Model_NORM(S_exp, S0_lin, n)
    Plot_All(S0_lin, SV_2_lin, "Лінійний тренд + експоненційний шум")

    S_uni = randoUni(-5, 2, iter)
    SV_3 = Model_NORM(S_uni, S0, n)
    Plot_All(S0, SV_3, "Квадратичний тренд + рівномірна похибка")
    SV_3_lin = Model_NORM(S_uni, S0_lin, n)
    Plot_All(S0_lin, SV_3_lin, "Лінійний тренд + рівномірна похибка")

    S_real = parse_file("", "Oschadbank_1.xlsx", "Продаж")
    Plot_All(S_real, S_real, "Курс USD в 2023 році")
    find_stat_values(S_real, "Коливання курсу")
