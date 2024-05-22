import FreeSimpleGUI as sg
import PIL.Image
import io
import base64
import os
from pathlib import Path  # core python module

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
def replace_file(str):
    return str.replace('{', '').replace('}', '')

def is_valid_path(filepath):
    if filepath and Path(filepath).exists():
        return True
    sg.popup_error("Filepath not correct")
    return False
def is_valid_extension(filepath, type):
    if filepath and Path(filepath).exists():
        nome, extensao = os.path.splitext(filepath)
        if (extensao.replace('.', '') in type):
            return True
        else:
            sg.popup_error("Image ou archive not suported 0")
            return False 

    return False

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
                    [sg.Stretch(),sg.Text(key="-FILENAME-"),sg.Stretch()],
                    [sg.DnDImage(key="-IMG_VIEWER-", source= "" + os.path.dirname(__file__) +"/dragindrop400.png" ,tooltip="Drag in drop to open image", size=(400,400), enable_events=False, link_img=None, background_color='#fff')],
            
                ]
layout = [
			[sg.DnDInput('Drag in drop image', size=(60, 10), enable_events=True, key='-INPUT_DND-', is_dnd=True, change_submits=True, key_dnd=lambda: func('Button 1 pressed'))],
            
            [sg.Frame('Input', [
                        [sg.Column(image_viewer_ia)],
                    ])],]

window = sg.Window("Drag in Drop", layout, finalize=True)

IMG_DND_DRAG = None
INPUT_DND_NAME = None
while True:
    event, values = window.read(timeout=1000)
    if event == sg.WINDOW_CLOSED:
        break
    if callable(event):
        print(event)
        event()

    elif event == '-INPUT_DND-' or (os.path.isfile(replace_file(values['-INPUT_DND-'])) and values['-INPUT_DND-'] != None and values['-INPUT_DND-'] != '' and INPUT_DND_NAME != replace_file(values['-INPUT_DND-'])):
            filename = replace_file(values['-INPUT_DND-'])
            INPUT_DND_NAME = filename
            if((values['-INPUT_DND-'][0] == '{' and values['-INPUT_DND-'][len(values['-INPUT_DND-'])-1] == '}')):
                window["-FILENAME-"].update(filename)
                window['-INPUT_DND-'].update(filename)
            if not os.path.isfile(filename) or not is_valid_extension(filename, ('png', 'jpeg', 'jpg', 'mp4')):
                window["-IMG_VIEWER-"].update(source= "" + os.path.dirname(__file__) +"/dragindrop400.png")
                window["-FILENAME-"].update('')
                window['-IMG_VIEWER-'].setLinkImg(None)

            elif os.path.isfile(filename) and is_valid_extension(filename, ('png', 'jpeg', 'jpg', 'mp4')):
                print ('teste ', INPUT_DND_NAME, filename)
                window["-FILENAME-"].update(filename)
                nome, extensao = os.path.splitext(filename)
                if extensao != '.mp4' :
                    window["-IMG_VIEWER-"].update(convert_to_bytes(filename, (400,400)))
                else:
                    window["-IMG_VIEWER-"].update(source= "" + os.path.dirname(__file__) +"/dragindrop400.png")
                    window["-FILENAME-"].update('')
    
    elif (window['-IMG_VIEWER-'].get() != None and IMG_DND_DRAG != replace_file(window['-IMG_VIEWER-'].get())):  # A file was chosen from the listbox
            filename = replace_file(window['-IMG_VIEWER-'].get())
            is_dir = os.path.isdir(filename)
            is_file = os.path.isfile(filename)
            IMG_DND_DRAG = filename
            if(is_file):
                if filename != '' and is_valid_extension(filename, ('png', 'jpeg', 'jpg','mp4')):
                    window["-FILENAME-"].update(filename)
                    window['-INPUT_DND-'].update(filename)
                    nome, extensao = os.path.splitext(filename)
                    if extensao != '.mp4' :
                        window["-IMG_VIEWER-"].update(source=convert_to_bytes(filename, (300,300)))#convert_to_bytes(values['INPUT'], (400,400))
                    else:
                        window["-IMG_VIEWER-"].update(source= "" + os.path.dirname(__file__) +"/dragindrop400.png")
                        window["-FILENAME-"].update('')
                else:
                    #IMG_DND_DRAG = None
                    window["-IMG_VIEWER-"].update(source= "" + os.path.dirname(__file__) +"/dragindrop400.png")
                    window["-FILENAME-"].update('')
                    window['-INPUT_DND-'].update('Drag in Drop File')
            else:
                window["-FILENAME-"].update(filename)
                window['-INPUT_DND-'].update(filename)
                window["-IMG_VIEWER-"].update(source=convert_to_bytes("" + os.path.dirname(__file__) +"/folder.png", (400,400)))

    

window.close()