# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF
import os

def divide_text(text,maxletters=11):
    text_divided=[]
    for x in text.split():
        if len(x)>maxletters:
            newx=""
            targ=0
            for y in x:
                if targ >= maxletters-1:
                    text_divided.append(newx)
                    newx=""
                    targ=0
                targ+=1
    return text_divided
                
                

def image(text,logo=u"./imgs/logo.png",font='./fonts/NotoSansCJK-Regular.ttc',out="./tmp/cover.png"):
    basewidth=75
     
    img = Image.open(logo, 'r')
    
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    
    img=img.resize((basewidth,hsize), Image.ANTIALIAS)
     
    
    
    img_w, img_h = img.size
    background = Image.new('RGB', (595,842), color = (255, 255, 255))
    bg_w, bg_h = background.size
    offset = ((bg_w - img_w) / 2, (bg_h - img_h) / 2)
    
    
    background.paste(img, (100,70))
    
    myfont = ImageFont.truetype(font, 50)
    d = ImageDraw.Draw(background)
    
    ntext=""
    for x in divide_text(text):
        ntext+=x+"\n"
    d.multiline_text((190,70), text, font=myfont, fill=(0, 0, 0))
    background.save(out)

def make_page(img="./tmp/cover.png"):
    cover = Image.open(img)
    width, height = cover.size

    pdf = FPDF(unit = "pt", format = [width, height])

    pdf.add_page()
    pdf.image(img, 0, 0)

    pdf.output("./tmp/AAA_000_out.pdf","F")
    os.remove(img)

def from_scratch(text,logo=u"./imgs/logo.png",font="./fonts/NotoSansCJK-Regular.ttc"):
    image(text,logo,font,out="./tmp/cover.png")
    make_page("./tmp/cover.png")

#from_scratch("wat")