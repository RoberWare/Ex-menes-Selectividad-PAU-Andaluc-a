#!/usr/bin/env python
# -*- coding: utf-8 -*-

#KIVY IMPORTS
import kivy
#kivy.config.Config.set('graphics','resizable', False)

from kivy.core.window import Window
from kivy.metrics import dp

Window.size=(dp(590),dp((480)))
Window.minimum_width=(dp(580))
Window.minimum_height=dp(480)

from kivy.app import App

from kivy.uix.button import Button
from kivy.uix.spinner import Spinner

from kivy.uix.popup import Popup
from kivy.uix.video import Video

from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from  kivy.uix.widget import Widget

from kivy.properties import ListProperty, OptionProperty, BooleanProperty, DictProperty, ObjectProperty, StringProperty, NumericProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout

from kivy.utils import platform

from kivy.clock import Clock
from functools import partial

from kivy.config import Config
Config.set("input", "mouse", "mouse, disable_multitouch")

#SYSTEM IMPORTS
import os
import json,re,shutil

from scripts import scrap_html,download,pdf_tools,zip_tools,zips_to_pdf

if platform == 'android':
    from plyer import email

#GLOBAL VARS
url='https://www.juntadeandalucia.es/economiayconocimiento/sguit/g_b_examenes_anteriores.php'
workpath=os.path.abspath("./tmp")+"/"
progressbar="blue-barber-bar"

class NoneUI(Screen):
    pass

class MainPanel(BoxLayout):
    pass

class PicChooser(Popup):
    pass

class MyButton(Button):
    myimg=StringProperty()
    mylbl=StringProperty()
    pass

class PopFAQ(Popup):
    pass

class PopSETTINGS(Popup):
    pass

class PopINFO(AnchorLayout):
    pass

class PopMsg(AnchorLayout):
    pass

class PopMsgERRORFILL(AnchorLayout):
    pass

class PopMsgWARN(Popup):
    pass

class PopMsgEND(Popup):
    pass

class PopMsgUPD(AnchorLayout):
    pass

class PopMsgUPDCOMPLETED(Popup):
    pass

