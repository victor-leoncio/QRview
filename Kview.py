# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2
from pyzbar.pyzbar import decode
import numpy as np
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import threading

class OpenView(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.camera = cv2.VideoCapture(0)
        self.ligar = KivyCamera(self.camera,15)
        self.add_widget(self.ligar)

        def on_stop(self):
            self.camera.release()

class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.time = Clock.schedule_interval(self.update, 1 / fps)
        self.data = None

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
             #convert it to texture
            for barcode in decode(frame):
                self.data = barcode.data
                print(self.data.decode('UTF-8'))
                pts = np.array([barcode.polygon],np.int32)
                pts.reshape(-1,1,2)
                cv2.polylines(frame, pts, True, (255,0,255), 5)
                pts2 = barcode.rect
                cv2.putText(frame,self.data.decode('UTF-8'),(pts2[0]+100, pts2[1]+100),cv2.FONT_HERSHEY_DUPLEX,1,(255, 0, 255))

            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            self.tamax = frame.shape[1]
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture

#class CamApp(App):
#    def build(self):
#        return OpenView()
        #self.capture = cv2.VideoCapture(0)
        #self.my_camera = KivyCamera(capture=self.capture, fps=60)
        #return self.my_camera

    #def on_stop(self):
        #without this, app will not exit even if the window is closed
        #self.capture.release()


#if __name__ == '__main__':
#    CamApp().run()
