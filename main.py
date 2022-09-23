import os

os.environ['KIVY_VIDEO'] = 'ffpyplayer'
#os.environ['KIVY_AUDIO'] = 'sdl2'

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import Screen
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.button import MDIconButton
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivymd.utils.fitimage import FitImage
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivy.clock import Clock
from kivymd.toast import toast
#from kivymd.uix.slider import MDSlider
#from kivymd.uix.label import MDLabel
#from kivymd.uix.label import MDIcon
#from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
#from kivy_garden.mapview import MapView
from Kview import OpenView
#import threading
import cv2
from Mywidget import QRtext, QRimage, QRvideo, QRaudio, QRcount, QRmap, QRfile, QRitems
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window

global itens, name
itens = []
name = ''

global QRids
QRids = {}

global IDs
IDs = 0

class Manager(ScreenManager):
    def __init__(self,**kargs):
        super().__init__(**kargs)

    def Teste(self):
        self.current = 'login'

class Login(Screen):
    def __init__(self,**args):
        super().__init__(**args)

class Register(Screen):
    def __init__(self,**args):
        super().__init__(**args)

class Principal(Screen):
    def __init__(self,**args):
        super().__init__(**args)
        self.aberto = False

    def View(self):
        self.remove_widget(self.ids.help)
        self.camera ='''
BoxLayout:
    id:teste
    size_hint_y:None
    height:self.minimum_height
'''
        self.camera = Builder.load_string(self.camera)
        self.view = OpenView()
        self.view.size_hint_y = None
        self.view.height = self.ids.view.height
        self.camera.add_widget(self.view)
        self.ids.camera.add_widget(self.camera)
        self.aberto = True
        self.cnt = Clock.schedule_interval(self.FindQR, 0)
        self.remove_widget(self.ids.camicon)

    def on_pre_leave(self):
        try:
            self.add_widget(self.ids.camicon)
            self.add_widget(self.ids.help)
        except:
            pass

        if self.aberto == True:
            self.ids.camera.remove_widget(self.camera)
            self.view.ligar.time.cancel()
            self.cnt.cancel()
            self.aberto = False

    def FindQR(self,*args):
        try:
            self.view.ligar.data.decode('UTF-8')
            self.manager.transition.direction = 'left'
            self.manager.current = 'vizualizar'
            self.add_widget(self.ids.camicon)
            self.add_widget(self.ids.help)
        except:
            pass

class QRdados(Screen):
    def __init__(self,**args):
        super().__init__(**args)

    def Name(self):
        self.box = '''
BoxLayout:
    id:dial
    canvas:
        Color:
            rgba:1,1,1,1
        RoundedRectangle:
            pos:self.pos
            size:self.size
            radius:[10,10,10,10]
    padding:'10dp'
    size_hint_y:None
    height: '150dp'
    size_hint_x: .5
    pos_hint:{'center_x':.5, 'center_y':.5}
    orientation:'vertical'
    MDLabel:
        #size_hint_y:None
        #height:'50dp'
        #pos_hint:{'top':1}
        text:'Name:'
        bold:True
    TextInput:
        id:te
        size_hint_y:None
        height:self.minimum_height
        text_color:0,0,0,0
        #line_color_normal: 0, 0.588, 0.533,1
    BoxLayout:
        MDRaisedButton:
            text:'Voltar'
            on_release:app.root.get_screen('qrdados').Cancel()
        Widget:
        MDRaisedButton:
            text:'Ok'
            on_release:
                app.root.get_screen('qrdados').Prox(te.text)
'''
        self.box = Builder.load_string(self.box)
        self.add_widget(self.box)

    def Cancel(self):
        self.remove_widget(self.box)

    def Prox(self, nome):
        self.remove_widget(self.box)
        global name
        name = nome
        self.manager.transition.direction = 'left'
        self.manager.current = 'criardados'