class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)

    def build(self):
        #Window.borderless = True
        #Window.left=0
        #Window.top=0
        # WINDOW SETTINGS
        self.title = u"PAU PDF MERGER"
        self.window_icon = "./imgs/logo.png"
        
        Window.bind(on_resize=self.wd_resize)
        Config.set("graphics","resizable",0)
        #Window.size=(dp(885)),dp(370)

        #self.icon = "./imgs/logo.png"
        self.url=url        
        self.criterios=1
        self.orientation_name=""
        self.years=[]
        # SCREENS
        self.myMainPanel = MainPanel()
        
        root = self.myMainPanel        
        
        self.myNoneUI = self.myMainPanel.ids.myNoneUI

        self.myPicChooser = PicChooser()
        self.myPicChooser.ids.pc.path=os.path.expanduser("~")
        
        self.myPopSETTINGS = PopSETTINGS()
        self.myPopFAQ = PopFAQ()
        self.myPopINFO = Popup(title='Información',content=PopINFO(),size_hint=(.8,.5))
        self.myPopMsg = Popup(title='Lo sentimos...',content=PopMsg(),size_hint=(.8,.5))
        self.myPopMsgERRORFILL = Popup(title='ERROR',content=PopMsgERRORFILL(),size_hint=(.8, .5))
        self.myPopMsgWARN = PopMsgWARN()
        self.myPopMsgUPD = Popup(title='Actualizando',content=PopMsgUPD(),size_hint=(.8,.5))
        self.myPopMsgUPDC =PopMsgUPDCOMPLETED()
        self.myPopMsgEND = PopMsgEND()
        
        self.myNoneUI.ids.pbar.source = "./imgs/animations/progress-bar/%s/%s-stop.png"%(progressbar,progressbar)
        
        
        return root

    def on_start(self):
        tmp= self.is_extension(os.listdir("./tmp"),".zip")
        
        print tmp
        
        if tmp != []:
            self.myPopMsg.open()     

        #scrap_html.table(url=url)
        try:
            with open('./data/subjects.json') as json_data:
                self.all_subjects = json.load(json_data)
                
            with open('./data/orientations.json') as json_data:
                self.all_subjects_orientations = json.load(json_data)                
                
            with open('./data/settings.json') as json_data:
                self.settings = json.load(json_data)
        except:pass
            
        self.myNoneUI.ids.subjects.values=self.all_subjects
        
        self.myPopSETTINGS.ids.path.text = self.settings["default_folder"]
        self.myPopSETTINGS.ids.img.text = self.settings["img_pau"]
        self.myPopSETTINGS.ids.font.text = self.settings["font"]
        self.myPopSETTINGS.ids.url.text = self.settings["url"]
        
        self.myNoneUI.ids.path.text = self.settings["default_folder"]
        
        
        
        self.main()

    def show_side_panel(self):
        self.myMetaPanel.ids.NavDraw.toggle_state()

    def wd_resize(self,window,x,y):
        print Window.size
        #Window.size=(dp(885), dp(315))

    ##SCREENS

    def vpui(self):
        self.myMainPanel.ids.ScrMan.current = self.myVideoPadUI.name

    ###UPDATE FUNCTIONS
    def spinner_subjects_update(self):
        if self.myNoneUI.ids.subjects.text in self.all_subjects:
            years=[]
            for x in self.all_subjects[self.myNoneUI.ids.subjects.text]:
                 n= re.sub("\D", "", x)
                 if re.search('[0-9]+',n)!=None:
                     years.append(n)
                     print n
            self.myNoneUI.ids.since.values=years
            self.myNoneUI.ids.since.text=min(years)
            self.myNoneUI.ids.to.values=years
            self.myNoneUI.ids.to.text=max(years)


    ###MAIN FUNCTIONS
    def is_extension(self,file_names,extension):
        files=[]
        for x in file_names:
            filename, file_extension = os.path.splitext(x)
            if file_extension == extension:
                files.append(x)
        return files

    def delete_all(self):
        shutil.rmtree('./tmp')
        os.mkdir("./tmp")
        self.myPopMsg.dismiss()

    def continue_zipping(self):
        pass
        """
        nl=list_plus_str(string1=workpath,list_names=tmp)
        print nl
        zips_to_pdf.merge_all(nl,workpath)                 
        """

    def ignore(self):
        self.myPopMsg.dismiss()
    
    def ignoreERRORFILL(self):
        self.myPopMsgERRORFILL.dismiss()
        
    def ignoreEND(self):
        self.myPopMsgEND.dismiss()

    def ignoreINFO(self):
        self.myPopINFO.dismiss()
        
    def ignoreFAQ(self,arg):
        self.myPopFAQ.dismiss()
        if arg:
            print pdf_tools.word_counter("/home/roberto/Programación/Python/PROJECTS/BUFFERPDF/PC/beta_0.2/output/sel_2011_matematicas_sel_2012_matematicas_sel_2013_matematicas_sel_2014_matematicas_sel_2015_matematicas_sel_2016_matematicas_sel_2017_matematicas_.pdf")
        
    def ignoreSETTINGS(self,save):
        self.myPopSETTINGS.dismiss()
        if save:
            self.settings={}
            self.settings["img_pau"]=self.myPopSETTINGS.ids.img.text
            self.settings["font"]=self.myPopSETTINGS.ids.font.text
            self.settings["default_folder"]=self.myPopSETTINGS.ids.path.text
            self.settings["url"]=self.myPopSETTINGS.ids.url.text

            with open('./data/settings.json', 'w') as outfile:
                json.dump(self.settings, outfile)

    def ignorePicChooser(self,upd):
        self.myPicChooser.dismiss()
        if upd:
            self.myNoneUI.ids.path.text=self.myPicChooser.ids.pc.path
            self.myPopSETTINGS.ids.path.text=self.myPicChooser.ids.pc.path
            print self.myPopSETTINGS.ids.path.text

    def name_from_url(self,link):
        n=0
        for x in link[::-1]:
            if x == "/":break
            else:n+=1
        print link[-n:]
        file_name = "./tmp/"+link[-n:]
        return file_name
        
    def wait_until_download(self,myurl,*largs):
        #self.myNoneUI.ids.prompt.text = download.progress
        if download.download_finished:
            print "FINISHED"
            download.download_finished=False
            self.myNoneUI.ids.pbar.value+=1
            #name=self.name_from_url(myurl)
            name=download.file_name
            print "SE acaba de descargar",download.file_name
            if os.path.splitext(name)[1] == ".zip":
                self.zip_names.append(name)
            else:
                self.orientation_name=name
                print "Orientaciones>>>>>>>",name
            if len(self.zip_names)>=len(self.pdf_urls):
                self.THREADdownload.cancel()
                self.THREADwaitfordownload.cancel()
                self.merge_zips(self.zip_names)
                self.disabled_all_widgets(self.myNoneUI.ids.core.children,False)
                self.delete_all()
                self.myPopMsgEND.ids.name.text = self.myNoneUI.ids.subjects.text
                self.myPopMsgEND.ids.date.text = str(str(self.years[0])+"-"+str(self.years[1]))
                self.myPopMsgEND.ids.docname.text = self.myNoneUI.ids.path.text
                self.myPopMsgEND.open()
                self.myNoneUI.ids.prompt.text="¡Trabajo completado!"
                self.myNoneUI.ids.pbar.source = "./imgs/animations/progress-bar/%s/%s-stop.png"%(progressbar,progressbar)
            return False

    def merge_zips(self,zip_names):
        print zip_names
        zips_to_pdf.merge_all(zip_names,workpath,self.myNoneUI.ids.create_cover.active,self.myNoneUI.ids.subjects.text,self.criterios,self.orientation_name,self.myNoneUI.ids.path.text,str((self.myNoneUI.ids.subjects.text).encode("utf-8")+"_"+str(self.years[0])+"-"+str(self.years[1])))  
        print "-cr.",self.criterios        
        
    def disabled_all_widgets(self,name,value):
        for x in name:
            x.disabled=value
        
    def proceed(self):        
        if self.myNoneUI.ids.subjects.text != "Materia" and self.myNoneUI.ids.since.text != "Desde" and self.myNoneUI.ids.to.text != "Hasta" and self.myNoneUI.ids.path.text != "...":
            self.all_years=pdf_tools.n_to_m(int(self.myNoneUI.ids.since.text),int(self.myNoneUI.ids.to.text))
            for y in self.years:
                self.years.remove(y)   
            self.years.append(min(self.all_years))
            self.years.append(max(self.all_years))
            print self.years
            
            if self.settings["show_warn"]=="normal": self.myPopMsgWARN.open()
            else: self.process()
            
        else:
            self.myPopMsgERRORFILL.open()
        
    def update_table_links(self):
        self.myPopMsgUPD.open()
        scrap_html.table(url=url)
        self.myPopMsgUPD.dismiss()
        self.myPopMsgUPDC.open()
        
    def process(self):
        print self.myNoneUI.ids.subjects.text,self.myNoneUI.ids.since.text,self.myNoneUI.ids.to.text,self.myNoneUI.ids.path.text
        self.myPopMsgWARN.dismiss()
        
        print self.myPopMsgWARN.ids.show_again.state
        self.settings["show_warn"]=self.myPopMsgWARN.ids.show_again.state

        with open('./data/settings.json', 'w') as outfile:
            json.dump(self.settings, outfile)
        
        self.myNoneUI.ids.pbar.source = "./imgs/animations/progress-bar/%s/%s.zip"%(progressbar,progressbar)
        self.myNoneUI.ids.pbar.anim_delay = 0.01     
        self.disabled_all_widgets(self.myNoneUI.ids.core.children,True) 
        self.myNoneUI.ids.prompt.disabled=False
        
        if self.myNoneUI.ids.orientations.state=="down":
            self.orientations=1    
            self.orientation_name=self.name_from_url(self.all_subjects_orientations[self.myNoneUI.ids.subjects.text])
        
        if self.myNoneUI.ids.allyears.state=="down":self.criterios=1
        elif self.myNoneUI.ids.lastyear.state=="down":self.criterios=self.years[1]
        else: self.criterios=-1
        
        self.pdf_urls=[]
        if self.orientations: self.THREADdownload=Clock.schedule_interval(partial(download.progress_bar,self.all_subjects_orientations[self.myNoneUI.ids.subjects.text]), 0.5)
        for x in self.all_subjects[self.myNoneUI.ids.subjects.text]:
            for y in self.all_years:
                if x.find(str(y)) != -1:
                    self.pdf_urls.append(x)
        
        #print pdf_urls
        self.myNoneUI.ids.pbar.max=len(self.pdf_urls)
        self.myNoneUI.ids.pbar.value=0
        self.myNoneUI.ids.prompt.text="Su tarea se está procesando. Porfavor, sea paciente...."
        #chunks=len(pdf_urls)
        self.zip_names=[]
        
        
        for x in self.pdf_urls:
            #download.download_finished=False
            #download.progress_bar(x)
            self.THREADdownload=Clock.schedule_interval(partial(download.progress_bar,x), 0.5)
            #Clock.schedule_once(partial(download.progress_bar,x), 0.5)
            self.THREADwaitfordownload=Clock.schedule_interval(partial(self.wait_until_download,x), 0.5)

    def prompt(self,text):
        self.myNoneUI.ids.prompt.text=text
        
    def main(self):
        print ""

if __name__ == '__main__':
    MainApp().run()
