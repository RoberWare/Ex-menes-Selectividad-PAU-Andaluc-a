# -*- coding: utf-8 -*-

import os
import re
#import pandas as pd    
from bs4 import BeautifulSoup 
from requests import get
import json

def convert_to_excel(all_subjects,output,excel_format):
    df = pd.DataFrame.from_dict(all_subjects, orient='index')
    df.transpose()
    if excel_format=="csv":
        df.to_csv(output+'file.csv', sep='\t', encoding='utf-8')
    else:
        df.to_excel(output+'file.xls')

def convert_to_json(all_subjects,output):
    new_subjects={}
    for subject in all_subjects:
        if re.search('[a-zA-Z]+',subject) != None:
            new_subjects[subject]=all_subjects[subject]
    with open(output+'.json', 'w') as outfile:
        json.dump(new_subjects, outfile)

def table(url = 'https://www.juntadeandalucia.es/economiayconocimiento/sguit/g_b_examenes_anteriores.php',outputs=["./data/subjects","./data/orientations"],convert_to="json",dev=True,excel_format="csv"):
    response = get(url)
    #print(response.text[:500])
    
    html_soup = BeautifulSoup(response.text, 'html.parser')
    type(html_soup)
    
    subjects_containers = html_soup.find_all('tr')
    if dev:print(type(subjects_containers))
    if dev:print(len(subjects_containers))
    
    all_subjects={}
    all_subjects_orientation={}    
    
    for subject in subjects_containers:
        #try:
        if subject.td is not None and subject != "\n":
            subject_name=subject.td.text
            
            #print subject_name
            if type(subject_name) != unicode: subject.td.text.decode("utf-8")
                
            all_subjects[subject_name]=[]
            all_subjects_orientation[subject_name]=""

            for exams in subject.find_all("a",href=True):
                #print exams['href']
                if "ORIENT" in str(exams['href']).upper():all_subjects_orientation[subject_name]=(exams['href'])
                else: all_subjects[subject_name].append(exams['href'])
                    
                    
        #except Exception as s:
        #    if dev:print "no",s
    
    if dev:print all_subjects

    if convert_to == "excel":
        convert_to_excel(all_subjects,outputs[0],excel_format)
        convert_to_excel(all_subjects_orientation,outputs[1],excel_format)
    if convert_to == "json":
        convert_to_json(all_subjects_orientation,outputs[1])
        convert_to_json(all_subjects,outputs[0])

#table()