class Criardados(Screen):
    def __init__(self,**args):
        super().__init__(**args)
        self.cnt = True
        self.container = '''
BoxLayout:
    canvas:
        Color:
            rgba:.10,.10,.10,1
        RoundedRectangle:
            pos:self.pos
            size:self.size
            radius:20,20,20,20
    padding:'20dp'
    width:self.minimum_height
    size_hint_y:None
    height:self.minimum_height
'''
        self.container = Builder.load_string(self.container)

    def Path(self, n1):
        self.file = QRfile()
        self.file.file_manager_open()
        self.file.file_manager.ext = self.file.file_manager.ext + [".mp4",".mp3",".gif"]
        self.cntp = Clock.schedule_interval(self.File, 0)
        self.n1 = n1

    def File(self,*args):
        if self.file.manager_open == False:
            self.cntp.cancel

        if self.n1 == 2 and self.file.path != '':
            self.image = QRimage()
            self.image.source = self.file.path
            self.ids.box.add_widget(self.image)
            self.cntp.cancel()

        elif self.n1 == 3 and self.file.path != '':
            self.video = QRvideo()
            self.video.source = self.file.path
            self.ids.box.add_widget(self.video)
            self.cntp.cancel()

        elif self.n1 == 4 and self.file.path != '':
            self.song = QRaudio()
            self.song.audio = self.file.path
            self.ids.box.add_widget(self.song)
            self.cntp.cancel()

    def menu(self):
        menu = MDGridBottomSheet()
        menu.sheet_list.ids.box_sheet_list.padding = '16dp',0,'16dp','0dp'
        menu.add_item('Texto', lambda x: self.ids.box.add_widget(QRtext()), 'format-text')
        menu.add_item('Imagem', lambda x: self.Path(2),'file-image-outline')
        menu.add_item('Vídeo', lambda x: self.Path(3), 'video')
        menu.add_item('Audio', lambda x: self.Path(4), 'music')
        menu.add_item('Contador', lambda x: self.ids.box.add_widget(QRcount()), 'timer')
        menu.add_item('Mapa', lambda x: self.ids.box.add_widget(QRmap()), 'map')
        menu.open()

    def Guardar(self):
        for i in self.ids.box.children:
            if i.iden == 1:
                itens.append([i.iden,i.text])
            elif i.iden == 2:
                itens.append([i.iden,i.source])
            elif i.iden == 3:
                itens.append([i.iden,i.source])
            elif i.iden == 4:
                itens.append([i.iden,i.audio])
            elif i.iden == 5:
                itens.append([i.iden,i.texto.text])
            elif i.iden == 6:
                itens.append([i.iden,(i.mapa.lat, i.mapa.lon)])

        itens.reverse()

    def Saindo(self):
        self.ids.box.clear_widgets()

        try:
            self.add_widget(self.ids.ajuda)
        except:
            pass

    def Disp(self):
        try:
            self.remove_widget(self.ids.ajuda)
        except:
            pass

class Finaldados(Screen):
    def __init__(self, **args):
        super().__init__(**args)
        self.item = QRitems() 

    def Criar(self):
        global itens, IDs
        #IDs += 1
        QRids[1] = itens
        itens = []

    def on_leave(self):
        try:
            itens.clear()
        except:
            pass

    def ChangeColor(self,cor2):
        self.ids.cor.source = cor2

class Vizualizar(Screen):
    def __init__(self, **args):
        super().__init__(**args)

    def on_pre_enter(self):
        for i in QRids[1]:
            if i[0] == 1:
                self.ids.vizu.add_widget(QRtext(text = i[1]))
            elif i[0] == 2:
                self.img = QRimage()
                self.img.source = i[1]
                self.ids.vizu.add_widget(self.img)
            elif i[0] == 3:
                self.vid = QRvideo()
                self.vid.source = i[1]
                self.ids.vizu.add_widget(self.vid)
            elif i[0] == 4:
                music = QRaudio()
                music.audio = i[1]
                self.ids.vizu.add_widget(music)
            elif i[0] == 5:
                self.con = QRcount()
                self.con.texto.text = i[1]
                self.ids.vizu.add_widget(self.con)
            elif i[0] == 6:
                mapa = QRmap()
                mapa.mapa.lat = i[1][0]
                mapa.mapa.lon = i[1][1]
                self.ids.vizu.add_widget(mapa)

class main(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Teal'
        self.theme_cls.theme_style = 'Dark'
        return Manager()

main().run()
