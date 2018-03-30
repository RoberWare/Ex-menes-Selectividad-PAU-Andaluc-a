#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zipfile,os
import pdf_tools 

dev = 0

def force_to_unicode(text):
    "If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else text.decode('utf8')

def try_to_rename(myfile,to_file,all_pdfs):
    if os.path.exists(myfile):
        os.rename(myfile,to_file)
        all_pdfs.append(to_file)
    else: 
        print "Error","["+myfile+"]",os.path.exists(myfile)
    return all_pdfs

def merge(zips,path,criterios):
    remove=1
    all_pdfs=[]
    print criterios
    zips=sorted(zips)
    all_pdfs=[]
    nfname=[]
    for myzip in zips:
        zipname, file_extension = os.path.splitext(os.path.basename(myzip))
        print myzip
        myfile=zipfile.ZipFile(myzip)
        
        myfile.extractall("./tmp")
        
        file_names = myfile.namelist()
        y=0
        for x in file_names:
            filename, file_extension = os.path.splitext(x)
            folder = ""
            newname=path+folder+str(zipname)[:-1]+"_"+os.path.basename(filename)+str(y)+file_extension
            for letter in x:
                if letter != "/":folder+=letter
                else:break
            if file_extension == ".pdf":
                if criterios == 1:
                    all_pdfs=try_to_rename((path+x),newname,all_pdfs)
                    print "ADDED",x,x.upper().find("CRITER")
                    y+=1
                elif criterios > 1:
                    if x.upper().find("CRITER") == -1 and x.upper().find("-CR") == -1 and x.find(str(criterios)) != -1:
                        print "CRITERIO",x,(x.find("criterio"), x.find("-cr."))   
                    else:     
                        all_pdfs=try_to_rename((path+x),newname,all_pdfs)
                        print "ADDED",x,x.upper().find("CRITER")
                        y+=1
                    
                elif criterios == -1:
                    if (x.upper().find("CRITER") == -1) and (x.upper().find("-CR") == -1):
                        all_pdfs=try_to_rename((path+x),newname,all_pdfs)
                        print "ADDED",x,x.upper().find("CRITER")
                        y+=1
                    else: print "CRITERIO",x,(x.find("criterio"), x.find("-cr."))
            else:print "error",x
            
    return all_pdfs

if dev ==1:
    zips=[u'../tmp/sel_2015_fisica.zip', u'../tmp/sel_2016_fisica.zip', u'../tmp/sel_2017_fisica.zip']
    merge(zips,0)
    
#pdf_tools.pdf_cat(pdf_tools.find_files("../tmp/","pdf"),"test.pdf")



#pdf_tools.merge(["A.pdf","B.pdf","C.pdf"],"1.pdf")
"""
path="/home/roberto/Programación/Python/PROJECTS/BUFFERPDF/tmp/test/"


for myzip in zip_files:
    myfile=zipfile.ZipFile(path+myzip)
    
    file_names = myfile.namelist()
    nfname=[]
    for x in file_names:
        nfname.append(path+x)
        
    myfile.extractall(path)

    print pdf_tools.merge(nfname,path+"new.pdf")

"""