# -*- coding: utf-8 -*-

import zip_tools,pdf_tools,create_frontpage

def merge_all(zips=[],workpath="",frontpage=True,cover_text=None,criterios=1,orientation_name="",output_folder="./output/",pdf_name="none"):
    all_pdfs=zip_tools.merge(zips,workpath,criterios)
    if output_folder[-1:]!="/": output_folder+="/"
    if frontpage:
        if cover_text==None:cover_text=raw_input("Subject name > ")
        create_frontpage.from_scratch(cover_text)
        all_pdfs.append("./tmp/AAA_000_out.pdf")
    if orientation_name!="":
        all_pdfs.append(str(orientation_name))
    print orientation_name
    out_pdf_name = (str(output_folder)+pdf_name+".pdf")
    pdf_tools.merge(sorted(all_pdfs),out_pdf_name)
    print "finished"
    print "Orientaciones",orientation_name