import FreeSimpleGUI as sg
#import FreeDragInDropDnD as sg
#import PySimpleGUIQt as sg

import io
import base64
import os
import PIL
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def make_square(im, min_size=256, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = PIL.Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

def convert_to_bytes(file_or_bytes, resize=None, fill=False):
    if isinstance(file_or_bytes, str) and file_or_bytes != '':
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height / cur_height, new_width / cur_width)
        img = img.resize((int(cur_width * scale), int(cur_height * scale)), PIL.Image.LANCZOS)
    if fill:
        if resize is not None:
            img = make_square(img, resize[0])
    with io.BytesIO() as bio:
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()

def func(message='Default message'):
    print(message)

def create_img() :
    imagem = None
    if os.path.isfile('drag.png'):
        img = Image.new("RGB", (400, 400), (255,255,255))
        draw = ImageDraw.Draw(img)
        # Custom font style and font size
        font = ImageFont.load_default()
        #myFont = ImageFont.truetype('FreeMono.ttf', 65)
        myFont = ImageFont.truetype("arial.ttf", 28)
        # Add Text to an image
        draw.text((100, 200), "Drag in Drop image", font=myFont, fill =(0, 0, 0),align='center')
        img.save("drag.png")
        imagem = convert_to_bytes('drag.png')
    else:
        imagem = convert_to_bytes('drag.png')
    return imagem

def replace_file(str):
    return str.replace('{', '').replace('}', '')

class Listbox(sg.Listbox):

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        data = window['LISTBOX'].get_list_values()
        print(data)
        items = [str(v) for v in e.mimeData().text().strip().split('\n')]
        print(items)
        data.extend(items)
        print(data)
        window['LISTBOX'].update(data)
        window.refresh()

    def enable_drop(self):
        # Called after window finalized
        self.Widget.setAcceptDrops(True)
        self.Widget.dragEnterEvent = self.dragEnterEvent
        self.Widget.dragMoveEvent = self.dragMoveEvent
        self.Widget.dropEvent = self.dropEvent


image_viewer_ia = [
                    [sg.Stretch(),sg.Text(key="-FILENAME-"), sg.B(enable_events=True, key='-OPEN_IMG_INPUT-', visible=False, tooltip="Click to open image"),sg.Stretch()],
                    [sg.DnDImage(key="-IMG_VIEWER-", source=create_img() ,tooltip="Drag in drop to open image", size=(400,400), enable_events=False, link_img=None, background_color='#000')],
                    #[sg.DnDImage(source="./resources/dragindrop400.png", key="-IMG_VIEWER-", tooltip="Drag in drop to open image", size=(400,400), enable_events=True, link_img=None, background_color='#fff')],
                ]
layout = [
		#[Listbox([], size=(50, 10), enable_events=True, key='LISTBOX')], 
			[sg.DnDInput('Drag in drop image', size=(60, 10), enable_events=True, key='-INPUT_DND-', change_submits=True)],
            
            [sg.Frame('Input', [
                        #[sg.Text("Image File"),sg.In(size=(60, 1), enable_events=True, key="-FILE-"),sg.FileBrowse(key='-FILE_BROWSE_INPUT-')],
                        [sg.Column(image_viewer_ia)],
                        #[sg.Text("Image File"),sg.Input('Drag in drop image', size=(60, 20), enable_events=True, key='-INPUP-', change_submits=True),sg.FileBrowse(key='-FILE_BROWSE_INPUT-', file_types=[("PNG","*.png"),("JPG","*.jpg"),("JPEG","*.jpeg")])],
                    ])],]

window = sg.Window("Drag in Drop", layout, finalize=True)
#window['LISTBOX'].enable_drop()
IMG_DND_DRAG = None
INPUT_DND_NAME = None
while True:
    event, values = window.read(timeout=1000)
    #print(values )
    if event == sg.WINDOW_CLOSED:
        break
    if callable(event):
        print(event)
        event()

    
    elif event == '-INPUT_DND-' or values['-INPUT_DND-'] != None and values['-INPUT_DND-'] != '' and (os.path.isfile(values['-INPUT_DND-'][1:len(values['-INPUT_DND-'])-1] if (values['-INPUT_DND-'][0] == '{' and values['-INPUT_DND-'][len(values['-INPUT_DND-'])-1] == '}') else values['-INPUT_DND-']) and values['-INPUT_DND-'] != None and values['-INPUT_DND-'] != ''  and INPUT_DND_NAME != values['-INPUT_DND-']):
        #filename = 'C:/Users/aliss/Desktop/Captura de tela 2023-12-19 173350.png'
        filename = values['-INPUT_DND-']
   
        if((filename[0] == '{' and filename[len(filename)-1] == '}')):
            window["-FILENAME-"].update(filename[1:len(filename)-1])
            window['-INPUT_DND-'].update(filename[1:len(filename)-1])
            #window["-IMG_VIEWER-"].update(convert_to_bytes(filename[1:len(filename)-1], (400,400)))
            filename = filename[1:len(filename)-1]
        if not os.path.isfile(filename):
                window["-IMG_VIEWER-"].update(source=create_img())
                window["-FILENAME-"].update('')
        elif os.path.isfile(filename):
                filename = filename.replace('file:///', '')
                INPUT_DND_NAME = filename
                #cls
                # IMG_DND_DRAG = values["-INPUT_DND-"]
                window["-FILENAME-"].update(filename)
                if values['-INPUT_DND-'] != '':
                    window["-IMG_VIEWER-"].update(convert_to_bytes(filename, (400,400)))
                    #window["-OPEN_IMG_INPUT-"].update(visible=True)
    elif (window['-IMG_VIEWER-'].get() != None and IMG_DND_DRAG != replace_file(window['-IMG_VIEWER-'].get())):
        ''' '''
        window["-FILENAME-"].update(replace_file(window['-IMG_VIEWER-'].get()))
        window['-INPUT_DND-'].update(replace_file(window['-IMG_VIEWER-'].get()))
        if window['-IMG_VIEWER-'].get() != '':
            IMG_DND_DRAG = replace_file(window['-IMG_VIEWER-'].get())
            INPUT_DND_NAME = replace_file(window['-IMG_VIEWER-'].get())
            #window["-IMG_VIEWER-"].update(window['-IMG_VIEWER-'].get())
            window["-IMG_VIEWER-"].update(convert_to_bytes(replace_file(window['-IMG_VIEWER-'].get()), (400,400)))#convert_to_bytes(values['INPUT'], (400,400))
            print('img drag', replace_file(window['-IMG_VIEWER-'].get()))
    
    #print(event, values)
    

window.close()