
import kivy
# kivy.require('1.0.6') # replace with your current kivy version !
#
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import cv2
import numpy as np

class MyGrid(GridLayout):


    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1
        self.inside = GridLayout()
        self.inside.cols = 2


        self.inside.add_widget(Label(text = "Name: "))
        self.name = TextInput(multiline = False)
        self.inside.add_widget(self.name)

        self.inside.add_widget(Label(text = "Last name: "))
        self.last = TextInput(multiline = False)
        self.inside.add_widget(self.last)

        self.inside.add_widget(Label(text = "email: "))
        self.email = TextInput(multiline = False)
        self.inside.add_widget(self.email)

        self.add_widget(self.inside)

        self.submit = Button(text = "click me", font_size = 40)
        self.submit.bind(on_press = self.pressed)
        self.add_widget(self.submit)

    def pressed(self, instance):
        print("my name is mayank singh")
        name = self.name.text
        last = self.last.text
        email = self.email.text

        print(f'First name is: {name} \nLast name is: {last} \nEmail is: {email}')
        
        

        cap = cv2.VideoCapture(0)
        frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        
        frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
        
        out = cv2.VideoWriter("output.avi", fourcc, 5.0, (1280,720))
        
        ret, frame1 = cap.read()
        ret, frame2 = cap.read()
        print(frame1.shape)
        while cap.isOpened():
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5,5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            image, contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
        
                if cv2.contourArea(contour) < 10000:
                    continue
                cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0, 255), 3)
            #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)
        
            image = cv2.resize(frame1, (1280,720))
            out.write(image)
            cv2.imshow("feed", frame1)
            frame1 = frame2
            ret, frame2 = cap.read()
        
            if cv2.waitKey(40) == 27:
                break
        
        cv2.destroyAllWindows()
        cap.release()
        out.release()




class MyApp(App):

    def build(self):
        return MyGrid()


if __name__ == '__main__':
    MyApp().run()