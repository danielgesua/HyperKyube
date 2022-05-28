#
#    HyperKyube: OCR Gui MultiTool.
#
#    Copyright 2022 Daniel Gesua
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#   

''' 
Acts as a centralized location for functions that open a dialog
with the user and [optionally] return the user's response.
'''

from __future__ import annotations

from typing import TYPE_CHECKING


from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.filedialog import askopenfilename


if TYPE_CHECKING: from geometry import WordBox


def display_invalid_value_error():
    ''' 
    Text Editor Input Error: 
    Display an error prompt to let the user know to correct the inputted value.
    '''
    window_title = 'Error.'
    error_message = 'A value is mandatory. Please enter a new value.'
    messagebox.showinfo(window_title,error_message)

def prompt_for_wordbox_text(wordbox: WordBox) -> str|None:
    '''
    Text Editor Text Input:
    Request text from user and return it.
    '''
    window_title = 'Edit text.'
    prompt = 'Value:' + '\t'*10
    return askstring(window_title,prompt,initialvalue=wordbox.core.text)

def prompt_for_boxfile_to_open() -> str:
    ''' 
    Open Box File Dialog:
    Request a box file from the user to open on the canvas and return its path.
    '''
    title = 'Select Box-File to open.'
    valid_filetypes = [('Tesseract Box Files','*.box')]
    return askopenfilename(title=title,filetypes=valid_filetypes)