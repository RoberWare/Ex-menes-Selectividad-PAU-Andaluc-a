# -*- coding: utf-8 -*-

#!/usr/bin/env python

import sys,os
from os import listdir, getcwd, walk
from os.path import abspath

from PyPDF2 import PdfFileMerger,PdfFileReader
import pyPdf

def n_to_m(n,m):
    if n != m:
        nums=n,m
        mini=min(nums)
        maxi=max(nums)
        
        l=[]
        l.append(maxi)
        for x in range(maxi-mini):
            l.append(mini+x)
    else: l=[n]
    return sorted(l)

def merge(input_files, output_stream):
    pdfs_to_merge=[]
    output = pyPdf.PdfFileWriter()
    for item in input_files:
        print item
        try:
            if os.path.splitext(item)[1].upper() == ".PDF":
                pdfDocument = item
                input1 = pyPdf.PdfFileReader(file(pdfDocument, "rb"))
                pdfs_to_merge.append(pdfDocument)
                for page in range(input1.getNumPages()):
                    if input1.getPage(page).getContents() != None:
                        output.addPage(input1.getPage(page))
                    else: print page
        except Exception as e:
            print e
     
    outputStream = file(output_stream, "wb")
    output.write(outputStream)
    outputStream.close()

    return pdfs_to_merge


def find_files_x(folder,find,contain=0):
    files=[]
    for dirName, subdirList, fileList in os.walk(folder):
        for x in find:
            if dirName.find(x) != -1:
                print dirName.find(x),dirName
                #print('Directorio encontrado: %s' % dirName)
                for fname in fileList:
                    print('\t%s' % fname)
                    if contain!=0:
                        if fname[-len(contain[:-1]):]==contain[1:]:
                            files.append(dirName+"/"+fname)
                    else:
                        files.append(dirName+"/"+fname)
                break
    return files


def find_files(path,text_to_find,file_format=".pdf"):
    lstFiles = []
    lstDir = os.walk(path)   #os.walk()Lista directorios y ficheros
    print lstDir
    for root, dirs, files in lstDir:
        print root, dirs
        for fichero in files:
            (file_name, extension) = os.path.splitext(fichero)
            if(extension == file_format):
                if file_name.find(text_to_find) != -1:
                    lstFiles.append(file_name+extension)
                    print (file_name+extension)
                else: print file_name,file_name.find(text_to_find)
#find_files("../tmp/fisica","2015")
                
def get_pdf_content(pdf_file_path):
    with open(pdf_file_path) as f:
        pdf_reader = PdfFileReader(f)
        content = "\n".join(page.extractText().strip() for page in pdf_reader.pages)
        content = ' '.join(content.split())
        
    print content
    return content
                
                
def getPDFContent(path):
    content = ""
    num_pages = 10
    p = file(path, "rb")
    pdf = pyPdf.PdfFileReader(p)
    for i in range(0, num_pages):
        content += pdf.getPage(i).extractText() + "\n"
    content = " ".join(content.replace(u"\xa0", " ").strip().split())     
    print content
    return content 
    
def word_counter(filename):
    #graphlab.text_analytics.count_words(
    wordcount={}
    for word in get_pdf_content(filename).split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    for k,v in wordcount.items():
        print k, v
   
#pdf_cat(sorted(find_files(folder,year_range,file_format)), output_name)
#pdf_cat([cover_pages,output_name],output_name)