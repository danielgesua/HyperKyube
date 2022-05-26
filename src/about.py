'''
This module contains all code necessary output relevant information about the application
itself to the user.
'''

from __future__ import annotations

from typing import TYPE_CHECKING
from gui_builder import builder

import textwrap
import pathlib
import tkinter

if TYPE_CHECKING:from main import GuiApp

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "about.ui"


class AboutDialog():
    ''' 
    Class that display the standard about dialog for the program, including:
    
     - Version info
     - Name
     - Author
     - Description
     - License
    
    '''

    @property
    def message(self):
        
        separator = '*'*80
        version = 1.0
        author = 'Daniel Gesua'
        release_date = 'May 22nd 2022'
        description = textwrap.dedent(''' 
        HyperKyube is a free and open-source GUI tool designed to automate and simplify
        various tasks related to Google's Tesseract-OCR API. Its primary purpose is 
        editing lstmbox box files for training the LSTM engine, however it can also copy
        text from the images, and automate creation of box files (coming soon!!!).

        Traditionally many of the tasks involved with training of the Tesseract LSTM 
        engine have required cryptic usage of console commands and are made difficult
        by the overwhelming ammount of misinformation found in the world wide web.

        HyperKyube is designed to make editing box files extremely easy and fast in an 
        attempt to "re-democratize" the OCR engine training process and enable 
        Tesseract's expansion and development and subsequent technologies.

        HyperKyube is 100% free and open-source forever and for life for the duration of 
        eternity in all dimensions. The word hypercube refers to the four dimensional 
        analogue of the 3D cube. 
        
        Just as cube is an extension of the square into a third dimension, the hypercube 
        is an extension of the cube into the fourth. The goal of HyperKyube is to 
        elevate the user's experience to new dimensions.

        If you like what we do please consider donating or contributing to the project.
        Your support is greatly appreciated.
        ''')
            
        message = (f'{separator}\n'
            f'{"Version:":<9} {version:<80}'
            f'{"Released:":<9} {release_date:<80}'
            f'{"Author:":<9} {author:<80}'
            f'{separator}'
            f'{description}'
            f'{separator}')
        return message

    def __init__(self, master:GuiApp=None):
        self.tk = tkinter
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        self.mainwindow: tkinter.Toplevel = builder.get_object('about_toplevel', master)
        self.about_message: tkinter.Message = builder.get_object('about_message',master)
        self.about_message.configure(text=self.message)
        builder.connect_callbacks(self)
        self.mainwindow.protocol('WM_DELETE_WINDOW',self.hide)
        self.mainwindow.attributes('-topmost',True)
        self.mainwindow.withdraw()
        
    def show(self):
        self.mainwindow.deiconify()
        self.mainwindow.focus_force()
        self.mainwindow.grab_set()
        self.mainwindow.wait_window()

    def hide(self, event: tkinter.Event = None): 
        self.mainwindow.grab_release()
        self.mainwindow.withdraw()


if __name__ == '__main__':
    app = AboutDialog()
    app.run()