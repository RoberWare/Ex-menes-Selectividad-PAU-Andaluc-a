# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 00:06:50 2018

@author: roberto
"""

url = "https://www.juntadeandalucia.es/economiayconocimiento/sguit/g_b_examenes_anteriores.php"
#fof = pd.read_html(fof_url)[0]
#fof.to_csv("fof.csv", header = False, index = False, encoding = "utf8")

import bs4 as bs
import pandas as pd
import numpy as np
import os

import urllib2

response = urllib2.urlopen(url)
webContent = response.read()

print webContent

with open(os.path.join("wp.html"), "w") as file0:
    toFile = webContent
    file0.write(toFile)

with open("wp.html","r") as f:
    soup = bs.BeautifulSoup(f, 'lxml')
    parsed_table = soup.find_all('table')[0] 
    data = [[td.a['href'] if td.find('a') else 
             ''.join(td.stripped_strings)
             for td in row.find_all('td')]
            for row in parsed_table.find_all('tr')]
    df = pd.DataFrame(data[1:], columns=data[0])
    print(df)  