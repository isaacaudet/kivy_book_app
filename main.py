import kivy
import re
from kivy.app import App
from kivy.uix.widget import Widget
import urllib.request
import json
import textwrap
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
import cv2
import pytesseract
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import time

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class TextInp(Widget):
    pass


class BookFinder(Widget):
    pass


class Camera(Widget):
    pass


class MainApp(App):
    def build(self):
        return TextInp()

    def isbn_lookup(self, name=''):
        base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
        if name == '':
            name = self.root.ids.input.text

        with urllib.request.urlopen(base_api_link + name) as f:
            text = f.read()

        decoded_text = text.decode("utf-8")
        obj = json.loads(decoded_text)
        volume_info = obj["items"][0]
        authors = obj["items"][0]["volumeInfo"]["authors"]
        print("\nTitle:", volume_info["volumeInfo"]["title"])
        print("\nSummary:\n")
        print(textwrap.fill(volume_info["searchInfo"]["textSnippet"], width=65))
        print("\nAuthor(s):", ",".join(authors))
        print("\nPublic Domain:", volume_info["accessInfo"]["publicDomain"])
        print("\nPage count:", volume_info["volumeInfo"]["pageCount"])
        print("\nLanguage:", volume_info["volumeInfo"]["language"])
        print("\n***")

    def capture(self):
        global isbn
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            timestr = time.strftime("%Y%m%d_%H%M%S")
            name = "IMG_{}.png".format(timestr)
            cv2.imwrite(name, frame)
            isbn = self.nlp_cam(name)
            break
        cap.release()
        cv2.destroyAllWindows()
        print(isbn)

    def nlp_cam(self, img):
        img = cv2.imread(img)
        text = pytesseract.image_to_string(img)
        match = re.search("(?:[0-9]{3}-)?[0-9]{1,5}-[0-9]{1,7}-[0-9]{1,6}-[0-9]", text)
        try:
            name = match.group().replace('-', '')
            self.isbn_lookup(name)
        except AttributeError:
            print('Invalid ISBN. Try again.')
            print(text)


    # def cam_2_isbn(self):
    #     img = self.capture()
    #     print(img)
    #     # print(self.nlp_cam(img))


if __name__ == '__main__':
    MainApp().run()
