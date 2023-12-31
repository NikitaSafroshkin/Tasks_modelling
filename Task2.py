import numpy
import requests
import xml.etree.ElementTree as ET
from scipy import special, constants
from numpy import arange, abs, sum
from matplotlib import pyplot as plt
import csv
import os.path

# читаем XML файл
data = requests.get('https://jenyay.net/uploads/Student/Modelling/task_02.xml').text
root = ET.fromstring(data)
for element in root.iter('variant'):
    if element.get('number') == '17':
        D = float(element.get('D'))
        f_min = float(element.get('fmin'))
        f_max = float(element.get('fmax'))

# задаем константы для рассчетов
n_end = 10
f_step = 100000
r = D / 2
f_arange = arange(f_min, f_max, f_step)
wavelength_arange = constants.c / f_arange
k_arange = 2 * constants.pi / wavelength_arange


# h
def f4(n, x):
    return special.spherical_jn(n, x) + 1j * special.spherical_yn(n, x)


# b
def f3(n, x):
    return (x * special.spherical_jn(n - 1, x) - n * special.spherical_jn(n, x)) / (x * f4(n - 1, x) - n * f4(n, x))


# a
def f2(n, x):
    return special.spherical_jn(n, x) / f4(n, x)


# ЭПР
rcs_arange = (wavelength_arange ** 2) / numpy.pi * (abs(sum([((-1) ** n) * (n+0.5) * (f3(n, k_arange * r) - f2(n, k_arange * r)) for n in range(1, n_end)], axis=0)) ** 2)


counter = 0

if os.path.exists('result') == False:
    os.mkdir('result')


with open('result/data.csv', 'w') as file:
    writer = csv.writer(file)
    for x, y, z in zip(f_arange, wavelength_arange, rcs_arange):
        counter += 1
        writer.writerow([counter, x, y, z])

# Строим график
plt.plot(f_arange, rcs_arange)
plt.xlabel("Частота, Гц")
plt.ylabel("ЭПР, м^2")
plt.show()
