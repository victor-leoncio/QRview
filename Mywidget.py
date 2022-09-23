from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from kivy.uix.videoplayer import VideoPlayer
from kivymd.uix.label import MDLabel
from kivy.clock import Clock
from kivymd.toast import toast
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.mapview import MapView
from kivy_garden.mapview import MapMarkerPopup
from kivy.core.audio import SoundLoader
from kivymd.uix.label import MDIcon
from kivymd.uix.button import MDIconButton
from kivymd.uix.slider import MDSlider
from kivy.lang import Builder
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivy.uix.textinput import TextInput

class QRfile():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )
        self.path = ''

    def file_manager_open(self):
        self.file_manager.show('/')
        self.manager_open = True

    def select_path(self, path):
        self.path = path
        self.exit_manager()
        toast(path)

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    #def events(self, instance, keyboard, keycode, text, modifiers):
    #    '''Called when buttons are pressed on the mobile device.'''

    #    if keyboard in (1001, 27):
    #        if self.manager_open:
    #            self.file_manager.back()
    #    return True

class QRtext(TextInput):
    def __init__(self, **args):
        super().__init__(**args)
        self.iden = 1
        self.background_normal = '' 
        self.background_color = [0.188,0.188,0.188,1]
        self.hint_text = 'Digite Algo'
        self.foreground_color= [1,1,1,1]
        self.size_hint_y = None
        self.height = '110dp'
        self.font_size = '20sp'
        self.multiline = True

class QRimage(Image, QRfile):
    def __init__(self, **args):
        super().__init__(**args)
        self.iden = 2
        self.anim_delay = 0.05
        self.anim_loop = 0
        self.size_hint_y = None
        self.height = '200dp'
        self.source = ''

class QRvideo(VideoPlayer):
    def __init__(self, **args):
        super().__init__(**args)
        self.iden = 3
        self.source = ''
        self.size_hint_y = None
        self.height = '400dp'
        self.state = 'play'

class QRaudio(BoxLayout):
    def __init__(self, **args):
        super().__init__(**args)
        self.audio = 'elliot.mp3'

        self.iden = 4
        self.size_hint_y = None
        self.height = '50dp'

        self.box = '''
BoxLayout:
    canvas:
        Color:
            rgba:.10,.10,.10,1
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius:20,20,20,20
    size_hint_y: None
    height: '50dp'
'''
        self.box = Builder.load_string(self.box)

        self.sound = SoundLoader.load(self.audio)
        self.on = False
        self.same = 0.0

        self.audico = MDIcon()
        self.audico.theme_text_color = "Custom"
        self.audico.text_color = [1, 1, 1, 1]
        self.audico.pos_hint = {'center_y':0.5}
        self.audico.icon = 'music'
        self.audico.halign = 'center'

        self.status = MDIconButton()
        self.status.pos_hint = {'center_y':0.5}
        self.status.icon = 'play'
        self.status.bind(on_release = lambda x: self.Som())

        self.slider = MDSlider()
        self.slider.pos_hint = {'center_y':0.5, 'center_x':0.5}
        self.slider.min = 0
        self.slider.max = self.sound.length
        self.slider.value = 0
        self.slider.hint = False

        self.audimax = MDLabel()
        self.audimax.theme_text_color = "Custom"
        self.audimax.text_color = [1, 1, 1, 1]
        self.audimax.bold = True
        self.audimax.text = str(int(self.slider.max / 60)) + ':' + str(int(self.slider.max % 60))
        self.audimax.halign = 'center'

        self.box.add_widget(self.audico)
        self.box.add_widget(self.status)
        self.box.add_widget(self.slider)
        self.box.add_widget(self.audimax)
        self.add_widget(self.box)

    def Som(self):
        self.on = not self.on
        if self.on == True:
            self.sound.play()
            self.status.icon = 'pause'
            self.cnt = Clock.schedule_interval(self.Posi, 0)
        else:
            self.sound.stop()
            self.status.icon = 'play'
            self.cnt.cancel()

    def Posi(self, *args):
        if self.slider.value != self.same:
            self.sound.seek(self.slider.value)
        self.slider.value = self.sound.get_pos()
        self.same = self.slider.value
        self.min = int(self.slider.value / 60)
        self.sec = int(self.slider.value % 60)

        if self.sec < 10:
            self.audimax.text = str(self.min) + ':' + '0' + str(self.sec)
        else:
            self.audimax.text = str(self.min) + ':' + str(self.sec)

    def Change(self):
        self.sound.seek(self.slider.value)

