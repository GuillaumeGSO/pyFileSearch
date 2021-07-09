import PySimpleGUI as sg
from File_Search.file_parser import findFilesInSet
import os, sys
import asyncio

__SEARCHING__ = False
__INTERRUPT__ = False
lst = list()
layout = [
    [sg.InputText(key="-INPUT-", enable_events=True),
     sg.Text(len(lst), size=(10, 1), key="-NB-")],
    [sg.Listbox(values=lst, size=(140, 30),
                key="-RESULT-", tooltip="double click to open", bind_return_key=True), ],
    [sg.Exit()]
]

def merge_nested_if(a, b):
    if a:
        if b:
            return 2


window = sg.Window('Py Simple Search', layout, finalize=True)

async def wait_list(my_set):
    await asyncio.wait([background(my_set), ui()])

def construct_interface(my_set):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_list(my_set))
    loop.close()


async def ui():
    last_search = ''
    global __INTERRUPT__
    global __SEARCHING__
    # Event Loop to process "events"
    while True:
        event, values = window.read(timeout=1)
        if event in (sg.WIN_CLOSED, 'Exit'):
            sys.exit()
        elif event == '-INPUT-':
            if last_search != values['-INPUT-']:
                window['-RESULT-'].update([])
                last_search = values['-INPUT-']
                if __SEARCHING__:
                    __INTERRUPT__ = True
        elif event == '-RESULT-':
            file_clicked = values['-RESULT-'][0]
            if __SEARCHING__:
                    __INTERRUPT__ = True
            os.startfile(file_clicked)
        elif event == '__TIMEOUT__':
            pass
        else:
            print(event, values)
        await asyncio.sleep(0)


async def background(my_set):
    search = ''
    while True:
        if window['-INPUT-'].get() != search:
            search = window['-INPUT-'].get()
            print(search)
            lst.clear()
            window['-NB-'].update(0)
            i = 0
            for r in findFilesInSet(my_set,search):
                i += 1
                lst.append(r)
                global __SEARCHING__
                global __INTERRUPT__
                if __SEARCHING__ and __INTERRUPT__:
                    __INTERRUPT__ = False
                    break
                __SEARCHING__ = True
                if i % 100 == 0:
                    window['-RESULT-'].update(lst)
                    window['-NB-'].update(len(lst))
                await asyncio.sleep(0)
            __SEARCHING__ = False
            __INTERRUPT__= False
            window['-RESULT-'].update(lst)
            window['-NB-'].update(len(lst))
        await asyncio.sleep(0.001)