class QRcount(BoxLayout):
    def __init__(self, **args):
        super().__init__(**args)
        self.iden = 5
        self.size_hint_y = None
        self.height= '50dp'

        self.box = '''
BoxLayout:
    canvas:
        Color:
            rgba:.10,.10,.10,1
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius:20,20,20,20
    size_hint_y: None
    height: '50dp'
    size_hint_x:None
    width: self.minimum_width
    pos_hint: {'center_x':0.5,'center_y':0.5}
'''
        self.box = Builder.load_string(self.box)

        self.time = MDIcon()
        self.time.icon = 'timer'
        self.time.halign = 'center'
        self.time.size_hint_x = None
        self.time.width = self.box.height
        self.time.theme_text_color = "Custom"
        self.time.text_color = [1, 1, 1, 1]

        self.texto = MDLabel()
        self.texto.size_hint_y = None
        self.texto.halign = 'center'
        self.texto.height = '50dp'
        self.texto.text = '20'
        self.texto.theme_text_color = 'Custom'
        self.texto.text_color = 1,1,1,1
        self.texto.size_hint_x = None
        self.texto.width = self.box.height

        self.box.add_widget(self.time)
        self.box.add_widget(self.texto)
        self.add_widget(self.box)

        def cont(*args):
            if int(self.texto.text) == 0:
                toast('TERMINOU!')
                self.cnt.cancel()
            else:
                self.texto.text = str(int(self.texto.text) - 1)

        self.cnt = Clock.schedule_interval(cont,1)

class QRmap(BoxLayout):
    def __init__(self, **args):
        super().__init__(**args)
        self.iden = 6
        self.size_hint_y = None
        self.height = '550dp'
        self.orientation = 'vertical'

        self.title = MDLabel()
        self.title.size_hint_y = None
        self.title.height = '50dp'
        self.title.text = 'MAPA'
        self.title.bold = True
        self.title.halign = 'center'
        self.title.theme_text_color = 'Custom'
        self.title.text_color = 1,1,1,1

        self.mapa = MapView()
        self.mapa.size_hint_y = None
        self.mapa.height = '500dp'
        self.mapa.size_hint_x = .85
        self.mapa.pos_hint = {'center_x':0.5}
        self.mapa.lat = -22.809580561286147
        self.mapa.lon = -43.170143727850416
        self.mapa.zoom = 10

        self.mapamarker = MapMarkerPopup()
        self.mapamarker.lat = -22.809580561286147
        self.mapamarker.lon = -43.170143727850416
        self.mapamarker.source = 'marker.png'
        self.mapa.add_widget(self.mapamarker)

        self.add_widget(self.title)
        self.add_widget(self.mapa)

class QRitems(BoxLayout):
    def __init__(self, **args):
        super().__init__(**args)
        self.size_hint_y = None
        self.height = '100dp'
        self.pos_hint = {'top':1}
        self.card = '''
BoxLayout:
    canvas:
        Color:
            rgba:1,1,1,1
        RoundedRectangle:
            pos:self.pos
            size:self.size
            radius:20,20,20,20
    size_hint_y:None
    height:'100dp'
    MDIcon:
        icon:'account'
        halign:'center'
    BoxLayout:
        orientation:'vertical'
        MDLabel:
            text:'Ola'
        MDLabel:
            text:'ola'
    MDIcon:
        icon:'qrcode'
        halign:'center'
'''
        self.card = Builder.load_string(self.card)
        self.add_widget(self.card)
